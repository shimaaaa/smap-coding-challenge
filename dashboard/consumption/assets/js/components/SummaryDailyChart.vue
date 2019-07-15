<template>
  <line-chart
    v-if="loaded"
    :chart-id="chartId"
    :chartdata="chartdata"
    :options="options"/>
</template>

<script>
import LineChart from '@/components/LineChart.vue'
import Axios from 'axios'

export default {
  name: 'SummaryDailyChart',
  components: {
    'line-chart': LineChart
  },
  data() {
    return {
      chartId: 'daily-line-chart',
      loaded: false,
      chartdata: null,
      options: {
        responsive: false,
        maintainAspectRatio: false
      }
    }
  },
  mounted () {
    const self = this
    Axios.get('/api/charts/consumptions/daily')
    .then((res) => {
      self.loaded = true
      self.chartdata = {
        labels: res.data.days,
        datasets: [
          {
            label: 'TotalValues',
            backgroundColor: '#f87979',
            data: res.data.total_values
          }
        ]
      }
    })
  }
}
</script>

<style>
</style>
