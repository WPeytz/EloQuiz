<template>
  <div class="questions-container">
    <div class="header">
      <NavBar currentPage="view-questions" />
    </div>

    <h1> Se Quizspørgsmål</h1>

    <!-- Sorting Options -->
    <div class="sort-options">
      <label for="sort">Sortér efter:</label>
      <select id="sort" v-model="sortOption" @change="sortQuestions">
        <option value="closest">Tættest på 1000 Elo</option>
        <option value="asc">Laveste Elo først</option>
        <option value="desc">Højeste Elo først</option>
      </select>
    </div>

        <!-- Loading Indicator -->
        <div v-if="loading" class="loading">
      <p>Loader spørgsmål...</p>
    </div>

    <!-- Error Message -->
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
    </div>

    <!-- Questions List -->
    <div v-if="questions.length > 0">
      <div 
        v-for="question in questions" 
        :key="question.id" 
        class="question-card"
      >
        <div class="question-info">
          <p class="question-topic">Emne: {{ question.topic }}</p>
          <p class="question-elo">Elo: {{ Math.round(question.elo) }}</p>
          <br>
          <p class="question-text">{{ question.question }}</p>
          <div class="question-answers">
            <p>Svarmuligheder:</p>
            <ul>
              <li v-for="(option, index) in question.options" :key="index">
                <span v-if="option === question.answer"><strong>{{ option }}</strong></span>
                <span v-else>{{ option }}</span>
              </li>
            </ul>
          </div>
          <p class="answered-count">Antal besvarelser: {{ question.answeredCount }}</p>
        </div>
        <button 
          class="delete-btn" 
          @click="deleteQuestion(question.id)"
        >
          Fjern
        </button>
      </div>
      <button class="back-btn" @click="$router.push('/teacher-dashboard')">Tilbage til forside</button>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';

export default {
  name: "ViewQuestions",
  components: {
    NavBar
  },
  data() {
    return {
      questions: [],
      loading: true,
      error: null,
      sortOption: "closest",
    };
  },
  methods: {
    async fetchQuestions() {
      try {
        this.loading = true;
        const response = await fetch(`${process.env.VUE_APP_API_URL}/api/get_questions`);
        if (!response.ok) {
          throw new Error("Fejl ved hentning af spørgsmål");
        }
        const data = await response.json();
        this.questions = data;
        this.sortQuestions();
      } catch (err) {
        this.error = err.message;
      } finally {
        this.loading = false;
      }
    },
    async deleteQuestion(questionId) {
      if (!confirm("Er du sikker på, at du vil fjerne dette spørgsmål?")) return;
      try {
        const response = await fetch(`${process.env.VUE_APP_API_URL}/api/remove_question?question_id=${questionId}`, {
          method: "DELETE"
        });
        if (!response.ok) {
          throw new Error("Fejl ved fjernelse af spørgsmål");
        }
        this.questions = this.questions.filter(q => q.id !== questionId);
      } catch (err) {
        alert(err.message);
      }
    },
    sortQuestions() {
      if (this.sortOption === "asc") {
        this.questions.sort((a, b) => a.elo - b.elo);
      } else if (this.sortOption === "desc") {
        this.questions.sort((a, b) => b.elo - a.elo);
      } else if (this.sortOption === "closest") {
        this.questions.sort((a, b) => Math.abs(a.elo - 1000) - Math.abs(b.elo - 1000));
      }
    }
  },
  mounted() {
    this.fetchQuestions();
  }
};
</script>

<style scoped>
.questions-container {
  max-width: 800px;
  margin: 40px auto;
  padding: 20px;
  font-family: Arial, sans-serif;
  text-align: center;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.header h1 {
  margin: 0;
}

.back-btn {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 8px 16px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.back-btn:hover {
  background-color: #0056b3;
}

.loading,
.error {
  font-size: 1.2rem;
  color: #333;
  margin-top: 20px;
}

.sort-options {
  text-align: left;
  margin-bottom: 20px;
}

.sort-options select {
  margin-left: 10px;
  padding: 5px;
}

.question-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 10px;
  background-color: #fff;
}

.question-info {
  text-align: left;
  flex-grow: 1;
}

.question-topic {
  font-size: 0.95rem;
  color: #555;
  margin-bottom: 5px;
}

.question-elo {
  font-size: 0.95rem;
  color: #333;
  margin-bottom: 5px;
}

.question-text {
  font-size: 1.1rem;
  margin: 0 0 5px 0;
}

.question-answers {
  font-size: 0.9rem;
  color: #333;
}

.question-answers ul {
  margin: 0;
  padding-left: 20px;
}

.delete-btn {
  background-color: #dc3545;
  color: #fff;
  border: none;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
  margin-left: 10px;
}

.delete-btn:hover {
  background-color: #c82333;
}
</style>