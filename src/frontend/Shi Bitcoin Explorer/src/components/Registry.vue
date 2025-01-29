<template>
  <div class="registry-container">
    <h2>Copyright Registration</h2>

    <!-- Document Upload Section -->
    <DocumentUpload @document-uploaded="handleDocumentUploaded" />

    <!-- Payment Section -->
    <PaymentStatus
      v-if="documentHash"
      :document-hash="documentHash"
      :wallet-address="walletAddress"
      @payment-status-updated="handlePaymentStatusUpdated"
    />

    <!-- Blockchain Link Section -->
    <BlockchainLink v-if="transactionId" :transaction-id="transactionId" />
  </div>
</template>

<script>
import DocumentUpload from './DocumentUpload.vue'
import PaymentStatus from './PaymentStatus.vue'
import BlockchainLink from './BlockchainLink.vue'

export default {
  components: {
    DocumentUpload,
    PaymentStatus,
    BlockchainLink,
  },
  data() {
    return {
      documentHash: '',
      walletAddress: '',
      transactionId: '',
    }
  },
  methods: {
    handleDocumentUploaded(data) {
      this.documentHash = data.document_hash
      this.walletAddress = data.wallet_address
    },
    async handlePaymentStatusUpdated(data) {
      if (data.status === 'Payment Confirmed') {
        // Send transaction to the blockchain
        const response = await fetch('/reg/send-transaction', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            document_hash: this.documentHash,
          }),
        })

        if (!response.ok) {
          throw new Error('Failed to send transaction.')
        }

        const txData = await response.json()
        this.transactionId = txData.tx_id
      }
    },
  },
}
</script>

<style scoped>
.registry-container {
  padding: 1rem;
  background-color: var(--background-color);
  border-radius: 8px;
  border: 1px solid var(--border-color);
}
</style>
