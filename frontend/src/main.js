import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import { onAuthStateChanged } from 'firebase/auth'
import { auth } from './firebase'

// Set up global API URL
const API_URL = "https://adaptive-learning-489216095849.europe-west1.run.app"; // Cloud Run backend URL
window.API_URL = API_URL; // Make it accessible globally

onAuthStateChanged(auth, (user) => {
    createApp(App).use(store).use(router).mount('#app')

    if (user) {
        store.dispatch('setUser', user);
    }
});

