import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    token: null,
    short_urls: [],
    error: null
  },
  mutations: {
    setToken (state, token) {
      state.token = token
    },
    setShortURLs (state, shortURLs) {
      state.short_urls = shortURLs
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

    async fetcShortURLs ({ commit, state }) {
      try {
        const response = await axios.get('/api/shorturl', {
          headers: {
            Authorization: `Bearer ${state.token}`
          }
        })
        const shortURLs = response.data
        commit('setShortURLs', shortURLs)
      } catch (error) {
        commit('setError', error)
      }
    },

    async deleteShortURL ({ commit, state }, shortURL) {
      try {
        await axios.delete(`/api/shorturl/${shortURL}`, {
          headers: {
            Authorization: `Bearer ${state.token}`
          }
        })
      } catch (error) {
        commit('setError', error)
      }
    },

    async createShortURL ({ commit, state }, { longURL }) {
      try {
        await axios.post(
          '/api/shorturl',
          { long_url: longURL },
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
