import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import StudentDashboard from '../views/StudentDashboard.vue'
import CompanyDashboard from '../views/CompanyDashboard.vue'
import LandingPage from '../views/LandingPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      component: LoginView
    },
    {
      path: '/admin/dashboard',
      component: AdminDashboard
    },
    {
      path: '/student/dashboard',
      component: StudentDashboard
    },
    {
      path: '/company/dashboard',
      component: CompanyDashboard
    },
    {
      path: '/',
      component: LandingPage
    }
  ],
})

export default router
