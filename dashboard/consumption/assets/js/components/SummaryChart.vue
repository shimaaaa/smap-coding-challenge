<template>
  <div class="row">
    <b-tabs content-class="mt-3">
      <b-tab title="Total" active>
        <summary-line-chart
          :chartdata="totalChartData">
        </summary-line-chart>
      </b-tab>
      <b-tab title="Average">
        <summary-line-chart
          :chartdata="averageChartData">
        </summary-line-chart>
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>

import Axios from 'axios'
import SummaryLineChart from '@/components/SummaryLineChart.vue'

export default {
  components: {
    'summary-line-chart': SummaryLineChart
  },
  data() {
    return {
      totalChartData: null,
      averageChartData: null
    }
  },
  created () {
    const self = this
    Axios.get('/api/consumption-daily-summary/')
    .then((res) => {
      
      const lebels = res.data.map(data => data.target_date)
      const totalValues = res.data.map(data => data.total_value)
      const averageValues = res.data.map(data => data.average_value)
      self.totalChartData = {
        labels: lebels,
        datasets: [
          {
            label: 'TotalValues',
            backgroundColor: '#f87979',
            data: totalValues
          }
        ]
      }
      self.averageChartData = {
        labels: lebels,
        datasets: [
          {
            label: 'AverageValues',
            backgroundColor: '#7979f8',
            data: averageValues
          }
        ]
      }
    })
  }
}
</script>
