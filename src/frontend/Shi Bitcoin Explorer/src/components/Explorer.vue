<template>
  <div>
    <div class="blockchain-info">
      <h2>Blockchain Info</h2>
      <pre>{{ blockchainInfo }}</pre>
    </div>

    <div class="search-bar">
      <input type="text" v-model="searchQuery" placeholder="Enter address, height, hash, or txid" />
      <button @click="search">Search</button>
    </div>

    <div class="results">
      <h3>Balance:</h3>
      <pre>{{ balance }}</pre>

      <h3>Block Hash:</h3>
      <pre>{{ blockHash }}</pre>

      <h3>Block:</h3>
      <pre>{{ block }}</pre>

      <h3>Transaction:</h3>
      <pre>{{ transaction }}</pre>

      <h3>Raw Transaction:</h3>
      <pre>{{ rawTransaction }}</pre>
    </div>
  </div>
</template>

<script>
import { useBlockchainStore } from '../stores/blockchain'

export default {
  setup() {
    const blockchainStore = useBlockchainStore()

    const search = () => {
      const query = blockchainStore.searchQuery
      if (query.startsWith('bc1') || query.startsWith('1')) {
        // Assuming Bitcoin addresses start with bc1 or 1
        blockchainStore.fetchBalance(query)
      } else if (!isNaN(query)) {
        // Assuming height is a number
        blockchainStore.fetchBlockHash(query)
      } else {
        // Attempt to fetch block, transaction, or raw transaction
        blockchainStore.fetchBlock(query)
        blockchainStore.fetchTransaction(query)
        blockchainStore.fetchRawTransaction(query)
      }
    }

    return {
      blockchainStore,
      search,
    }
  },
}
</script>

<style>
/* Add some basic styling */
.blockchain-info {
  float: right;
  margin-right: 20px;
}
.search-bar {
  margin-bottom: 20px;
}
</style>
