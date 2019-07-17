<template>
  <line-chart
    :chart-id="chartId"
    :chartdata="chartdata"
    :options="options"/>
</template>

<script>
import LineChart from '@/components/LineChart.vue'

export default {
  components: {
    'line-chart': LineChart
  },
  props: {
    chartdata: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      chartId: 'daily-line-chart',
      options: {
        responsive: false,
        maintainAspectRatio: false
      }
    }
  }
}
</script>

<style>
</style>
