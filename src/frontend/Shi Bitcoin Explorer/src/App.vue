<template>
  <div id="app">
    <Header @blockchain-info="updateBlockchainInfo" />
    <SearchBar @data-fetched="showResults" />
    <Results :searchResults="searchResults" />
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
      searchResults: {},
    }
  },
  methods: {
    updateBlockchainInfo(data) {
      // Handle blockchain info update if needed
      console.log('Blockchain Info:', data)
    },
    showResults(data) {
      this.searchResults = data
    },
  },
}
</script>
