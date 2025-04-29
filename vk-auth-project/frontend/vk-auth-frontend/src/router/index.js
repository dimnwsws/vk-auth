import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Profile from '../views/Profile.vue'
import Dashboard from '../views/Dashboard.vue'
import WaitingApproval from '../views/WaitingApproval.vue'
import AuthCallback from '../views/AuthCallback.vue'
import AuthError from '../views/AuthError.vue'
import NotFound from '../views/NotFound.vue'
import AdminPanel from '../views/AdminPanel.vue'
import GoogleSheetsIntegration from '../views/GoogleSheetsIntegration.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/admin',
    name: 'admin',
    component: AdminPanel,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/profile',
    name: 'profile',
    component: Profile,
    meta: { requiresAuth: true }
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/waiting-approval',
    name: 'waiting-approval',
    component: WaitingApproval,
    meta: { requiresAuth: true }
  },
  {
    path: '/auth-callback',
    name: 'auth-callback',
    component: AuthCallback
  },
  {
    path: '/auth-error',
    name: 'auth-error',
    component: AuthError
  },
  {
    path: '/google-sheets',
    name: 'google-sheets',
    component: GoogleSheetsIntegration,
    meta: { requiresAuth: true }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFound
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// Защита маршрутов, требующих авторизации
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('access_token') !== null

  if (to.matched && to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router
