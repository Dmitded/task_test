import axios from './index'

export default {
  async login (credentials) {
    try {
      await axios.post('/login', {
        ean13: parseInt(credentials.login),
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

  async getData (date) {
    try {
      const workers = await axios.get(`/activity?day=${date}`)
      return workers.data
    } catch (error) {
      return error.response.status
    }
  }

  // async register (credentials) {2019-05-13
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
}
