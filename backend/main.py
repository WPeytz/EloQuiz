from flask import Flask, jsonify
import logging, traceback
from datetime import datetime
from flask_cors import CORS
import os

# --- Defensive bootstrap: wrap startup to surface errors in Cloud Run logs ---
try:
  # Defer heavy imports to keep import-time errors within try/except
  from dotenv import load_dotenv
  import firebase_admin
  from firebase_admin import credentials, db, firestore
  # Load environment variables from .env file
  load_dotenv(override=True)

  print("Startup: entered main.py try-block", flush=True)

  # Lazy Firebase initialization to avoid heavy work at process start
  firebase_app = None
  DEFAULT_DB_URL = os.getenv("FIREBASE_DB_URL", "https://adaptivelearning-ff09f-default-rtdb.europe-west1.firebasedatabase.app/")
  def ensure_firebase():
      """
      Ensure a Firebase app exists and has a Realtime Database URL.
      If an app exists but was initialized elsewhere without databaseURL,
      reinitialize it with the required databaseURL so firebase_admin.db works.
      """
      global firebase_app
      try:
          firebase_app = firebase_admin.get_app()
          # Some code paths may have initialized without a DB URL; fix that.
          if not firebase_app.options.get('databaseURL'):
              print("Firebase app exists without databaseURL; reinitializing with DB URL.", flush=True)
              firebase_admin.delete_app(firebase_app)
              raise ValueError("Reinitialize with DB URL")
          return firebase_app
      except ValueError:
          cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "/app/serviceAccountKey.json")
          if not cred_path or not os.path.exists(cred_path):
              raise FileNotFoundError(f"GOOGLE_APPLICATION_CREDENTIALS file not found: {cred_path}")
          cred = credentials.Certificate(cred_path)
          firebase_app = firebase_admin.initialize_app(cred, {'databaseURL': DEFAULT_DB_URL})
          print(f"Firebase Admin initialized with databaseURL={DEFAULT_DB_URL}", flush=True)
          return firebase_app

  from auth import auth_bp
  from quiz import quiz_bp
  from stats import stats_bp


  app = Flask(__name__)
  CORS(app)

  @app.before_request
  def _ensure_firebase_before_request():
      # Initialize lazily; no-op after the first time
      ensure_firebase()

  @app.route('/')
  def index():
      return "Adaptive Learning Backend is running"

  # Register Flask blueprints
  app.register_blueprint(auth_bp)
  app.register_blueprint(quiz_bp)
  app.register_blueprint(stats_bp)

  @app.get("/api/health")
  def health():
      return {"status": "ok", "time": datetime.utcnow().isoformat() + "Z"}, 200

except Exception as e:
  print("Backend startup failed:", str(e), flush=True)
  print("Traceback:\\n" + traceback.format_exc(), flush=True)
  app = Flask(__name__)

  @app.get("/")
  def _failed():
      return {"status": "error", "message": "Startup failed. See logs.", "error": str(e)}, 500

  @app.get("/api/health")
  def _failed_health():
      return {"status": "error"}, 500
  
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host='0.0.0.0', port=port)