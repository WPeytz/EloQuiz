<template>
  <div class="questions-container">
    <div class="header">
      <NavBar :currentPage="'student-progress'" />
      <h1 class="page-title">Se Elevfremgang</h1>
    </div>

    <!-- Loading Indicator -->
    <div v-if="loading" class="loading">
      <p>Loader statistik...</p>
    </div>

    <!-- Error Message -->
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
    </div>

    <!-- Students & Their Stats -->
    <div v-else class="questions-list">
      <div v-for="student in students" :key="student.user_id" class="question-card">
        <h2>{{ student.name || student.user_id }}</h2>
        
        <div v-for="(topicData, topicName) in student.stats.per_topics" :key="topicName" class="topic-card">
          <h3>{{ topicName }}</h3>
          <p><strong>Nøjagtighed:</strong> {{ (topicData.accuracy * 100).toFixed(2) }}%</p>
          <p><strong>Elo: </strong>{{ Math.round(topicData.elo) }}</p>
        </div>
        <button @click="removeStudent(student.user_id)" class="remove-btn">Fjern elev</button>
      </div>
      <div class="header-buttons">
        <button class="dashboard" @click="goToDashboard">Tilbage til Forside</button>
      </div>
    </div>
  </div>
</template>

<script>
import { getAuth } from "firebase/auth";
import NavBar from "@/components/NavBar.vue";

export default {
  name: "StudentProgress",
  components: {
    NavBar
  },
  data() {
    return {
      students: [],
      loading: true,
      error: null,
      user: getAuth().currentUser, // The currently logged-in teacher
    };
  },
  methods: {
    async fetchStudents() {
      try {
        const teacherId = this.user.uid;
        const response = await fetch(`${process.env.VUE_APP_API_URL}/api/get_students?user_id=${teacherId}`);
        if (!response.ok) {
          throw new Error("Fejl ved hentning af elever");
        }
        const data = await response.json();
        this.students = data;
        console.log("Elever:", this.students);
      } catch (err) {
        this.error = err.message;
      } finally {
        this.loading = false;
      }
    },
    goToDashboard() {
      this.$router.push("/teacher-dashboard");
    },
    logout() {
      console.log("User logged out");
      this.$router.push("/login");
    },
    async removeStudent(studentId) {
      if (!confirm("Er du sikker på, at du vil fjerne denne elev?")) return;
      try {
        const response = await fetch(`${process.env.VUE_APP_API_URL}/api/remove_student?user_id=${studentId}`, {
          method: "DELETE",
        });
        if (!response.ok) {
          throw new Error("Kunne ikke fjerne eleven.");
        }
        await this.fetchStudents();
      } catch (err) {
        alert("Fejl ved fjernelse af elev: " + err.message);
      }
    },
  },
  mounted() {
    this.fetchStudents();
  },
};
</script>

<style scoped>
.questions-container {
  max-width: 800px;
  margin: 40px auto;
  text-align: center;
  padding: 20px;
}

.header-buttons {
  display: flex;
  justify-content: center; /* Aligns buttons to the right */
  align-items: center;
  gap: 15px; /* Space between buttons */
  margin-bottom: 20px;
}

/* Button styling for header buttons */
.header-buttons .dashboard {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 8px 16px;
  font-size: 1rem;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.header-buttons .dashboard:hover {
  background-color: #0056b3;
  transform: scale(1.05);
}

.loading,
.error {
  font-size: 1.2rem;
  color: #333;
}

.question-card {
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  text-align: left;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.topic-card {
  margin-top: 10px;
  padding: 15px;
  background: #fefefe;
  border-radius: 8px;
  border: 1px solid #eee;
}

.remove-btn {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 8px 12px;
  margin-top: 10px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s ease;
}

.remove-btn:hover {
  background-color: #c82333;
}

.page-title {
  font-weight: bold;
  font-size: 2.2rem;
  color: #2c3e50;
  margin: 20px 0;
}
</style>