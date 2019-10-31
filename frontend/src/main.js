import Vue from 'vue'
import App from './App.vue'
import router from './router/index'
import store from './store/index'
import vuetify from './plugins/vuetify'

Vue.config.productionTip = false

new Vue({
  router,
  store,
  vuetify,
  async created () {
    await this.$store.dispatch('getCurrentUser')
  },
  render: h => h(App)
}).$mount('#app')
