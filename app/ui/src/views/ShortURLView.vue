<template>
  <div>
    <div v-for="short_url in short_urls" :key="short_url._id" class="data-item">
      <div class="data-col-1">{{ generateFullURL(short_url._id) }}</div>
      <div class="data-col-2">{{ short_url.long_url }}</div>
      <button :disabled="!isAuthenticated" @click="deleteData(short_url._id)" class="delete-button">Delete</button>
    </div>

    <div v-if="showModal" class="modal">
      <h1>Create New Short URL</h1>
      <div class="input-row">
        <input v-model="newShortURL.longURL" placeholder="https://www.imdb.com/" class="input-field" />
      </div>
      <button @click="createData" class="create-button">Create</button>
      <button @click="showModal = false" class="cancel-button">Cancel</button>
      <p v-if="!isFormValid" class="warning-text">Please fill in all fields with valid format.</p>
    </div>
    <button v-if="!showModal" :disabled="!isAuthenticated" @click="showModal = true" class="add-button">Create Short URL</button>
  </div>
</template>

<script>
export default {
  data () {
    return {
      showModal: false,
      newShortURL: {
        longURL: ''
      },
      isFormValid: true
    }
  },
  computed: {
    short_urls () {
      return this.$store.state.short_urls
    },
    isAuthenticated () {
      return this.$store.state.token
    }
  },
  methods: {
    async fetchData () {
      await this.$store.dispatch('fetcShortURLs')
    },
    async deleteData (shortURL) {
      await this.$store.dispatch('deleteShortURL', shortURL)
      await this.$store.dispatch('fetcShortURLs')
    },
    async createData () {
      if (this.newShortURL.longURL) {
        this.isFormValid = true
        const { longURL } = this.newShortURL

        await this.$store.dispatch('createShortURL', { longURL })
        await this.$store.dispatch('fetcShortURLs')

        // Reset the new input fields
        this.newShortURL.longURL = ''
        this.showModal = false
      } else {
        this.isFormValid = false
      }
    },
    generateFullURL (shortURL) {
      return `${window.location.origin}/r/${shortURL}`
    }
  },
  created () {
    this.fetchData()
  }
}
</script>

<style>
.data-item {
  background-color: #fff;
  border: 1px solid #ddd;
  padding: 20px;
  margin: 10px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.data-col-1 {
  flex: 2;
  font-size: 18px;
  font-weight: bold;
}

.data-col-2 {
  flex: 3;
  color: #777;
}

.delete-button {
  background-color: #e74c3c;
  color: #fff;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.delete-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.modal {
  background-color: #fff;
  border: 1px solid #ddd;
  padding: 20px;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1000;
  max-width: 400px;
  width: 90%;
}

.input-row {
  width: 100%;
  margin-bottom: 15px;
  display: flex;
}

.input-field {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.create-button {
  background-color: #2ecc71;
  color: #fff;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.create-button:hover {
  background-color: #27ae60;
}

.cancel-button {
  background-color: #ccc;
  color: #fff;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  margin-left: 10px;
  transition: background-color 0.3s;
}

.cancel-button:hover {
  background-color: #999;
}

.warning-text {
  color: #e74c3c;
  font-weight: bold;
  margin-top: 10px;
}

.add-button {
  background-color: #3498db;
  color: #fff;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  margin-top: 20px;
  transition: background-color 0.3s;
}

.add-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.add-button:hover {
  background-color: #2980b9;
}
</style>
