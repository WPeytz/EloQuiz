from flask import Flask, Blueprint, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_cors import cross_origin
import firebase_admin
from firebase_admin import credentials, db, firestore
import os
from dotenv import load_dotenv
from google.cloud import secretmanager
import random
import json
from openai import OpenAI


quiz_bp = Blueprint('quiz', __name__)  # Define the Blueprint

CORS(quiz_bp, origins=[
    "https://eloquiz.dk", 
    "http://localhost:8080", 
    "http://127.0.0.1:8080", 
    "http://192.168.0.48:8080" 
])

db_firestore = firestore.client()


# List of common math topics
MATH_TOPICS = ["De fire regnearter", "Brøker, decimaler og procenter", "Måling og anvendt matematik", "Geometri", "Simpel Algebra"]

@quiz_bp.route('/api/get_question', methods=['GET'])
def get_question():
    
    qestion_id = request.args.get('question_id')
    question_ref = db_firestore.collection('questions').document(qestion_id)
    question = question_ref.get().to_dict()
    return jsonify({'id':question})

@quiz_bp.route('/api/get_questions', methods=['GET'])
def get_questions():
    questions_ref = db_firestore.collection('questions').stream()
    all_questions = []
    for doc in questions_ref:
        question_data = doc.to_dict()
        question_data["id"] = doc.id

        # Query the 'answers' collection for all documents referencing this question
        answers_query = db_firestore.collection('answers').where('question_id', '==', doc.id).stream()
        answered_count = sum(1 for _ in answers_query)  # Count the docs
        question_data["answeredCount"] = answered_count

        all_questions.append(question_data)

    return jsonify(all_questions), 200



@quiz_bp.route('/api/remove_question', methods=['DELETE'])
@cross_origin()  # Ensures CORS preflight (OPTIONS) requests are handled
def remove_question():
    question_id = request.args.get('question_id')
    if not question_id:
        return jsonify({"error": "Missing question_id"}), 400

    try:
        # Your logic to remove the question from Firestore
        # For example:
        db_firestore.collection('questions').document(question_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@quiz_bp.route('/api/get_next_question', methods=['GET'])
def get_next_question():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'Missing user_id'}), 400

    try:
        user_ref = db_firestore.collection('users').document(user_id)
        user_snapshot = user_ref.get()
        if not user_snapshot.exists:
            return jsonify({'error': 'User not found'}), 404
        user_data = user_snapshot.to_dict()
        if user_data.get('role') != 'student':
            return jsonify({'error': 'Unauthorized: Only students can start the quiz.'}), 403
    except Exception as e:
        return jsonify({'error': f'Error fetching user data: {str(e)}'}), 500

    # Ensure 'question_answers' list exists in the validated user_data
    if 'question_answers' not in user_data:
        user_data['question_answers'] = []
        db_firestore.collection('users').document(user_id).update({'question_answers': []})

    # If the user has an 'elo' dict, great; otherwise default to {}
    student_elos = user_data.get('elo', {})

    # 1. Gather all existing questions from Firestore
    questions_docs = db_firestore.collection('questions').stream()
    unanswered_questions = []
    for doc in questions_docs:
        # Skip questions the student has already answered
        if doc.id in user_data['question_answers']:
            continue
        qdata = doc.to_dict()
        qdata["id"] = doc.id
        unanswered_questions.append(qdata)
    print("Unanswered questions retrieved:", unanswered_questions)

    # 2. If there are no unanswered questions, generate a new one
    if not unanswered_questions:
        topic = random.choice(MATH_TOPICS)  # pick random topic
        data = {
            'user_id': user_id,
            'topic': topic,
            'difficulty': _get_difficulty_for_student(student_elos, topic)
        }
        question = _gen_question(data)
        return jsonify({'id': question.get('id')})

    # 3. Among unanswered questions, pick the one whose Elo is closest to the student's Elo
    #    for that question's topic. If no student Elo for that topic, default to 1000.
    #    We'll track the minimum absolute difference in Elo.
    best_diff = None
    best_questions = []  # in case multiple have the same diff
    for q in unanswered_questions:
        q_topic = q.get('topic', 'unknown')
        q_elo = q.get('elo', 1000)
        student_elo_for_topic = student_elos.get(q_topic, 1000)
        diff = abs(q_elo - student_elo_for_topic)

        if best_diff is None or diff < best_diff:
            best_diff = diff
            best_questions = [q]
        elif diff == best_diff:
            best_questions.append(q)

    # 4. Pick a random question among those with the smallest diff
    if best_diff is not None and best_diff <= 200:
        chosen_question = random.choice(best_questions)
        if isinstance(chosen_question, dict):
            question_id = chosen_question.get('id')
            print("Chosen question ID:", question_id)
            return jsonify({'id': question_id})
        else:
            print("Chosen question is not a dict:", chosen_question)
            return jsonify({'error': 'Invalid question format'}), 500
    else:
        # No suitable question found, generate a new one
        topic = random.choice(MATH_TOPICS)
        data = {
            'user_id': user_id,
            'topic': topic,
            'difficulty': _get_difficulty_for_student(student_elos, topic)
        }
        question = _gen_question(data)
        print("Question generated via get_next_question route", _get_difficulty_for_student(student_elos, topic))
        if isinstance(question, dict) and 'id' in question:
            return jsonify({'id': question['id']})
        else:
            print("Failed to generate valid question:", question)
            return jsonify({'error': 'Question generation failed'}), 500
    
    
