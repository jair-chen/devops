<template>
  <div id="app">
    <div class="header">
      <div class="title">DevOps in a Nutshell</div>
      <router-link to="/login" class="nav-link">Login</router-link>
      <router-link to="/movies" class="nav-link">Movies</router-link>
    </div>
    <div v-if="errorMessage" class="global-error">
      <div class="error-content">{{ errorMessage }}</div>
      <button @click="dismissError" class="dismiss-button">Dismiss</button>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  computed: {
    errorMessage () {
      return this.$store.state.error ? this.$store.state.error.message : null
    }
  },
  methods: {
    dismissError () {
      this.$store.dispatch('clearError')
    }
  }
}
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  background-color: #f0f0f0;
  padding: 20px;
}

.header {
  background-color: #333;
  padding: 10px;
  display: flex;
  text-align: left;
}

.title {
  color: #aaa;
  flex: 1;
  text-align: left;
}

.nav-link {
  color: #fff;
  text-decoration: none;
  width: 80px;
}

.global-error {
  background-color: #e74c3c;
  color: #fff;
  padding: 10px;
  display: flex;
  text-align: center;
  font-weight: bold;
}

.error-content {
  flex: 1;
}

.dismiss-button {
  background-color: transparent;
  border: none;
  color: #fff;
  cursor: pointer;
  margin-left: 10px;
  font-size: 16px;
}

.dismiss-button:hover {
  text-decoration: underline;
}

</style>
