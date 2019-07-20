<template>
  <div class="row">

    <b-form-group
      label-cols-lg="3"
      label="Filter"
      label-size="lg"
      label-class="font-weight-bold pt-0"
      class="mb-0"
    >
      <b-form-group>
        <b-form-input id="search" :value="filter" @change="onChangeFilter"></b-form-input>
      </b-form-group>
      <b-form-group>
        <b-button @click="onClickSearch">search</b-button>
      </b-form-group>
    </b-form-group>

  </div>
</template>

<script>

export default {
  props: {
    filter: {
      type: String,
      default: null
    }
  },
  methods: {
    onChangeFilter(event) {
      this.$emit('input', event)
    },
    onClickSearch(event) {
      this.$emit('search')
    }
  }
}
</script>
