<script>
import { Line } from 'vue-chartjs'

export default {
  extends: Line,
  props: {
    chartId: {
      type: String,
      default: null
    },
    chartdata: {
      type: Object,
      default: null
    },
    options: {
      type: Object,
      default: null
    }
  },
  mounted () {
    if (this.chartdata == null) {
      return
    }
    this.renderChart(this.chartdata, this.options)
  },
  watch: {
    chartdata() {
        this.renderChart(this.chartdata, this.options)
    }
  }
}
</script>