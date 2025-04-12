from flask import Flask, Blueprint, request, jsonify, send_from_directory
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db, firestore
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

# Check if GOOGLE_APPLICATION_CREDENTIALS is set correctly
cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "/app/serviceAccountKey.json")
if not cred_path or not os.path.exists(cred_path):
    raise FileNotFoundError(f"GOOGLE_APPLICATION_CREDENTIALS file not found: {cred_path}")

# Load Firebase credentials
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://adaptivelearning-ff09f-default-rtdb.europe-west1.firebasedatabase.app/'
})

from auth import auth_bp
from quiz import quiz_bp
from statistics import stats_bp


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "Adaptive Learning Backend is running"

# Register Flask blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(quiz_bp)
app.register_blueprint(stats_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)