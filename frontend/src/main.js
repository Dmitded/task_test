import Vue from 'vue'
import App from './App.vue'
import router from './router/index'
import store from './store/index'
import vuetify from './plugins/vuetify'
import VeeValidate from 'vee-validate'
import { Line } from 'vue-chartjs'

Vue.config.productionTip = false

Vue.component('line-chart', {
  extends: Line,
  mounted () {
    this.renderChart({
      labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
      datasets: [
        {
          label: 'Data One',
          backgroundColor: '#f87979aa',
          data: [40, 39, 10, 40, 39, 80, 40]
        },
        {
          label: 'Data Two',
          backgroundColor: '#aaa979aa',
          data: [60, 49, 30, 40, 39, 20, 10]
        }
      ]
    }, { responsive: true, maintainAspectRatio: false })
  }
})

Vue.use(
  VeeValidate,
  {
    aria: true,
    dictionary: {
      ru: {
        messages: {
          required: 'Это поле не должно быть пустным'
        }
      }
    }
  }
)

new Vue({
  router,
  store,
  vuetify,
  async created () {
    await this.$store.dispatch('getCurrentUser')
  },
  render: h => h(App)
}).$mount('#app')
