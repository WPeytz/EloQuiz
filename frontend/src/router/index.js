import { createRouter, createWebHistory } from 'vue-router';
import { auth } from '../firebase'; //AuthStateChanged
import { getFirestore, doc, getDoc } from 'firebase/firestore';
import UserLogin from '../views/UserLogin.vue';
import QuizScreen from '../views/QuizScreen.vue';
import StudentProgress from '../views/StudentProgress.vue';
import UserSignUp from "../views/UserSignUp.vue";
import StudentDashboard from "../views/StudentDashboard.vue";
import TeacherDashboard from "../views/TeacherDashboard.vue";
import StatisticsPage from '@/views/StatisticsPage.vue';
import ViewQuestions from '@/views/ViewQuestions.vue';
import AdminPanel from '@/views/AdminPanel.vue';
import RedirectHandler from '../views/RedirectHandler.vue'

const routes = [
{
  path: '/',
  component: RedirectHandler
},
  { path: '/login', component: UserLogin },
  { path: '/signup', component: UserSignUp },
  { path: '/quiz/:id?', component: QuizScreen, meta: { requiresAuth: true } },
  { path: '/student-progress', component: StudentProgress, meta: { requiresAuth: true } },
  { path: '/student-dashboard', component: StudentDashboard, meta: { requiresAuth: true, role: 'student' } },
  { path: '/teacher-dashboard', component: TeacherDashboard, meta: { requiresAuth: true, role: 'teacher' } },
  { path: '/statistics', component: StatisticsPage, meta: { requiresAuth: true, role: 'student'} },
  { path: '/view-questions', component: ViewQuestions, meta: { requiresAuth: true, role: 'teacher' } },
  { path: '/admin-panel', component: AdminPanel, meta: { requiresAuth: true, role: 'admin' } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Authentication & Role-Based Navigation Guard
router.beforeEach(async (to, from, next) => {
  const resolveAuth = () =>
    new Promise((resolve) => {
      const unsubscribe = auth.onAuthStateChanged((user) => {
        unsubscribe();
        resolve(user);
      });
    });

  const user = await resolveAuth();

  if (to.meta.requiresAuth) {
    if (!user) {
      next('/login');
    } else {
      const db = getFirestore();
      const userRef = doc(db, "users", user.uid);
      const userDoc = await getDoc(userRef);

      if (userDoc.exists()) {
        const userRole = userDoc.data().role;

        if (to.meta.role && to.meta.role !== userRole) {
          // Redirect to appropriate dashboard instead of just /login
          if (userRole === 'student') next('/student-dashboard');
          else if (userRole === 'teacher') next('/teacher-dashboard');
          else if (userRole === 'admin') next('/admin-panel');
          else next('/login');
        } else {
          next();
        }
      } else {
        next('/login');
      }
    }
  } else {
    if ((to.path === '/login' || to.path === '/signup') && user) {
      const db = getFirestore();
      const userRef = doc(db, "users", user.uid);
      const userDoc = await getDoc(userRef);
      if (userDoc.exists()) {
        const role = userDoc.data().role;
        if (role === 'student') next('/student-dashboard');
        else if (role === 'teacher') next('/teacher-dashboard');
        else if (role === 'admin') next('/admin-panel');
        else next();
      } else {
        next();
      }
    } else {
      next();
    }
  }
});

export default router;