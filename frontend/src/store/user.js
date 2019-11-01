import userAPI from '@/api/user'

export default {

  state: {
    user: undefined,
    current: undefined
  },

  mutations: {
    setData (state, current) {
      state.current = current
    },

    setUser (state, user) {
      state.user = user
    }
  },

  actions: {
    async login ({ commit }, credentials) {
      await userAPI.login(credentials)
    },

    async getCurrentUser ({ commit }) {
      const user = await userAPI.getCurrentUser()
      if (user !== 401) {
        commit('setUser', user)
      }
    },

    async logout ({ commit }) {
      const status = await userAPI.logout()
      if (status !== 401) {
        commit('setUser', undefined)
      }
    },

    // async register ({ commit }, credentials) {
    //   await userAPI.register(credentials)
    // },

    async getData ({ commit }) {
      const users = await userAPI.getData()
      commit('setData', users)
    }
  }
}