def _get_difficulty_for_student(elos, topic):
    topic_elo = elos.get(topic, 1000)
    if topic_elo >= 1500:
        return "Very Hard"
    elif topic_elo >= 1300:
        return "Hard"
    elif topic_elo >= 1100:
        return "Medium"
    elif topic_elo >= 900:
        return "Easy"
    else:
        return "Very Easy"

def _gen_question(data):

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Missing OpenAI API key")
    client = OpenAI(api_key=api_key)

    user_id = data.get("user_id", "test_user")
    topic = data.get("topic", random.choice(MATH_TOPICS))
    
    user_ref = db_firestore.collection('users').document(user_id)
    user_data = user_ref.get().to_dict() or {}
    student_elos = user_data.get('elo', {})
    difficulty = data.get("difficulty") or _get_difficulty_for_student(student_elos, topic)

    user_ref = db.reference(f'performance/{user_id}')
    performance_data = user_ref.get() or {"correct_streak": 0, "incorrect_streak": 0}
    correct_streak = performance_data.get("correct_streak", 0)

    prompt = f"""
    Create a unique {difficulty}-level multiple-choice question about {topic}.
    Use random numbers and vary the math operations involved to ensure the questions are not repetitive.
    Ask the questions in danish language.

    Return ONLY valid JSON with the following structure (and nothing more):
    {{
        "question": "<Your question text>",
        "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
        "answer": "<One correct option from the above>"
    }}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",  
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_completion_tokens=200
    )

    try:
        raw_content = str(response.choices[0].message.content.strip().replace("json\n", "").replace("```", ""))
        question_obj = json.loads(raw_content)
    except Exception as e:
        print("JSON parse error:", str(e))
        return {"error": "Invalid question format"}

    question_obj["correct_streak"] = correct_streak
    
    if difficulty == "Very Easy":
        initial_elo = 800
    elif difficulty == "Easy":
        initial_elo = 1000
    elif difficulty == "Medium":
        initial_elo = 1200
    elif difficulty == "Hard":
        initial_elo = 1400
    elif difficulty == "Very Hard":
        initial_elo = 1600
    else:
        initial_elo = 1000
    try:
        _, doc_ref = db_firestore.collection('questions').add({
            'question': question_obj["question"],
            'options': question_obj["options"],
            'answer': question_obj["answer"],
            'topic': topic,
            'difficulty': difficulty,
            'elo': initial_elo,
        })
        
        question_obj["id"] = doc_ref.id
        print("Generated question with ID:", doc_ref.id)
        question_obj["topic"] = topic
        question_obj["difficulty"] = difficulty
        question_obj["elo"] = initial_elo

        return question_obj

    except Exception as e:
        print("Failed to store question:", str(e))
        return {"error": "Could not save question", "details": str(e)}


@quiz_bp.route('/api/generate_question', methods=['POST'])
def generate_question():
    try:
        data = request.get_json()
        question_obj =  _gen_question(data)
        
        return jsonify(question_obj), 200

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500


def update_elo(student_elo, question_elo, score_student, score_question, k=32):
    expected_student = 1 / (1 + 10 ** ((question_elo - student_elo) / 400))
    expected_question = 1 - expected_student

    new_student_elo = student_elo + k * (score_student - expected_student)
    new_question_elo = question_elo + k * (score_question - expected_question)

    return new_student_elo, new_question_elo

@quiz_bp.route('/api/submit_answer', methods=['POST'])
def submit_answer():
    data = request.get_json()
    user_id = data.get('user_id')
    response_time = data.get('response_time')
    question_id = data.get('question_id')
    is_correct = data.get('is_correct')

    # Fetch the question document
    question_doc = db_firestore.collection('questions').document(question_id).get()
    question_data = question_doc.to_dict()
    if not question_data:
        return jsonify({"error": "Question not found"}), 404
    # Get the topic and question Elo (default to 1000 if not set)
    topic = question_data.get('topic')
    question_elo = question_data.get('elo', 1000)
    
    # Fetch the user's document and get the student's Elo for this topic.
    user_doc = db_firestore.collection('users').document(user_id).get()
    user_data = user_doc.to_dict() or {}
    # Update current streak only if the previous answer was correct
    previous_streak = user_data.get('current_streak', 0)

    if is_correct:
        user_data['current_streak'] = previous_streak + 1
    else:
        user_data['current_streak'] = 0

    user_data['longest_streak'] = max(user_data.get('longest_streak', 0), user_data['current_streak'])
    db_firestore.collection('users').document(user_id).update(user_data)
            
    
    # 'elo' is now a dict mapping topics to Elo ratings.
    student_elos = user_data.get('elo', {})
    student_elo = student_elos.get(topic, 1000)
    
    # Custom scoring for "don't know" response
    if is_correct is None:
        score_student = 0.25
        score_question = 0.75
    else:
        score_student = 1 if is_correct else 0
        score_question = 0 if is_correct else 1

    # Compute new Elo scores
    new_student_elo, new_question_elo = update_elo(student_elo, question_elo, score_student, score_question)
    
    # Update the student's Elo for the topic
    student_elos[topic] = new_student_elo
    db_firestore.collection('users').document(user_id).update({'elo': student_elos})
    user_doc = db_firestore.collection('users').document(user_id).get()
    
    user_data = user_doc.to_dict()
    print(user_data)
    if not user_data.get('question_answers', False):
      db_firestore.collection('users').document(user_id).update({'question_answers': [question_id]})
    else:        
        user_data['question_answers'].append(question_id)
        db_firestore.collection('users').document(user_id).update(user_data)
        
    # Update the question's Elo rating
    db_firestore.collection('questions').document(question_id).update({'elo': new_question_elo})
    
    answer  = {
        'topic': topic,
        'time_taken': response_time,
        'user_id': user_id,
        'question_id': question_id,
        'correct': is_correct,
        'user_elo': student_elo,
        'question_elo': question_elo,
        
    }
    db_firestore.collection('answers').add(answer)
    # You might update performance or streaks here as needed.
    return jsonify({
        'student_elo': new_student_elo,
        'question_elo': new_question_elo,
        'current_streak': user_data['current_streak']
    }), 200


def update_student_performance(user_id, topic, is_correct, response_time, question_id):
    student_ref = db.reference(f"students/{user_id}/topics/{topic}")
    print("Updating student performance for", user_id, topic, is_correct, response_time)
    db_firestore.collection('answers').add({
        'time': response_time,
        'correct': is_correct,
        'topic': topic,
        'user_id': user_id,
        'question_id': question_id
    })
    
    user_ref  = db_firestore.collection('users').document(user_id)
    user_data = user_ref.get().to_dict()
    print(user_data)
    if not user_data.get('question_answers', False):
        user_ref.update({
            "question_answers": [question_id]
        })
    else:
        user_ref.update({
            "question_answers": user_data.question_answers.append(question_id)
        })

    
    student_data = student_ref.get() or {"accuracy": 0, "avg_time_per_question": 0, "total_questions": 0, "total_time": 0}

    # Update accuracy
    total_questions = student_data["total_questions"] + 1
    correct_answers = (student_data["accuracy"] * student_data["total_questions"] / 100) + (1 if is_correct else 0)
    new_accuracy = (correct_answers / total_questions) * 100

    # Update database
    student_ref.update({
        "accuracy": round(new_accuracy, 2),
        "total_questions": total_questions,
    })
    
@quiz_bp.route('/api/reset_student_elo', methods=['POST'])
def reset_student_elo():
    data = request.get_json()
    user_id = data.get('user_id')
    
    try:
        user_ref = db_firestore.collection('users').document(user_id)
        user_ref.update({'elo': {}})
        return jsonify({"message": f"Elo ratings reset for user {user_id}."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@quiz_bp.route('/api/reset_question_elo', methods=['POST'])
def reset_question_elo():
    try:
        questions_ref = db_firestore.collection('questions').stream()
        for doc in questions_ref:
            difficulty = doc.to_dict().get('difficulty', 'Medium')
            if difficulty == "Very Easy":
                initial_elo = 800
            elif difficulty == "Easy":
                initial_elo = 1000
            elif difficulty == "Medium":
                initial_elo = 1200
            elif difficulty == "Hard":
                initial_elo = 1400
            elif difficulty == "Very Hard":
                initial_elo = 1600
            else:
                initial_elo = 1000
            doc.reference.update({'elo': initial_elo})
            # Archive all answers related to this question
            answers_query = db_firestore.collection('answers').where('question_id', '==', doc.id).stream()
            for answer_doc in answers_query:
                answer_data = answer_doc.to_dict()
                db_firestore.collection('archived_answers').add(answer_data)
                answer_doc.reference.delete()
        return jsonify({"message": "Elo ratings reset to inital Elo for all questions."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
@quiz_bp.route('/api/pre_generate_questions', methods=['POST'])
def pre_generate_questions():
    try:
        for difficulty in ["Very Easy", "Easy", "Medium", "Hard", "Very Hard"]:
            for topic in MATH_TOPICS:
                for _ in range(1):  # Adjust number of questions per pair here
                    data = {
                        "user_id": "system",
                        "topic": topic,
                        "difficulty": difficulty
                    }
                    _gen_question(data)
        return jsonify({"message": "Questions pre-generated successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))  # Use PORT env variable
    quiz_bp.run(debug=True, host='0.0.0.0', port=port)