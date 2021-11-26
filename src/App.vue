<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import Detail from './components/Detail.vue'
window.addEventListener('beforeunload', e => {
  window.scroll(0, 0)
})
export default {
  components: {
    HelloWorld,
    Detail
  }
}
</script>

<style>
</style>
