<template>
    <div class="student-link-container">
      <h1>Tilslut til en lærer</h1>
      <input v-model="classCode" placeholder="Indtast lærerkode" />
      <button @click="linkToTeacher">Tilslut</button>
    </div>
  </template>
  
  <script>
  import { getAuth } from "firebase/auth";
  import { getDatabase, ref, get, set } from "firebase/database";
  
  export default {
    data() {
      return {
        classCode: "",
      };
    },
    methods: {
      async linkToTeacher() {
        const auth = getAuth();
        const studentId = auth.currentUser?.uid;
        if (!studentId) {
          alert("Du skal være logget ind for at tilslutte en lærer!");
          return;
        }

        const db = getDatabase();
        const teachersRef = ref(db, "teachers");
        const snapshot = await get(teachersRef);

        if (!snapshot.exists()) {
          alert("Ingen lærere fundet.");
          return;
        }

        let teacherId = null;
        snapshot.forEach((teacher) => {
          if (teacher.val().class_code === this.classCode) {
            teacherId = teacher.key;
          }
        });

        if (!teacherId) {
          alert("Ugyldig kode, prøv igen.");
          return;
        }

        try {
          console.log("Lærer fundet! ID:", teacherId);
          console.log("Forsøger at oprette students node:", `students/${studentId}`);

          // ✅ Create `students` node and link teacher
          await set(ref(db, `students/${studentId}`), {
            teacher_id: teacherId,
            joined_at: new Date().toISOString()
          });

          console.log("Student entry added successfully");

          // ✅ Add student under the teacher's students list
          console.log("Forsøger at tilføje studenten under teacher:", `teachers/${teacherId}/students/${studentId}`);

          await set(ref(db, `teachers/${teacherId}/students/${studentId}`), {
            joined_at: new Date().toISOString()
          });

          console.log("Student added under teacher");

          alert("Du er nu tilsluttet til din lærer!");
          this.$router.push("/student/dashboard");
        } catch (error) {
          console.error("Fejl ved tilslutning:", error);
          alert("Der opstod en fejl. Prøv igen.");
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .student-link-container {
    max-width: 400px;
    margin: auto;
    text-align: center;
  }
  input {
    width: 100%;
    padding: 10px;
    margin-bottom: 10px;
  }
  button {
    width: 100%;
    padding: 10px;
    background-color: #4caf50;
    color: white;
    border: none;
    cursor: pointer;
  }
  </style>