<template>
  <div class="dashboard-container">
    <h1>Lærer Dashboard</h1>
    <h2 v-if="user">Velkommen, {{ user.name }}</h2>
    <h2 v-else>Velkommen!</h2>

    <button @click="generateCode">Generér Klassens Kode</button>
    <p v-if="classCode">Din klassekode: <strong>{{ classCode }}</strong></p>

    <button @click="viewStudentProgress">Se Elevfremgang</button> 
    <button @click="$router.push('/view-questions')"> Se Quizspørgsmål </button>
    <button @click="giveFeedback">Giv Feedback</button>
    <button @click="logOut" class="logout-button">Log ud</button>
  </div>
</template>

<script>
import { getAuth, signOut } from "firebase/auth";
import { getDatabase, ref, get, set } from "firebase/database";
import { getFirestore, doc, getDoc } from "firebase/firestore";

export default {
  data() {
    return {
      classCode: null,
      students: [],
      user: {
        displayName: ""
      },
    };
  },
  mounted() {
    const auth = getAuth();
    auth.onAuthStateChanged((user) => {
      if (user) {
        const db = getFirestore();
        const docRef = doc(db, "users", user.uid);
        getDoc(docRef).then((docSnap) => {
          if (docSnap.exists()) {
            const userData = docSnap.data();
            this.user = { name: userData.name || user.email || "Lærer" };
          } else {
            this.user = { name: user.email || "Lærer" };
          }
        }).catch((error) => {
          console.error("Failed to fetch teacher name from Firestore:", error);
          this.user = { name: user.email || "Lærer" };
        });
        this.fetchClassCode();
      }
    });
  },
  methods: {
    
    async fetchClassCode() {
      const auth = getAuth();
      const teacherId = auth.currentUser?.uid;
      const db = getDatabase();

      if (teacherId) {
        const codeRef = ref(db, `teachers/${teacherId}/class_code`);
        const snapshot = await get(codeRef);

        if (snapshot.exists()) {
          this.classCode = snapshot.val(); // ✅ Set existing code
        }
      }
    },

    async generateCode() {
      if (this.classCode) {
        alert(`Du har allerede en klassekode: ${this.classCode}`);
        return; //  Prevent generating a new code if one exists
      }

      const auth = getAuth();
      const teacherId = auth.currentUser.uid;
      const db = getDatabase();
      const newCode = Math.floor(1000 + Math.random() * 9000).toString();

      await set(ref(db, `teachers/${teacherId}/class_code`), newCode);
      this.classCode = newCode;
    },
    async viewStudents() {
      await this.fetchStudents();
    },
    viewStudentProgress() {
      this.$router.push("/student-progress");
    },
    async fetchStudents() {
      const auth = getAuth();
      const teacherId = auth.currentUser?.uid;
      const db = getDatabase();

      if (teacherId) {
        const studentsRef = ref(db, `teachers/${teacherId}/students`);
        const snapshot = await get(studentsRef);

        if (snapshot.exists()) {
          this.students = Object.values(snapshot.val());
          console.log("Students fetched successfully:", this.students);
        } else {
          this.students = [];
          console.log("No students found for this teacher.");
        }
      } else {
        console.log("Error: Teacher ID not found.");
      }
    },
    giveFeedback() {
      open("https://docs.google.com/forms/d/e/1FAIpQLScBSNJ5Gdm8ba-RWPdyRqIV4fkwxi8pMMI-5H5b8EshEXXEUw/viewform", "_blank");
    },
    async logOut() {
      const auth = getAuth();
      try {
        await signOut(auth);
        this.$router.push("/login");
      } catch (error) {
        console.error("Log out error:", error.message);
        alert("Fejl ved log ud: " + error.message);
      }
    },
  },
};
</script>

<style scoped>
.dashboard-container {
  max-width: 500px;
  margin: 0 auto;
  text-align: center;
}

button {
    display: block;
    width: 100%;
    padding: 12px;
    margin: 10px 0;
    font-size: 18px;
    background-color: #42b983;
    color: white;
    border: none;
    cursor: pointer;
    border-radius: 5px;
  }
  
  button:hover {
    background-color: #2a864e;
  }
.logout-button {
  background-color: #ff5252;
}

.logout-button:hover {
  background-color: #d42e2e;
}
</style>