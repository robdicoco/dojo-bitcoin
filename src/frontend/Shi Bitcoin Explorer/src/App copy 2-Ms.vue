<template>
  <div id="app">
    <BlockchainInfo />
    <SearchBar />
  </div>
</template>

<script>
import BlockchainInfo from './components/BlockchainInfo.vue'
import SearchBar from './components/SearchBar.vue'

export default {
  components: {
    BlockchainInfo,
    SearchBar,
  },
}
</script>

<style>
#app {
  text-align: center;
}
</style>
