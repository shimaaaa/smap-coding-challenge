<template> 
  <div class="container">
  	<h2>Aggregation Chart</h2>
    <summary-chart></summary-chart>
  	
    <h2>Users</h2>
    <summary-table></summary-table>
  </div>
</template>

<script>
import SummaryTable from '@/components/SummaryTable.vue'
import SummaryChart from '@/components/SummaryChart.vue'

export default {
  components: {
  	'summary-table': SummaryTable,
    'summary-chart': SummaryChart
  }
}
</script>

<style>
</style>
