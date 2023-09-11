import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    token: null,
    movies: [],
    error: null
  },
  mutations: {
    setToken (state, token) {
      state.token = token
    },
    setMovies (state, movies) {
      state.movies = movies
    },
    setError (state, error) {
      state.error = error
    }
  },
  actions: {
    async login ({ commit }, { username, password }) {
      try {
        const response = await axios.post('/api/login', {
          username,
          password
        })
        const token = response.data.token
        commit('setToken', token)
      } catch (error) {
        commit('setError', error)
      }
    },

    async fetchMovies ({ commit }) {
      try {
        const response = await axios.get('/api/movies')
        const movies = response.data
        commit('setMovies', movies)
      } catch (error) {
        commit('setError', error)
      }
    },

    async deleteMovie ({ commit, state }, movieId) {
      try {
        await axios.delete(`/api/movies/${movieId}`, {
          headers: {
            Authorization: `Bearer ${state.token}`
          }
        })
      } catch (error) {
        commit('setError', error)
      }
    },

    async createMovie ({ commit, state }, { title, genres }) {
      try {
        await axios.post(
          '/api/movies',
          { title, genres },
          {
            headers: {
              Authorization: `Bearer ${state.token}`
            }
          }
        )
      } catch (error) {
        commit('setError', error)
      }
    },

    clearError ({ commit }) {
      commit('setError', null)
    }
  },
  getters: {
  }
})
