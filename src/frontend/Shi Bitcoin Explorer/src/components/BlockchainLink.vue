<template>
  <div class="blockchain-link">
    <h3>Blockchain Transaction</h3>
    <p v-if="transactionId">
      Transaction ID: <code>{{ transactionId }}</code>
    </p>
    <p v-if="blockchainUrl">
      <a :href="blockchainUrl" target="_blank">View on Blockchain</a>
    </p>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
export default {
  props: {
    transactionId: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      blockchainUrl: '',
      error: '',
    }
  },
  methods: {
    async fetchBlockchainUrl() {
      try {
        const response = await fetch('/reg/mining-confirmation', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            tx_id: this.transactionId,
          }),
        })

        if (!response.ok) {
          throw new Error('Failed to fetch blockchain link.')
        }

        const data = await response.json()
        this.blockchainUrl = data.url
      } catch (err) {
        this.error = err.message || 'An error occurred while fetching the blockchain link.'
      }
    },
  },
  watch: {
    transactionId: {
      immediate: true,
      handler(newId) {
        if (newId) {
          this.fetchBlockchainUrl()
        }
      },
    },
  },
}
</script>

<style scoped>
.blockchain-link {
  margin-bottom: 2rem;
}

a {
  color: var(--button-bg-color);
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

.error {
  color: var(--error-color);
  margin-top: 1rem;
}
</style>
