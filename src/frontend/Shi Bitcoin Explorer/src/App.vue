<template>
  <div id="app" :class="theme">
    <!-- Theme Toggle Switch -->
    <div class="theme-toggle">
      <label>
        <input type="checkbox" v-model="isDarkMode" @change="toggleTheme" />
        <span class="slider"></span>
      </label>
    </div>

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
      isDarkMode: false, // Dark mode state
      theme: 'light', // Current theme
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
    toggleTheme() {
      this.theme = this.isDarkMode ? 'dark' : 'light'
      document.documentElement.setAttribute('data-theme', this.theme)
    },
  },
  mounted() {
    // Initialize theme based on user preference or system settings
    const prefersDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches
    this.isDarkMode = prefersDarkMode
    this.toggleTheme()
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
  transition:
    background-color 0.3s,
    color 0.3s;
}

/* Light Theme (Default) */
#app.light {
  --background-color: #f9f9f9;
  --text-color: #333;
  --border-color: #ddd;
  --button-bg-color: #007bff;
  --button-hover-bg-color: #0056b3;
  --error-color: red;
}

/* Dark Theme */
#app.dark {
  --background-color: #1a1a1a;
  --text-color: #f9f9f9;
  --border-color: #444;
  --button-bg-color: #0056b3;
  --button-hover-bg-color: #007bff;
  --error-color: #ff4d4d;
}

/* Apply CSS Variables */
#app {
  background-color: var(--background-color);
  color: var(--text-color);
}

/* Theme Toggle Switch */
.theme-toggle {
  position: absolute;
  top: 20px;
  right: 20px;
}

.theme-toggle label {
  display: flex;
  align-items: center;
  gap: 10px;
}

.theme-toggle input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
  background-color: #ccc;
  border-radius: 34px;
  transition: background-color 0.3s;
}

.slider::before {
  content: '';
  position: absolute;
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  border-radius: 50%;
  transition: transform 0.3s;
}

input:checked + .slider {
  background-color: var(--button-bg-color);
}

input:checked + .slider::before {
  transform: translateX(26px);
}

/* Site Title (Top Left Corner) */
.site-title {
  position: center;
  top: 10px;
  /* left: 20px; */
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--text-color);
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
  color: var(--button-bg-color);
  text-decoration: none;
  font-weight: bold;
  transition:
    transform 0.3s ease,
    color 0.3s ease;
}

.github-links a:hover {
  color: var(--button-hover-bg-color);
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
  color: var(--text-color);
}

.source-code a {
  color: var(--button-bg-color);
  text-decoration: none;
}

.source-code a:hover {
  text-decoration: underline;
}
</style>
