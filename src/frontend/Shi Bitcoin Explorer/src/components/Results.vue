<template>
  <div class="results-container">
    <h2>Search Results</h2>
    <div v-if="isLoading">Loading...</div>
    <div v-else-if="error" class="error-message">{{ error }}</div>
    <div v-else>
      <div v-if="Array.isArray(searchResults)">
        <!-- Handle array of results -->
        <div v-for="(result, index) in searchResults" :key="index" class="result-item">
          <vue-json-pretty :data="result" />
        </div>
      </div>
      <div v-else-if="searchResults">
        <!-- Handle single result -->
        <vue-json-pretty :data="searchResults" />
      </div>
      <div v-else>No results to display.</div>
    </div>
  </div>
</template>

<script>
import VueJsonPretty from 'vue-json-pretty'
import 'vue-json-pretty/lib/styles.css'

export default {
  components: {
    VueJsonPretty,
  },
  props: {
    searchResults: {
      type: [Object, Array], // Accepts both objects and arrays
      default: () => null, // Default to null
    },
    isLoading: {
      type: Boolean,
      default: false,
    },
    error: {
      type: String,
      default: '',
    },
  },
}
</script>

<style scoped>
.results-container {
  margin-top: 2rem;
  padding: 1rem;
  background-color: #f9f9f9;
  border-radius: 8px;
  border: 1px solid #ddd;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

h2 {
  margin-bottom: 1rem;
  font-size: 1.5rem;
  color: #333;
}

.result-item {
  margin-bottom: 1.5rem;
  padding: 1rem;
  background-color: #fff;
  border-radius: 8px;
  border: 1px solid #eee;
}

.error-message {
  color: red;
  margin-top: 0.5rem;
}
</style>
