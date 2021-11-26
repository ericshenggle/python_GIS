<template>
<div>
  <div>
    <iframe :src="this.url"></iframe>
  </div>
</div>
</template>

<script>
export default {
  name: 'AqiDate',
  data () {
    return {
      url: './test.html'
    }
  },
  mounted () {
  },

  methods: {
  }
}
</script>

<style>
</style>
