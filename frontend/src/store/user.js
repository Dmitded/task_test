import userAPI from '@/api/user'

export default {

  state: {
    current: undefined
  },

  mutations: {
    setData (state, current) {
      state.current = current
    }
  },

  actions: {
    async login ({ commit }, credentials) {
      await userAPI.login(credentials)
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
