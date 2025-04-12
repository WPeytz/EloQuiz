from flask import Flask, request, jsonify, send_from_directory
from flask import Blueprint, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth, firestore
import os

auth_bp = Blueprint('auth', __name__)  # Define the Blueprint

CORS(auth_bp)  # Allow CORS for this blueprint

if not firebase_admin._apps:
    firebase_admin.initialize_app()

db = firestore.client()

@auth_bp.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    name = data.get('name', '')  # Optional: let them provide a name
    role = data.get('role', 'student')  # Default to 'student' if not provided

    try:
        user = firebase_auth.create_user(email=email, password=password)

        # Save user data to Firestore
        user_doc = {
            "email": email,
            "name": name,
            "role": role,
            "current_streak": 0,
            "longest_streak": 0,
            "elo": {
                "Geometri": 1000,
                "Måling og anvendt matematik": 1000,
                "Brøker, decimaler og procenter": 1000,
                "Simpel Algebra": 1000,
                "De fire regnearter": 1000,
            },
            "question_answers": []
        }

        db.collection('users').document(user.uid).set(user_doc)

        return jsonify({"message": "User created", "uid": user.uid}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400
@auth_bp.route('/api/login', methods=['POST'])
def login():
    # Handle login logic
    return jsonify({"message": "Login endpoint"}), 200

@auth_bp.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "OK"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))  # Use PORT env variable
    auth_bp.run(debug=True, host='0.0.0.0', port=port)