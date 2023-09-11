<template>
  <div>
    <div v-for="movie in movies" :key="movie._id" class="movie-item">
      <div class="movie-title">{{ movie.title }}</div>
      <div class="movie-genres">{{ movie.genres }}</div>
      <button :disabled="!isAuthenticated" @click="deleteMovie(movie._id)" class="delete-button">Delete</button>
    </div>

    <!-- Modal for creating a new movie -->
    <div v-if="showModal" class="modal">
      <h1>Create New Movie</h1>
      <div class="input-row">
        <input v-model="newMovie.title" placeholder="Title" class="input-field" />
      </div>
      <div class="input-row">
        <select v-model="newMovie.genres" id="genres" class="input-field">
          <option value="" disabled selected>Choose a genres</option>
          <option value="Action">Action</option>
          <option value="Adventure">Adventure</option>
          <option value="Animation">Animation</option>
          <option value="Comedy">Comedy</option>
          <option value="Crime">Crime</option>
          <option value="Drama">Drama</option>
          <option value="Horror">Horror</option>
          <option value="Romance">Romance</option>
          <option value="Sci-Fi">Sci-Fi</option>
          <option value="Thriller">Thriller</option>
        </select>
      </div>
      <button @click="createMovie" class="create-button">Create Movie</button>
      <button @click="showModal = false" class="cancel-button">Cancel</button>
      <p v-if="!isFormValid" class="warning-text">Please fill in both title and genre fields.</p>
    </div>
    <button v-if="!showModal" :disabled="!isAuthenticated" @click="showModal = true" class="add-button">Add Movie</button>
  </div>
</template>

<script>
export default {
  data () {
    return {
      showModal: false,
      newMovie: {
        title: '',
        genres: ''
      },
      isFormValid: true
    }
  },
  computed: {
    movies () {
      return this.$store.state.movies
    },
    isAuthenticated () {
      return this.$store.state.token
    }
  },
  methods: {
    async fetchData () {
      await this.$store.dispatch('fetchMovies')
    },
    async deleteMovie (movieId) {
      await this.$store.dispatch('deleteMovie', movieId)
      await this.$store.dispatch('fetchMovies')
    },
    async createMovie () {
      if (this.newMovie.title && this.newMovie.genres) {
        this.isFormValid = true
        const { title, genres } = this.newMovie

        await this.$store.dispatch('createMovie', { title, genres })
        await this.$store.dispatch('fetchMovies')

        // Reset the new movie input fields
        this.newMovie.title = ''
        this.newMovie.genres = ''
        this.showModal = false
      } else {
        this.isFormValid = false
      }
    }
  },
  created () {
    this.fetchData()
  }
}
</script>

<style>
.movie-item {
  background-color: #fff;
  border: 1px solid #ddd;
  padding: 20px;
  margin: 10px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.movie-title {
  flex: 2;
  font-size: 18px;
  font-weight: bold;
}

.movie-genres {
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
