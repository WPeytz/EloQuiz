from flask import Flask, Blueprint, request, jsonify, send_from_directory
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db, firestore
import os
from dotenv import load_dotenv

stats_bp = Blueprint('statistics', __name__)  # Define the Blueprint

CORS(stats_bp)


db_firestore = firestore.client()
@stats_bp.route('/api/get_students', methods=['GET'])
def get_students():
    user_id  = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400
    class_code = db.reference(f"teachers/{user_id}/class_code").get()
    if not class_code:
        return jsonify({"error": "No class found"}), 200
    print(class_code)
    
    students_ref = db_firestore.collection('users').where('teacherCode', '==', class_code)
    students = students_ref.stream()
    
    students_stats = []
    
    for student in students:
        name = student.to_dict().get('name', 'unknown')
        user_id = student.id
        user_ref = db_firestore.collection('answers').where('user_id', '==', user_id)
        user_answers = user_ref.stream()
    
        user_stats = compute_user_stats(user_answers)
        print('************************')
        print(name)
        print(user_stats)
        print('************************')
        for key, _ in user_stats['per_topics'].items():
            user_stats['per_topics'][key]['elo'] = student.to_dict().get('elo', {}).get(key, 1000)
        students_stats.append({
            
            "name": name,
            "elo": student.to_dict().get('elo', 1000),
            "user_id": user_id,
            "stats": user_stats,
        })
    return jsonify(students_stats), 200 
        

def compute_user_stats(user_answers):
    total_questions = 0
    correct_answers = 0
    incorrect_answers = 0
    topics = {}

    # Iterate through each answer document
    for answer in user_answers:
        answer_data = answer.to_dict()
        total_questions += 1
        
        # Get topic name; default to 'unknown' if not provided
        topic = answer_data.get('topic', 'unknown')
        if topic not in topics:
            topics[topic] = {
                'correct_answers': 0,
                'incorrect_answers': 0,
                'total_time': 0,
                'num_times': 0,
            }
        print('topics', topics)
        # Check if the answer is marked as correct (adjust key if needed)
        if answer_data.get('correct'):
            correct_answers += 1
            topics[topic]['correct_answers'] += 1
        else:
            incorrect_answers += 1
            topics[topic]['incorrect_answers'] += 1
        
        # Optionally, accumulate time taken if available
        if 'time_taken' in answer_data:
            topics[topic]['total_time'] += answer_data['time_taken']
            topics[topic]['num_times'] += 1

    # Build per-topic stats including accuracy and average time per question
    per_topics = {}
    print('all topics', topics)
    for topic, stats in topics.items():
        total_topic = stats['correct_answers'] + stats['incorrect_answers']
        accuracy = stats['correct_answers'] / total_topic if total_topic > 0 else 0
        avg_time = stats['total_time'] / stats['num_times'] if stats['num_times'] > 0 else 0

        per_topics[topic] = {
            'accuracy': accuracy,
            'num_answered': total_topic,
            'wlo': 1000
        }
    print(per_topics)
    return {
        'total_questions': total_questions,
        'correct_answers': correct_answers,
        'incorrect_answers': incorrect_answers,
        'per_topics': per_topics
    }

@stats_bp.route('/api/get_user_stats', methods=['GET'])
def get_user_stats():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    # 1. Gather all answers for this user
    user_ref = db_firestore.collection('answers').where('user_id', '==', user_id)
    user_answers = user_ref.stream()
    
    # 2. Generate stats using the helper function
    user_stats = compute_user_stats(user_answers)
    
    # 3. Fetch the user's document to get their stored wlo/elo for each topic
    user_doc = db_firestore.collection('users').document(user_id).get()
    user_data = user_doc.to_dict() or {}
    # Suppose "elo" is the dict field where each topic’s rating is stored
    user_elo = user_data.get('elo', {})  

    # 4. Merge the user’s actual wlo/elo into per_topics
    for topic_name, topic_info in user_stats['per_topics'].items():
        # Default to 1000 if no stored rating
        topic_info['elo'] = user_elo.get(topic_name, 1000)

    return jsonify(user_stats), 200

@stats_bp.route('/api/remove_student', methods=['DELETE'])
def remove_student():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    try:
        # Delete user document
        db_firestore.collection('users').document(user_id).delete()

        # Optionally, also delete their answers (cleanup)
        answers = db_firestore.collection('answers').where('user_id', '==', user_id).stream()
        for answer in answers:
            answer.reference.delete()

        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500