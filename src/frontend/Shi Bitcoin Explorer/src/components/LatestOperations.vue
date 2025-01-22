<template>
  <div class="latest-operations">
    <h2>Latest Operations</h2>

    <!-- Refresh Button -->
    <button @click="refreshData" class="refresh-button">Refresh Data</button>

    <!-- Display Latest Block -->
    <div v-if="operations.latestBlock" class="latest-block">
      <h3>Latest Block</h3>
      <div class="block-info">
        <p><strong>Height:</strong> {{ operations.latestBlock.height }}</p>
        <p><strong>Hash:</strong> {{ operations.latestBlock.hash }}</p>
        <p><strong>Time:</strong> {{ formatTimestamp(operations.latestBlock.time) }}</p>
        <p><strong>Transactions:</strong> {{ operations.latestBlock.nTx }}</p>
      </div>
    </div>

    <!-- Display Latest Blocks -->
    <div v-if="operations.latestBlocks && operations.latestBlocks.length > 0" class="latest-blocks">
      <h3>Latest Blocks</h3>
      <ul>
        <li v-for="block in operations.latestBlocks" :key="block.hash" class="block-item">
          <p><strong>Height:</strong> {{ block.height }}</p>
          <p><strong>Hash:</strong> {{ block.hash }}</p>
          <p><strong>Time:</strong> {{ formatTimestamp(block.time) }}</p>
          <p><strong>Transactions:</strong> {{ block.num_transactions }}</p>
        </li>
      </ul>
    </div>

    <!-- Display Latest Transactions -->
    <div
      v-if="operations.latestTransactions && operations.latestTransactions.length > 0"
      class="latest-transactions"
    >
      <h3>Latest Transactions</h3>
      <ul>
        <li v-for="tx in operations.latestTransactions" :key="tx.txid" class="transaction-item">
          <p><strong>TXID:</strong> {{ tx.txid }}</p>
          <p><strong>Time:</strong> {{ formatTimestamp(tx.time) }}</p>
          <p><strong>Category:</strong> {{ tx.category }}</p>
          <p><strong>Value:</strong> {{ tx.details.vout[0].value }} BTC</p>
        </li>
      </ul>
    </div>

    <!-- Display Message if No Data -->
    <div
      v-if="
        !operations.latestBlock &&
        (!operations.latestBlocks || operations.latestBlocks.length === 0) &&
        (!operations.latestTransactions || operations.latestTransactions.length === 0)
      "
    >
      No latest activity found.
    </div>
  </div>
</template>

<script>
export default {
  props: {
    operations: {
      type: Object,
      required: true,
      default: () => ({
        latestBlock: null,
        latestBlocks: [],
        latestTransactions: [],
      }),
    },
  },
  methods: {
    // Format timestamp to a human-readable format
    formatTimestamp(timestamp) {
      return new Date(timestamp * 1000).toLocaleString()
    },

    // Emit an event to refresh the data
    refreshData() {
      this.$emit('refresh-data')
    },
  },
}
</script>

<style scoped>
.latest-operations {
  padding: 1rem;
  background-color: #f5f5f5;
  border-radius: 8px;
  border: 1px solid #ddd;
}

h2 {
  margin-bottom: 1rem;
  font-size: 1.5rem;
  color: #333;
}

.refresh-button {
  padding: 0.5rem 1rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 1rem;
}

.refresh-button:hover {
  background-color: #0056b3;
}

.latest-block,
.latest-blocks,
.latest-transactions {
  margin-bottom: 1.5rem;
}

h3 {
  margin-bottom: 0.5rem;
  font-size: 1.2rem;
  color: #333;
}

.block-info,
.block-item,
.transaction-item {
  padding: 1rem;
  background-color: #fff;
  border-radius: 8px;
  border: 1px solid #eee;
  margin-bottom: 1rem;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin-bottom: 1rem;
}

p {
  margin: 0.5rem 0;
}
</style>
