<template>
  <div class="row">
    <b-tabs content-class="mt-3">
      <b-tab title="Daily" active>
        <summary-daily-chart></summary-daily-chart>
      </b-tab>
      <b-tab title="Monthly">
        <summary-monthly-chart></summary-monthly-chart>        
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>

import SummaryDailyChart from '@/components/SummaryDailyChart.vue'
import SummaryMonthlyChart from '@/components/SummaryMonthlyChart.vue'

export default {
  components: {
    'summary-daily-chart': SummaryDailyChart,
    'summary-monthly-chart': SummaryMonthlyChart,
  }
}
</script>

<style>
</style>
