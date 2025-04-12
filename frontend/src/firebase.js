import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore"; 
import { 
  getAuth, 
  setPersistence, 
  browserSessionPersistence, 
  signInWithEmailAndPassword 
} from "firebase/auth"; 

const firebaseConfig = {
  apiKey: "AIzaSyAovTx7PHPOcl0TFsYblR3PvyKA1VCss-Y",
  authDomain: "adaptivelearning-ff09f.firebaseapp.com",
  databaseURL: "https://adaptivelearning-ff09f-default-rtdb.europe-west1.firebasedatabase.app", // http://192.168.0.93:8080
  projectId: "adaptivelearning-ff09f",
  storageBucket: "adaptivelearning-ff09f.firebasestorage.app",
  messagingSenderId: "304947427733",
  appId: "1:304947427733:web:1d52843cf21a9646245e9c",
  measurementId: "G-L1LCPLNPRK",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const db = getFirestore(app);
export const auth = getAuth(app);

// Replace these with actual values or implement a proper sign-in flow
const email = "your-email@example.com";
const password = "your-password";

setPersistence(auth, browserSessionPersistence)
  .then(() => {
    return signInWithEmailAndPassword(auth, email, password);
  })
  .catch((error) => {
    console.error("Error setting Firebase Auth persistence:", error);
  });