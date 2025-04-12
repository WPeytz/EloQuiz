<template>
  <div class="signup-container">
    <h1>Tilmeld dig EloQuiz.dk</h1>
    <form @submit.prevent="signUp">
      <label for="name">Indtast navn:</label>
      <input type="text" v-model="name" id="name" required />
      
      <label for="email">Email:</label>
      <input type="email" v-model="email" id="email" required />

      <label for="password">Adgangskode:</label>
      <input type="password" v-model="password" id="password" required />

      <label for="role">Vælg din rolle:</label>
      <select v-model="role" id="role" required>
        <option value="student">Elev</option>
        <option value="teacher">Lærer</option>
      </select>

      <button type="submit">Tilmeld dig</button>
    </form>
    <button @click="goToLogin" class="login-button">Tilbage til login</button>
  </div>
</template>

<script>
import { getAuth } from "firebase/auth";

export default {
  data() {
    return {
      name: "",
      email: "",
      password: "",
      role: "student",
    };
  },
  methods: {
    async signUp() {
      try {
        const auth = getAuth();
        const { createUserWithEmailAndPassword, signInWithEmailAndPassword } = await import("firebase/auth");
        const { getFirestore, doc, setDoc } = await import("firebase/firestore");

        // Create user in Firebase Auth
        const userCredential = await createUserWithEmailAndPassword(auth, this.email, this.password);

        // Save additional user data to Firestore
        const db = getFirestore();
        await setDoc(doc(db, "users", userCredential.user.uid), {
          name: this.name,
          email: this.email,
          role: this.role,
          current_streak: 0,
        });

        // Log in the user immediately after signup
        await signInWithEmailAndPassword(auth, this.email, this.password);

        alert("Tilmelding lykkedes! Du bliver nu omdirigeret.");

        if (this.role === "teacher") {
          this.$router.push("/teacher-dashboard");
        } else {
          this.$router.push("/student-dashboard");
        }

      } catch (error) {
        alert("Tilmelding mislykkedes: " + error.message);
      }
    },
    goToLogin() {
      this.$router.push("/login");
    },
  },
};
</script>

<style scoped>
.signup-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px 40px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

/* Ensure consistent sizing across inputs and buttons */
* {
  box-sizing: border-box;
}

button {
  margin-top: 10px;
  background-color: #42b983;
  color: white;
  padding: 10px;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  width: 100%;
}

button:hover {
  background-color: #2a864e;
}

.login-button {
  margin-top: 10px;
  background-color: #888;
}

.login-button:hover {
  background-color: #555;
}

/* Match the inputs/select to the button's width */
select,
input {
  width: 100%;
  padding: 10px;
  margin-top: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}
</style>