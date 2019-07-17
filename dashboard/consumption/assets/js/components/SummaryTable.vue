<template>
    <div>
      <summary-table-filter
        :filter="filter"
        @input="changeFilter"
        @search="search" />
      <summary-table-data :users="users" />
    </div>
</template>

<script>
import Axios from 'axios'
import SummaryTableData from '@/components/SummaryTableData.vue'
import SummaryTableFilter from '@/components/SummaryTableFilter.vue'

export default {
  components: {
    'summary-table-data': SummaryTableData,
    'summary-table-filter': SummaryTableFilter
  },
  data() {
    return {
      users: [],
      filter: null
    }
  },
  created () {
    this.fetchData()
 	},
  computed: {
    rows() {
      return this.users.length
    }
  },
  methods: {
    changeFilter(newFilter) {
      this.filter = newFilter
    },
    search() {
      this.fetchData()
    },
    fetchData() {
      const self = this

      let params = {}
      if (this.filter != null) {
        params.search = this.filter
      }

      Axios.get('/api/users/', 
        {
          params: params
        }
      ).then((res) => {
        self.users = res.data
      })
    }
  }
}
</script>

<style>
</style>
