<template>
  <div id="app">
    <!-- Site Title (Top Left Corner) -->
    <div class="site-title">Shi(し) Satoshi Explorer</div>

    <!-- Search Bar (Top Center) -->
    <div class="search-container">
      <SearchBar @data-fetched="handleDataFetched" />
    </div>

    <!-- Results (Below Search Bar) -->
    <div class="results-wrapper">
      <Results :searchResults="searchResults" :isLoading="isLoading" :error="error" />
    </div>

    <!-- Blockchain Info (Below Results) -->

    <div class="blockchain-wrapper">
      <BlockChainData />
    </div>

    <!-- GitHub Links (Bottom) -->
    <div class="github-links">
      <a href="https://github.com/robdicoco" target="_blank">robdicoco</a>
      <a href="https://github.com/Edugera" target="_blank">Edugera</a>
      <a href="https://github.com/alfatektecnologia" target="_blank">alfatektecnologia</a>
    </div>

    <!-- Source Code Reference (Bottom) -->
    <div class="source-code">
      Source Code:
      <a href="https://github.com/robdicoco/dojo-bitcoin/" target="_blank">dojo-bitcoin</a> |
      License: MIT
    </div>
  </div>
</template>

<script>
import BlockChainData from './components/BlockChainData.vue'
import SearchBar from './components/SearchBar.vue'
import Results from './components/Results.vue'

export default {
  components: {
    BlockChainData,
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
/* Global Styles */
#app {
  font-family: Arial, sans-serif;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  position: relative;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* Site Title (Top Left Corner) */
.site-title {
  position: center;
  top: 10px;
  /* left: 20px; */
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
}

/* Search Bar Container (Top Center) */
.search-container {
  margin-top: 50px; /* Adjust based on site title height */
  width: 100%;
  display: flex;
  justify-content: center;
}

/* Results Wrapper (Below Search Bar) */
.results-wrapper {
  width: 100%;
  margin-top: 20px; /* Space between search bar and results */
}

/* BlockChainData Wrapper (Below Results) */
.blockchain-wrapper {
  width: 100%;
  margin-top: 20px; /* Space between search bar and results */
}

/* GitHub Links (Bottom) */
.github-links {
  position: center;
  margin-top: 20px;
  /* bottom: 60px; Adjust based on source code reference height */
  /* left: 50%; */
  /* transform: translateX(-50%); */
  display: flex;
  gap: 20px;
}

.github-links a {
  color: #007bff;
  text-decoration: none;
  font-weight: bold;
  transition:
    transform 0.3s ease,
    color 0.3s ease;
}

.github-links a:hover {
  color: #0056b3;
  transform: scale(1.1); /* Enlarge on hover */
}

/* Source Code Reference (Bottom) */
.source-code {
  margin-top: 20px;
  position: center;
  /* position: absolute; */
  /* bottom: 20px; */
  /* left: 50%; */
  /* width: 100%; */
  /* transform: translateX(-50%); */
  font-size: 0.9rem;
  color: #666;
}

.source-code a {
  color: #007bff;
  text-decoration: none;
}

.source-code a:hover {
  text-decoration: underline;
}
</style>
