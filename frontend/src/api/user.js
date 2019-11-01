import axios from './index'

export default {
  async login (credentials) {
    try {
      await axios.post('/login', {
        login: credentials.login,
        password: credentials.password
      })
    } catch (error) {
      return error.response.status
    }
  },

  async logout () {
    try {
      await axios.get('/logout')
    } catch (error) {
      return error.response.status
    }
  },

  async getCurrentUser () {
    try {
      const user = await axios.get('/users/current')
      return user.data
    } catch (error) {
      return error.response.status
    }
  },

  // async register (credentials) {
  //   try {
  //     await axios.post('/users', {
  //       login: credentials.login,
  //       email: credentials.email,
  //       password: credentials.password
  //     })
  //   } catch (error) {
  //     return error.response.status
  //   }
  // },

  async getData () {
    try {
      const current = await axios.get('/current')
      console.log(current.data)
      return current.data
    } catch (error) {
      return error.response.status
    }
  }
}
