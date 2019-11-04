import userAPI from '@/api/user'

export default {

  state: {
    current: undefined,
    workers: undefined
  },

  mutations: {
    setUser (state, user) {
      state.current = user
    },
    setWorkers (state, workers) {
      state.workers = workers
    }
  },

  actions: {
    async login (credentials) {
      await userAPI.login(credentials)
    },

    async getCurrentUser ({ commit }) {
      const users = await userAPI.getCurrentUser()
      if (users !== 401 && 502) {
        commit('setUser', users)
      }
    },

    async logout ({ commit }) {
      const status = await userAPI.logout()
      if (status !== 401) {
        commit('setUser', undefined)
      }
    },

    async getData ({ commit }) {
      const workers = await userAPI.getData()
      if (workers !== 401 && 502) {
        commit('setWorkers', workers)
      }
    }

    // async register ({ commit }, credentials) {
    //   await userAPI.register(credentials)
    // },
  }
}
