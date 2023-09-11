import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../views/LoginView.vue'
import MovieList from '../views/MoviesView.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    name: 'login',
    path: '/login',
    component: Login
  },
  {
    name: 'movies',
    path: '/movies',
    component: MovieList
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
