<template>
  <div class="navbar-wrapper">
    <nav class="navbar">
      <div class="navbar-title" @click="$router.push('/')">{{ title }}</div>
      <div class="navbar-right">
        <ul class="navbar-links">
          <li v-for="(link, index) in computedLinks" :key="index">
            <router-link :to="link.path">{{ link.label }}</router-link>
          </li>
          <li>
            <button class="logout-button" @click="logout">Log ud</button>
          </li>
        </ul>
      </div>
    </nav>
  </div>
</template>

<script>
import { getAuth, signOut } from "firebase/auth";

export default {
  name: 'NavBar',
  props: {
    title: {
      type: String,
      default: 'EloQuiz.dk'
    },
    currentPage: {
      type: String,
      default: ''
    },
    links: {
      type: Array,
      default: () => []
    }
  },
  computed: {
    computedLinks() {
      if (this.currentPage === 'view-questions') {
        return [
          { label: 'Forside', path: '/teacher-dashboard' },
          { label: 'Se Elevfremgang', path: '/student-progress' }
        ];
      } else if (this.currentPage === 'student-progress') {
        return [
          { label: 'Forside', path: '/teacher-dashboard' },
          { label: 'Se Quizspørgsmål', path: '/view-questions' }
        ];
      } else if (this.currentPage === 'quiz-screen') {
        return [
          { label: 'Forside', path: '/student-dashboard' },
          { label: 'Statistik', path: '/statistics' }
        ];
      } else if (this.currentPage === 'statistics') {
        return [
          { label: 'Forside', path: '/student-dashboard' },
          { label: 'Quiz', path: '/quiz' }
        ];
      }
      return this.links;
    }
  },
  methods: {
    logout() {
      const auth = getAuth();
      localStorage.clear();
      sessionStorage.clear();
      signOut(auth).then(() => {
        this.$router.push('/login');
      }).catch(error => {
        console.error('Logout failed:', error);
      });
    }
  }
}
</script>

<style scoped>
.navbar-wrapper {
  background-color: #f8f9fa;
  padding: 1rem 2rem;
  width: 100%;
  box-sizing: border-box;
  display: flex;
  justify-content: center;
}

.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

body {
  margin: 0;
  overflow-x: hidden;
}

.navbar-title {
  font-size: 1.5rem;
  font-weight: bold;
  cursor: pointer;
  white-space: nowrap;
  margin-right: auto;
}

.navbar-right {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  flex: 1;
}

.navbar-links {
  list-style: none;
  display: flex;
  gap: 1rem;
  align-items: center;
  margin: 0;
  padding: 0;
}

.navbar-links li {
  margin: 0;
}

.navbar-links a {
  color: #333;
  text-decoration: none;
}

.navbar-links a:hover {
  text-decoration: underline;
}

.logout-button {
  background-color: #e74c3c;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  cursor: pointer;
  font-size: 1rem;
  border-radius: 4px;
}

.logout-button:hover {
  background-color: #c0392b;
}
</style>
