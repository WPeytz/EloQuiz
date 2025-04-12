<template>
  <div class="quiz-container">
    <div class="header">
      <NavBar :currentPage="'quiz-screen'" />
    </div>

    <div class="quiz-card">
      <h1 class="title">Quiz Spørgsmål</h1>

      <!-- Loading State -->
      <div v-if="loading" class="loading">
        <p>Loader spørgsmål...</p>
        <div class="spinner"></div>
      </div>
      
      <!-- Error State -->
      <div v-else-if="error" class="error">
        <p>{{ error }}</p>
        <button @click="loadQuestion" class="retry-btn">Prøv igen</button>
      </div>

      <!-- Quiz Question & Answers -->
      <div v-else>
        <div class="question-wrapper">
          <p class="question">{{ questionData.question }}</p>
          <div class="options">
            <button
              v-for="(option, index) in questionData.options"
              :key="index"
              :class="[
                'option-btn',
                {
                  correct: selectedOption === option && isCorrect,
                  incorrect: selectedOption === option && !isCorrect,
                  'show-correct': selectedOption !== null && option === questionData.answer && !isCorrect,
                }
              ]"
              @click="checkAnswer(option)"
              :disabled="selectedOption !== null"
            >
              {{ option }}
            </button>
            <button
              class="option-btn"
              @click="checkAnswer('Ved ikke')"
              :disabled="selectedOption !== null"
            >
              Ved ikke
            </button>
          </div>
          <div v-if="feedbackSubmitted" class="feedback">
            
            <p>Din nuværende streak: {{ correctStreak }}</p>
            
          <!-- Next Question Button -->
          <button
            @click="loadNextQuestion" 
            class="next-btn"
          >
            Næste spørgsmål
          </button>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import { auth } from '../firebase'; //AuthStateChanged
import { getFirestore, doc, getDoc } from 'firebase/firestore';
import NavBar from '@/components/NavBar.vue';

export default {
  name: "QuizScreen",
  components: {
    NavBar
  },
  data() {
    return {
      user: auth.currentUser,
    
      questionData: {
        question: "",
        options: [],
        answer: "",
        topic: "",
        difficulty: "",
        id: "",
      },
     
      loading: true,
      error: null,
      feedback: null,
      isCorrect: false,
      selectedOption: null, // Track the user's selected option
      correctStreak: 0, // Keep track of the correct streak
      feedbackSubmitted: false, // Track if feedback has been submitted
    };
  },
  methods: {
    async loadNextQuestion(){
      const response = await fetch(`${process.env.VUE_APP_API_URL || ''}/api/get_next_question?user_id=${this.user.uid}`, {
        method: "GET",
      });
      const data = await response.json();
      if (data.id) {
        await this.$router.push(`/quiz/${data.id}`);
        await this.loadQuestion(); // Ensure question loads after route change
      } else {
        console.error("No question ID returned from API:", data);
        this.error = "Kunne ikke hente næste spørgsmål.";
      }
    },

    async loadQuestion() {
   
      this.loading = true;
      this.error = null;
      this.feedback = null;
      this.selectedOption = null;
      this.feedbackSubmitted = false; // Reset feedback submission state

      try {
        const response = await fetch(`${process.env.VUE_APP_API_URL || ''}/api/get_question?question_id=${this.$router.currentRoute.value.params.id}`, {
          method: "GET",
        });

        if (!response.ok) {
          throw new Error("Failed to load question");
        }
       
        const data = await response.json();

        this.questionData = data.id;
        this.loading = false;
        this.start_time =  Date.now()
      } catch (err) {
        this.error = "Failed to load quiz question. Please try again.";
        this.loading = false;
      }
    },

    checkAnswer(selectedOption) {
      if (this.selectedOption !== null) return; // Prevent multiple clicks
 
      this.selectedOption = selectedOption; // Mark the selected option
      if (selectedOption === 'Ved ikke') {
        this.correctStreak = 0;
        this.feedbackSubmitted = true;
        this.updateStreak(null);
        return;
      }
      const normalizedSelected = selectedOption.trim().toLowerCase();
      const normalizedAnswer = this.questionData.answer.trim().toLowerCase();
      const isCorrect = normalizedSelected.slice(2) === normalizedAnswer.slice(2);

      this.isCorrect = isCorrect;
      this.feedbackSubmitted = true;

      this.updateStreak(isCorrect);
      if (!isCorrect) {
        this.correctStreak = 0;
      }
    },

    async updateStreak(isCorrect) {
      try {
        const stop_time = Date.now();
        console.log(this.user)

        const response = await fetch(`${process.env.VUE_APP_API_URL || ''}/api/submit_answer`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            user_id: this.user.uid,
            is_correct: isCorrect,
            response_time: stop_time - this.start_time,   // Hardcoded response time for now
            question_id:  this.$router.currentRoute.value.params.id,
            topic: this.questionData.topic,
          }),
        });

        const data = await response.json();
        if (typeof data.correct_streak === 'number') {
          this.correctStreak = data.correct_streak;
        } else if (isCorrect) {
          this.correctStreak += 1;
        }
      } catch (error) {
        console.error("Failed to update streak:", error);
      }
    },

    async submitFeedback(difficulty) {
      try {
        await fetch(`${process.env.VUE_APP_API_URL || ''}/api/feedback`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            user_id: this.user.uid,
            question: this.questionData.question,
            difficulty: difficulty,
          }),
        });
        this.feedbackSubmitted = true; // Mark feedback as submitted
        console.log(`Feedback '${difficulty}' submitted successfully.`);
      } catch (error) {
        console.error("Failed to submit feedback:", error);
      }
    },
  },
  async mounted() {
    const waitForAuth = () => {
      return new Promise((resolve) => {
        const unsubscribe = auth.onAuthStateChanged((user) => {
          if (user) {
            this.user = user;
            unsubscribe(); // stop listening
            resolve();
          } else {
            // Redirect if no user
            this.$router.push('/');
          }
        });
      });
    };

    await waitForAuth();

    const db = getFirestore();
    const userRef = doc(db, "users", this.user.uid);
    const userDoc = await getDoc(userRef);
    console.log(userDoc.data());
    this.correctStreak = userDoc.data().current_streak || 0;
    const role = userDoc.data().role;
    if (role !== 'student') {
      this.$router.push('/');
      return;
    }

    if (!this.$route.params.id) {
      await this.loadNextQuestion();
    } else {
      await this.loadQuestion();
    }
  },
};
</script>

