import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '../views/LandingPage.vue'
import LoginView from '../views/LoginView.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import StudentDashboard from '../views/StudentDashboard.vue'
import CompanyDashboard from '../views/CompanyDashboard.vue'
import RegisterPage from '../views/RegisterPage.vue'
import StudentRegister from '../views/StudentRegister.vue'
import CompanyRegister from '../views/CompanyRegister.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: LandingPage
    },
    {
      path: '/login',
      component: LoginView
    },
    {
      path: '/register',
      component: RegisterPage
    },
    {
      path: '/register/student',
      component: StudentRegister
    },
    {
      path: '/register/company',
      component: CompanyRegister
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
  ],
})

export default router
