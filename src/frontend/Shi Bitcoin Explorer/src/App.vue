<template>
  <div id="app">
    <Header />
    <SearchBar @data-fetched="handleDataFetched" />
    <Results :searchResults="searchResults" :isLoading="isLoading" :error="error" />
  </div>
</template>

<script>
import Header from './components/Header.vue'
import SearchBar from './components/SearchBar.vue'
import Results from './components/Results.vue'

export default {
  components: {
    Header,
    SearchBar,
    Results,
  },
  data() {
    return {
      searchResults: null, // Holds the search results
      isLoading: false, // Loading state
      error: '', // Error message
    }
  },
  methods: {
    async handleDataFetched(data) {
      this.isLoading = true
      this.error = ''

      try {
        this.searchResults = data // Update search results
      } catch (error) {
        console.error('Error handling data:', error)
        this.error = 'Failed to process data.'
      } finally {
        this.isLoading = false
      }
    },
  },
}
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}
</style>
