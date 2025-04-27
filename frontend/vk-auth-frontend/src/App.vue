<template>
  <div class="app-container">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  min-height: 100vh;
  background-color: #1a202c; /* bg-gray-900 */
  color: #e2e8f0; /* text-gray-200 */
  font-family: 'Montserrat', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.app-container {
  min-height: 100vh;
}

* {
  box-sizing: border-box;
}
</style>
