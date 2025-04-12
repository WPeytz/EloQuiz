<template>
  <div class="login-container">
    <div class="login-box">
      <h1>Velkommen til EloQuiz.dk</h1>
      <p>Log ind for at fortsætte din læringsrejse.</p>
      <form @submit.prevent="login">
        <div class="form-group">
          <label for="email">Email</label>
          <input v-model="email" type="email" id="email" placeholder="Indtast din email" required />
        </div>
        <div class="form-group">
          <label for="password">Adgangskode</label>
          <input v-model="password" type="password" id="password" placeholder="Indtast din adgangskode" required />
        </div>
        <button class="login-button" type="submit" :disabled="loading">
          {{ loading ? "Logger ind..." : "Log ind" }}
        </button>
      </form>
      <div class="additional-links">
        <p>Har du ikke en konto? <button @click="goToSignUp" class="link-button">Tilmeld dig</button></p>
      </div>
    </div>
  </div>
</template>

<script>
import { getAuth, signInWithEmailAndPassword } from "firebase/auth";
import { getFirestore, doc, getDoc } from "firebase/firestore";
import firebaseApp from "../firebase";

export default {
  name: "UserLogin",
  data() {
    return {
      email: "",
      password: "",
      loading: false, // Added loading state for UI feedback
    };
  },
  methods: {
    async login() {
      const auth = getAuth(firebaseApp);
      this.loading = true; // Show loading state

      try {

        const userCredential = await signInWithEmailAndPassword(auth, this.email, this.password);
        debugger;
        const user = userCredential.user;
        console.log("User logged in:", user);

        // Fetch user role from Firestore
        const db = getFirestore();
        const userRef = doc(db, "users", user.uid);
        const userDoc = await getDoc(userRef);

        if (userDoc.exists()) {
          const userRole = userDoc.data().role;
          console.log("User role:", userRole);

          if (userRole === "teacher") {
            this.$router.push("/teacher-dashboard");
          } else if (userRole === "student") {
            this.$router.push("/student-dashboard");
          } else if (userRole === "admin") {
            this.$router.push("/admin-panel");
          } else {
            console.error("Unknown user role:", userRole);
            alert("Fejl: Ukendt brugerrolle.");
          }
        } else {
          console.error("User data not found in Firestore");
          alert("Fejl: Brugerdata ikke fundet.");
        }
      } catch (error) {
        console.error("Login error:", error.message);
        alert("Login mislykkedes: " + error.message);
      } finally {
        this.loading = false; // Reset loading state
      }
    },
    goToSignUp() {
      this.$router.push("/signup");
    },
  },
};
</script>

<style scoped>
/* Container styling */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f4f4f9;
  font-family: Arial, sans-serif;
}

/* Login box */
.login-box {
  background: #ffffff;
  padding: 20px 40px;
  border-radius: px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
  max-width: 400px;
  width: 100%;
}

/* Heading */
h1 {
  color: #333;
  margin-bottom: 10px;
}

p {
  color: #666;
  font-size: 14px;
  margin-bottom: 20px;
}

/* Form group */
.form-group {
  margin-bottom: 15px;
  text-align: left;
}

label {
  display: block;
  font-size: 14px;
  color: #333;
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 10px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

/* Login button */
.login-button {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  width: 100%;
  transition: background-color 0.3s ease;
}

.login-button:hover {
  background-color: #2a864e;
}

.login-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

/* Additional links */
.additional-links {
  margin-top: 15px;
}

.link-button {
  background: none;
  border: none;
  color: #42b983;
  cursor: pointer;
  font-size: 14px;
  text-decoration: underline;
}

.link-button:hover {
  color: #2a864e;
}

/* Responsive design */
@media (max-width: 768px) {
  .login-box {
    padding: 15px;
    border-radius: 8px;
  }

  h1 {
    font-size: 20px;
  }

  p {
    font-size: 13px;
  }

  input,
  .login-button {
    font-size: 14px;
  }
}
</style>