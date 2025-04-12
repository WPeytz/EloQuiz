<template>
    <div class="admin-panel">
      <h2>Admin Interface</h2>
  
      <div class="reset-section">
        <h3>Reset Student Elo</h3>
        <input v-model="studentId" placeholder="Enter Student ID" />
        <button @click="resetStudentElo">Reset Student Elo</button>
      </div>
  
      <div class="reset-section">
        <h3>Reset All Questions Elo</h3>
        <button @click="resetQuestionElo">Reset Question Elo</button>
      </div>

      <div class="logout-section">
        <button @click="logout">Log ud</button>
      </div>
  
      <div v-if="message">{{ message }}</div>
      <div v-if="error" class="error">{{ error }}</div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        studentId: '',
        message: '',
        error: ''
      };
    },
    methods: {
      async resetStudentElo() {
        try {
          const response = await axios.post(`${process.env.VUE_APP_API_URL}/api/reset_student_elo`, {
            user_id: this.studentId
          });
          this.message = response.data.message;
          this.error = '';
        } catch (err) {
          this.error = err.response?.data?.error || 'Error resetting student Elo';
          this.message = '';
        }
      },
  
      async resetQuestionElo() {
        if (!confirm('Are you sure you want to reset Elo for all questions?')) return;
  
        try {
          const response = await axios.post(`${process.env.VUE_APP_API_URL}/api/reset_question_elo`);
          this.message = response.data.message;
          this.error = '';
        } catch (err) {
          this.error = err.response?.data?.error || 'Error resetting question Elo';
          this.message = '';
        }
      },
      logout() {
        this.$router.push('/login');
      }
    }
  };
  </script>
  
  <style scoped>
  .admin-panel {
    padding: 20px;
    background-color: #f9f9f9;
  }
  
  .reset-section {
    margin-bottom: 20px;
  }
  
  input {
    margin-right: 10px;
    padding: 5px;
  }
  
  button {
    padding: 5px 10px;
  }
  
  .error {
    color: red;
  }

  .logout-section {
    margin-top: 30px;
  }

  .logout-section button {
    background-color: #d9534f;
    color: white;
    border: none;
    padding: 8px 16px;
    cursor: pointer;
    border-radius: 4px;
  }

  .logout-section button:hover {
    background-color: #c9302c;
  }
  </style>