<template>
  <div class="registry-container">
    <h2>Copyright Registration</h2>

    <!-- Document Upload Section -->
    <div class="upload-section">
      <input type="file" @change="handleFileUpload" />
      <button @click="uploadDocument" :disabled="!file || isUploading">
        {{ isUploading ? 'Uploading...' : 'Upload Document' }}
      </button>
    </div>

    <!-- Payment Section -->
    <div v-if="walletAddress" class="payment-section">
      <p>Please send the payment to the following Bitcoin address:</p>
      <p>
        <strong>{{ walletAddress }}</strong>
      </p>
      <p>Amount: <strong>0.001 BTC</strong></p>
      <button @click="checkPaymentStatus" :disabled="isCheckingPayment">
        {{ isCheckingPayment ? 'Checking...' : 'Check Payment Status' }}
      </button>
    </div>

    <!-- Status Section -->
    <div v-if="status" class="status-section">
      <p>
        Status: <strong>{{ status }}</strong>
      </p>
      <p v-if="blockchainLink">
        <a :href="blockchainLink" target="_blank">View on Blockchain</a>
      </p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { sha256 } from 'crypto-hash'

export default {
  data() {
    return {
      file: null,
      fileHash: '',
      walletAddress: '',
      status: '',
      blockchainLink: '',
      isUploading: false,
      isCheckingPayment: false,
    }
  },
  methods: {
    async handleFileUpload(event) {
      this.file = event.target.files[0]
      const fileBuffer = await this.file.arrayBuffer()
      this.fileHash = await sha256(fileBuffer)
    },
    async uploadDocument() {
      if (!this.file) {
        alert('Please select a file to upload.')
        return
      }

      this.isUploading = true

      try {
        const response = await axios.post('/api/register-document', {
          fileHash: this.fileHash,
        })

        this.walletAddress = response.data.walletAddress
        this.status = 'Pending Payment'
      } catch (error) {
        console.error('Error uploading document:', error)
        alert('Failed to upload document.')
      } finally {
        this.isUploading = false
      }
    },
    async checkPaymentStatus() {
      this.isCheckingPayment = true

      try {
        const response = await axios.get('/api/check-payment', {
          params: { walletAddress: this.walletAddress },
        })

        if (response.data.paymentConfirmed) {
          this.status = 'Pending Block Mining'
          this.waitForMiningConfirmation()
        } else {
          alert('Payment not yet confirmed. Please try again later.')
        }
      } catch (error) {
        console.error('Error checking payment status:', error)
        alert('Failed to check payment status.')
      } finally {
        this.isCheckingPayment = false
      }
    },
    async waitForMiningConfirmation() {
      try {
        const response = await axios.get('/api/mining-status', {
          params: { walletAddress: this.walletAddress },
        })

        if (response.data.miningCompleted) {
          this.status = 'Mining Completed'
          this.blockchainLink = response.data.blockchainLink
        } else {
          setTimeout(this.waitForMiningConfirmation, 5000) // Retry after 5 seconds
        }
      } catch (error) {
        console.error('Error checking mining status:', error)
        alert('Failed to check mining status.')
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

.upload-section,
.payment-section,
.status-section {
  margin-bottom: 1.5rem;
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

a {
  color: var(--button-bg-color);
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>
