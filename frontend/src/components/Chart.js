import Vue from 'vue'
import { Line, mixins } from 'vue-chartjs'

Vue.component('line-chart', {
  extends: Line,
  mixins: [mixins.reactiveProp],
  props: ['options'],
  mounted () {
    this.renderChart(this.chartData, this.options)
  },

  created () {
  },

  methods: {

  }
})
