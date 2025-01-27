<template>
  <div class="payment-status">
    <h3>Payment Status</h3>
    <p v-if="walletAddress">
      Send payment to: <strong>{{ walletAddress }}</strong>
    </p>
    <p v-if="amount">
      Amount: <strong>{{ amount }} BTC</strong>
    </p>
    <button @click="checkPaymentStatus" :disabled="isCheckingPayment">
      {{ isCheckingPayment ? 'Checking...' : 'Check Payment Status' }}
    </button>
    <p v-if="status">
      Status: <strong>{{ status }}</strong>
    </p>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
export default {
  props: {
    walletAddress: {
      type: String,
      default: '',
    },
    amount: {
      type: String,
      default: '0.001',
    },
  },
  data() {
    return {
      status: '',
      isCheckingPayment: false,
      error: '',
    }
  },
  methods: {
    async checkPaymentStatus() {
      if (!this.walletAddress) {
        this.error = 'Wallet address is missing.'
        return
      }

      this.isCheckingPayment = true
      this.error = ''

      try {
        const response = await fetch(`/api2/check-payment?walletAddress=${this.walletAddress}`)
        if (!response.ok) {
          throw new Error('Failed to check payment status.')
        }

        const data = await response.json()
        this.status = data.status
        this.$emit('payment-status-updated', data) // Emit event with payment status
      } catch (err) {
        this.error = err.message || 'An error occurred while checking payment status.'
      } finally {
        this.isCheckingPayment = false
      }
    },
  },
}
</script>

<style scoped>
.payment-status {
  margin-bottom: 2rem;
}

button {
  padding: 0.5rem 1rem;
  background-color: var(--button-bg-color);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: var(--button-hover-bg-color);
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.error {
  color: var(--error-color);
  margin-top: 1rem;
}
</style>
