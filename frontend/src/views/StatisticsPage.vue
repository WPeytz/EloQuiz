<template>
    <div class="statistics-container">
      <NavBar currentPage="statistics" />
      <h1>Din Statistik</h1>
      <div v-if="loading" class="loading">
        <p>Loader statistik...</p>
      </div>
  
      <div v-else-if="error" class="error">
        <p>{{ error }}</p>
      </div>

      <p v-if="Object.keys(stats).length === 0 && !loading && !error" class="empty-stats">
        Svar på spørgsmål for at se din statistik
      </p>
    
      <div v-for="(data, topic) in stats" :key="topic" class="topic-card">
        <h2>{{ topic }}</h2>
        <p><strong>Nøjagtighed:</strong> {{ data.accuracy }}%</p>
        <p><strong>Elo: </strong> {{Math.round(data.elo) }}</p>
        <p><strong> Antal besvarede i denne kategori: </strong> {{ data.num_answered }}</p>
      </div>

    </div>
  </template>
  
  <script>

  import { getAuth } from "firebase/auth";
  import NavBar from '@/components/NavBar.vue';
  
  const auth = getAuth();
  export default {
    name: "StatisticsPage",
    components: {
      NavBar
    },
    data() {
      return {
        stats: {},
        loading: true,
        user: auth.currentUser,
        error: null
      };
    },
    methods: {
      async fetchStatistics() {
        if (!this.user) {
          this.loading = false;
          this.error = "Bruger ikke logget ind.";
          return;
        }

        try {
          const response = await fetch(`${process.env.VUE_APP_API_URL}/api/get_user_stats?user_id=${this.user.uid}`, {
            method: "GET",
          });

          const data_pre_prossed = await response.json();
          for (const [key, value] of Object.entries(data_pre_prossed.per_topics)) {
            this.stats[key] = {
              accuracy: Math.round(value.accuracy * 100),
              avg_time_per_question: value.avg_time_per_question / 1000,
              skill_level: value.skill_level,
              elo: value.elo, // include the elo returned from the backend
              num_answered: value.num_answered, // assuming backend returns this
            };
            console.log(key, value);
          }
        } catch (err) {
          this.error = "Der opstod en fejl ved hentning af statistik.";
        } finally {
          this.loading = false;
        }
      },
      goBack() {
        this.$router.push("/student-dashboard");
      }
    },
    mounted() {
      this.fetchStatistics();
    }
  };
  </script>
  
  <style scoped>
  .statistics-container {
    max-width: 800px;
    margin: 40px auto;
    text-align: center;
    padding: 20px;
    font-family: 'Arial', sans-serif;
  }
  
  .loading, .error {
    font-size: 1.2rem;
    color: #333;
  }
  
  .empty-stats {
    font-size: 1.2rem;
    color: #555;
    margin: 20px 0;
  }
  
  .stats {
    display: flex;
    flex-direction: column;
    gap: 15px;
  }
  
  .topic-card {
    background: white;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    text-align: left;
  }
  
  h2 {
    margin-bottom: 5px;
    font-size: 1.5rem;
  }
  
  .back-btn {
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1rem;
  }
  
  .back-btn:hover {
    background-color: #0056b3;
  }
  </style>