<template>
    <div>Redirecting...</div>
  </template>
  
  <script setup>
  import { onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import { auth } from '../firebase'
  import { getFirestore, doc, getDoc } from 'firebase/firestore'
  
  const router = useRouter()
  
  onMounted(async () => {
    const user = auth.currentUser
  
    if (user) {
      const db = getFirestore()
      const userRef = doc(db, "users", user.uid)
      const userSnap = await getDoc(userRef)
  
      if (userSnap.exists()) {
        const role = userSnap.data().role
        if (role === 'student') return router.push('/student-dashboard')
        if (role === 'teacher') return router.push('/teacher-dashboard')
        if (role === 'admin') return router.push('/admin-panel')
      }
    }
  
    router.push('/login')
  })
  </script>