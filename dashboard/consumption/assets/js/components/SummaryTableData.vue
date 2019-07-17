<template>
  <div class="row">
    <b-table
      id="user-list"
      :fields="fields"
      :items="users"
      :per-page="perPage"
      :current-page="currentPage"
      small
      striped
    ></b-table>
    <b-pagination
      v-model="currentPage"
      :total-rows="rows"
      :per-page="perPage"
      aria-controls="user-list"
    ></b-pagination>
  </div>
</template>

<script>

export default {
  props: {
    users: {
      type: Array,
      default: null
    }
  },
  data() {
    return {
      fields: [
        'id',
        'area',
        'tariff'
      ],
      perPage: 20,
      currentPage: 1
    }
  },
  computed: {
    rows() {
      return this.users.length
    }
  }
}
</script>

<style>
</style>
