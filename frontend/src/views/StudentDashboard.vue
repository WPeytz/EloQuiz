<template>
    <div class="dashboard-container">
      <h1>Elev Dashboard</h1>
      <h2 v-if="user">Velkommen, {{ user.name }}</h2>
      <h2 v-else>Velkommen!</h2>
      <p>Her kan du starte quizzen, se dine statistikker og linke med din lærer.</p>
      
      <button @click="startQuiz">Start Quiz</button>
      <button @click="viewStatistics">Statistik</button>
      <button @click="openLinkModal">Link med Lærer</button>
      <button @click="logOut" class="logout-button">Log ud</button>
  
      <!-- Modal for linking with teacher -->
      <div v-if="showModal" class="modal">
        <div class="modal-content">
          <h2>Indtast Lærerkode</h2>
          <input type="text" v-model="teacherCode" placeholder="Lærerkode">
          <button @click="linkTeacher">Forbind</button>
          <button @click="closeModal">Annuller</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { getAuth, signOut } from "firebase/auth";
  import { getFirestore, doc, updateDoc } from "firebase/firestore";
  import firebaseApp from "../firebase";
  
  export default {
    data() {
      return {
        showModal: false,
        teacherCode: "",
        user: null,
      };
    },
    mounted() {
      const authInstance = getAuth(firebaseApp);
      const db = getFirestore(firebaseApp);
      const currentUser = authInstance.currentUser;

      if (currentUser) {
        const userRef = doc(db, "users", currentUser.uid);
        import("firebase/firestore").then(({ getDoc }) => {
          getDoc(userRef).then((docSnap) => {
            if (docSnap.exists()) {
              this.user = { uid: currentUser.uid, ...docSnap.data() };
            } else {
              this.user = currentUser;
            }
          }).catch((error) => {
            console.error("Error fetching student data:", error.message);
            this.user = currentUser;
          });
        });
      }
    },
    methods: {
      async startQuiz() {
        const response = await fetch(`${process.env.VUE_APP_API_URL}/api/get_next_question?user_id=${this.user.uid}`, {
          method: "GET",
        });
        const data = await response.json();
        this.$router.push("/quiz/"+data.id);
      },
      viewStatistics() {
        this.$router.push("/statistics");
      },
      openLinkModal() {
        this.showModal = true;
      },
      closeModal() {
        this.showModal = false;
        this.teacherCode = "";
      },
      async linkTeacher() {
        if (!this.teacherCode.trim()) {
          alert("Indtast en gyldig lærerkode.");
          return;
        }
  
        const auth = getAuth(firebaseApp);
        const db = getFirestore(firebaseApp);
        const user = auth.currentUser;
  
        if (!user) {
          alert("Ingen bruger fundet.");
          return;
        }
  
        try {
          // Opdater Firestore med lærerkode
          await updateDoc(doc(db, "users", user.uid), {
            teacherCode: this.teacherCode,
          });
  
          alert("Lærerkode tilføjet succesfuldt!");
          this.closeModal();
        } catch (error) {
          console.error("Fejl ved tilknytning til lærer:", error.message);
          alert("Kunne ikke forbinde til lærer: " + error.message);
        }
      },
      logOut() {
        const auth = getAuth(firebaseApp);
        signOut(auth)
          .then(() => {
            this.$router.push("/login");
          })
          .catch((error) => {
            console.error("Log out error:", error.message);
            alert("Fejl ved log ud: " + error.message);
          });
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
  
  /* Modal Styling */
  .modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .modal-content {
    background: white;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
  }
  
  .modal-content input {
    width: 80%;
    padding: 8px;
    margin: 10px 0;
  }
  
  .modal-content button {
    margin: 5px;
  }
  </style>