<style scoped>
/* General Container Styles */
.quiz-container {
  max-width: 800px;
  margin: 40px auto;
  text-align: center;
  padding: 20px;
}

.quiz-card {
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  padding: 10px 30px 30px 30px;
  margin-top: 0;
}

.header {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

/* Title on the far left, buttons on the far right */
.title {
  margin: 0 0 10px 0;
}

.header-buttons {
  display: flex;
  gap: 10px; /* Decrease spacing between buttons */
}
.nav-button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 8px 15px;
  font-size: 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.nav-button:hover {
  background-color: #0056b3;
  transform: scale(1.05);
}

/* Loading State */
.loading p {
  font-size: 1.2rem;
  color: #333;
}

.spinner {
  margin: 10px auto;
  width: 30px;
  height: 30px;
  border: 4px solid #ccc;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* Error State */
.error {
  color: red;
  font-weight: bold;
}

.retry-btn {
  margin-top: 10px;
  padding: 10px 20px;
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
}

.retry-btn:hover {
  background-color: #c62828;
}

/* Question & Options */
.question {
  font-size: 1.4rem;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.option-btn {
  background-color: #e7e7e7;
  border: none;
  padding: 10px 15px;
  font-size: 1.1rem;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.option-btn:hover {
  background-color: #d6d6d6;
  transform: scale(1.05);
}

.option-btn.correct {
  background-color: #4caf50; /* Green for correct answers */
  color: white;
}

.option-btn.incorrect {
  background-color: #f44336; /* Red for incorrect answers */
  color: white;
}

.option-btn.show-correct {
  background-color: #4caf50; /* Highlight the correct answer */
  color: white;
}

/* Feedback */
.feedback {
  margin-top: 20px;
  font-size: 1.2rem;
}

.feedback-correct {
  color: #4caf50;
}

.feedback-incorrect {
  color: #f44336;
}

/* Next Question Button */
.next-btn {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
}

.next-btn:hover {
  background-color: #0056b3;
}

/* Styles for Feedback Buttons */
.feedback-buttons {
  margin-top: 20px;
  text-align: center;
}

.feedback-title {
  font-size: 1.2rem;
  margin-bottom: 10px;
  font-weight: bold;
}

.feedback-buttons-group {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
}

.feedback-btn {
  background-color: #f0f0f0;
  color: #333;
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.feedback-btn:hover {
  background-color: #007bff;
  color: white;
  transform: scale(1.05);
}

.skip-btn {
  background-color: #f0f0f0;
  color: black;
}

.skip-btn:hover {
  background-color: #c62828;
}

/* Next Button */
.next-btn {
  margin-top: 20px;
  padding: 12px 20px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1.2rem;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.next-btn:hover {
  background-color: #218838;
}

/* Streak Container */
.streak-container {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  font-family: 'Arial', sans-serif;
}

/* Streak Label */
.streak-label {
  font-size: 1.2rem;
  font-weight: bold;
  margin-right: 10px;
  color: #333;
}

/* Streak Badge */
.streak-badge {
  display: inline-block;
  background-color: #4caf50; /* Green for success */
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
  padding: 5px 15px;
  border-radius: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  /* animation: streak-pulse 1.5s infinite ease-in-out; */
}

/* Badge Animation */
@keyframes streak-pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

.question-wrapper {
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  padding: 30px;
  margin-top: 10px;
}
</style>