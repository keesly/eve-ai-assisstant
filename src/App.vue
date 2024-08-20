<template>
  <mainWindow/>
</template>

<script>
import mainWindow from './components/main.vue'

export default {
  name: 'App',
  components: {
    mainWindow
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
