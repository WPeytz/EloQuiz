# 📚 EloQuiz – Adaptive Learning with Elo and AI

EloQuiz is an adaptive quiz platform built to help middle school students practice math (and other subjects) through dynamically generated questions. It uses an Elo-based rating system to adjust difficulty, OpenAI's GPT for content generation, and Firebase for user management and data storage.

---

## 🚀 Features

- 📊 **Adaptive Difficulty** – Questions adapt in real-time based on each student's performance.
- 🤖 **AI-Generated Content** – New questions are generated using GPT for different topics and difficulty levels.
- 🎯 **Elo Rating System** – Both students and questions are scored using Elo, just like in chess.
- 👩‍🏫 **Role-Based Dashboards** – Custom interfaces for students, teachers, and administrators.
- 🧪 **Statistics and Progress Tracking** – Real-time performance analytics per topic and student.
- ☁️ **Cloud-Based Deployment** – Hosted on Google Cloud Run with Docker containers.

---

## 🧱 Project Structure
EloQuiz/
├── backend/             # Flask API, Elo logic, OpenAI question generation
├── frontend/            # Vue.js frontend (SPA)
├── .env.example         # Environment variable template
├── deploy.sh            # Deployment script to GCP
└── README.md            # You’re here!

---

## 🛠️ Getting Started

### 🔧 Prerequisites

- Node.js + npm
- Python 3.10+
- Firebase project (with service account key)
- OpenAI API key

### 🚀 Frontend Setup

```bash
npm install -g @vue/cli
cd frontend
npm install
npm run dev

🐍 Backend Setup
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py

⚙️ Environment Variables
Create a .env file in the root and add the following:
GOOGLE_APPLICATION_CREDENTIALS=serviceAccountKey.json
OPENAI_API_KEY=your-openai-key-here
FIREBASE_DATABASE_URL=https://your-project.firebaseio.com

🐳 Deployment
EloQuiz is deployed via Docker and Google Cloud Run.
./deploy.sh
This script builds and deploys both frontend and backend to GCP.

👥 User Roles
	•	Student: Takes quizzes, views streak and performance.
	•	Teacher: Links with students, views stats, manages questions.
	•	Admin: Has tools to reset Elo ratings, manage users and data.

🧠 Built With
	•	Vue.js
	•	Flask
	•	Firebase
	•	OpenAI
	•	Google Cloud Run

🧃 Author

William Peytz – https://www.linkedin.com/in/william-peytz/

🐛 Contributing & Issues

This is a personal research project turned product idea. Contributions are welcome, but please don’t break the Elo formula or teach GPT how to swear in Danish.

📜 License
MIT
