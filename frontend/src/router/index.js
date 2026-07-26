import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

const routes = [
  { path: '/login', name: 'Login', component: () => import('../views/Login.vue') },
  { path: '/register', name: 'Register', component: () => import('../views/Register.vue') },
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/models',
    name: 'Models',
    component: () => import('../views/Models.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/agents',
    name: 'Agents',
    component: () => import('../views/Agents.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/agent/:id',
    name: 'AgentDetail',
    component: () => import('../views/AgentDetail.vue'),
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/chat',
    name: 'Chat',
    component: () => import('../views/Chat.vue'),
    props: route => ({ agentId: route.query.agentId }),
    meta: { requiresAuth: true }
  },
  {
    path: '/history',
    name: 'History',
    component: () => import('../views/History.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/video',
    name: 'Video',
    component: () => import('../views/Home.vue'), // 或独立的VideoUpload
    meta: { requiresAuth: true }
  },
  {
    path: '/task/:id',
    name: 'TaskDetail',
    component: () => import('../views/TaskDetail.vue'),
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/report/:id',
    name: 'Report',
    component: () => import('../views/Report.vue'),
    props: true,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const token = store.state.token
  if (requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router