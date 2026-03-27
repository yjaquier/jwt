import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'home', component: () => import('../components/HomePage.vue') },
  { path: '/register', name: 'register', component: () => import('../components/RegisterUser.vue') },
  { path: '/login', name: 'login', component: () => import('../components/LoginUser.vue') },
  { path: '/todos', name: 'todos', component: () => import('../components/TodoList.vue') }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
