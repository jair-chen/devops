<template>
  <div class="login-modal">
    <div class="input-row">
      <input v-model="username" placeholder="Username" class="input-field" />
    </div>
    <div class="input-row">
      <input v-model="password" type="password" placeholder="Password" class="input-field" />
    </div>
    <button @click="login" class="login-button">Login</button>
  </div>
</template>

<script>
export default {
  data () {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    async login () {
      await this.$store.dispatch('login', {
        username: this.username,
        password: this.password
      })

      this.$router.push({ name: 'shorturl' })
    }
  }
}
</script>

<style>
.login-modal {
  max-width: 300px;
  margin: 20px auto;
  padding: 20px;
  background-color: #fff;
  border: 1px solid #ddd;
}

.input-row {
  width: 100%;
  margin-bottom: 15px;
  display: flex;
}

.input-field {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.login-button {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  width: 100%;
}

.login-button:hover {
  background-color: #0056b3;
}
</style>
