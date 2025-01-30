<template>
  <div class="registry-container">
    <h1>Registry Interface</h1>

    <!-- Upload Document Section -->
    <div class="section">
      <h2>1. Upload Document</h2>
      <textarea v-model="documentText" placeholder="Enter document content"></textarea>
      <button @click="updateHash">Calculate Hash</button>
      <p v-if="fileHash">Generated Hash: {{ fileHash }}</p>
      <input v-model="documentHash" placeholder="Enter document hash" />
      <button @click="uploadDocument">Upload</button>
      <p v-if="uploadResponse">Response: {{ uploadResponse }}</p>
    </div>

    <!-- Create or Load Wallet -->
    <div class="create-wallet">
      <h3>Load Wallet</h3>
      <input v-model="newWalletName" placeholder="Wallet Name" />
      <button @click="createOrLoadWallet">Load Wallet</button>
    </div>

    <!-- Wallet Info -->
    <div v-if="activeWallet" class="wallet-info">
      <h3>Active Wallet: {{ activeWallet.name }} (Balance: {{ activeWallet.balance }} BTC)</h3>
      <button @click="logOffWallet">Log Off Wallet</button>
    </div>

    <!-- Transfer Funds -->
    <div v-if="activeWallet" class="transfer-funds">
      <h3>Pay the service</h3>
      <input v-model="transferToAddress" placeholder="Recipient Address" />
      <input
        v-model="transferAmount"
        type="number"
        step="0.000001"
        placeholder="Amount (up to 6 decimals)"
      />
      <button @click="transferFunds">Transfer</button>
    </div>

    <!-- Mint Block -->
    <div v-if="activeWallet" class="mint-block">
      <h3>Mint Block</h3>
      <button @click="mintBlock">Mint 1 Block</button>
    </div>

    <!-- Payment Confirmation Section -->
    <div class="section">
      <h2>2. Confirm Payment</h2>
      <input v-model="paymentDocumentHash" placeholder="Enter document hash" />
      <button @click="confirmPayment">Confirm Payment</button>
      <p v-if="paymentResponse">Response: {{ paymentResponse }}</p>
    </div>

    <!-- Send Transaction Section -->
    <div class="section">
      <h2>3. Send Transaction</h2>
      <input v-model="transactionDocumentHash" placeholder="Enter document hash" />
      <button @click="sendTransaction">Send Transaction</button>
      <p v-if="transactionResponse">Response: {{ transactionResponse }}</p>
    </div>

    <!-- Mining Confirmation Section -->
    <div class="section">
      <h2>4. Confirm Mining</h2>
      <input v-model="miningTxId" placeholder="Enter transaction ID" />
      <button @click="confirmMining">Confirm Mining</button>
      <p v-if="miningResponse">Response: {{ miningResponse }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { sha256 } from 'crypto-hash'

export default {
  data() {
    return {
      documentText: '', // Holds the document content
      fileHash: '', // Holds the generated hash
      documentHash: '', // Holds the manually entered hash
      uploadResponse: null,

      activeWallet: null, // Track the active wallet (name and balance)
      newWalletName: '', // Input for new wallet name
      transferToAddress: '', // Recipient address for transfer
      transferAmount: 0, // Amount to transfer (up to 6 decimals)

      paymentDocumentHash: '',
      paymentResponse: null,

      transactionDocumentHash: '',
      transactionResponse: null,

      miningTxId: '',
      miningResponse: null,
    }
  },
  methods: {
    // Generate SHA-256 hash of the document
    async updateHash() {
      if (!this.documentText) {
        alert('Please enter document content.')
        return
      }
      this.fileHash = await sha256(this.documentText) // Await the Promise
      this.documentHash = this.fileHash // Auto-fill the hash input field
    },

    async uploadDocument() {
      if (!this.documentHash) {
        alert('Please generate or enter a document hash.')
        return
      }
      try {
        const response = await axios.post('reg/upload', {
          document: this.documentText,
          document_hash: this.documentHash,
        })
        this.uploadResponse = response.data
      } catch (error) {
        this.uploadResponse = `Error: ${error.message}`
      }
    },

    async confirmPayment() {
      try {
        const response = await axios.post('reg/payment-confirmation', {
          document_hash: this.paymentDocumentHash,
        })
        this.paymentResponse = response.data
      } catch (error) {
        this.paymentResponse = `Error: ${error.message}`
      }
    },

    async sendTransaction() {
      try {
        const response = await axios.post('reg/send-transaction', {
          document_hash: this.transactionDocumentHash,
        })
        this.transactionResponse = response.data
      } catch (error) {
        this.transactionResponse = `Error: ${error.message}`
      }
    },

    async confirmMining() {
      try {
        const response = await axios.post('reg/mining-confirmation', {
          tx_id: this.miningTxId,
        })
        this.miningResponse = response.data
      } catch (error) {
        this.miningResponse = `Error: ${error.message}`
      }
    },

    // Transfer funds from the active wallet
    async transferFunds() {
      if (this.transferToAddress.trim() === '' || this.transferAmount <= 0) {
        alert('Please enter a valid recipient address and amount.')
        return
      }
      try {
        const response = await axios.post('/api/send_transaction', {
          wallet_name: this.activeWallet.name,
          to_address: this.transferToAddress,
          amount: this.transferAmount,
        })
        this.fetchWalletBalance() // Refresh balance after transfer
        alert(`Transaction sent: ${response.data.txid}`)
      } catch (error) {
        console.error('Error transferring funds:', error)
      }
    },

    // Create or Load Wallet
    async createOrLoadWallet() {
      if (this.newWalletName.trim() === '') {
        alert('Please enter a wallet name.')
        return
      }
      try {
        // Check if the wallet exists
        const walletsResponse = await axios.get('/api/list_wallets')
        const wallets = walletsResponse.data.wallets || []
        if (wallets.includes(this.newWalletName)) {
          // Wallet exists, load it
          await this.loadWallet(this.newWalletName)
        } else {
          // Wallet does not exist, create it
          await this.createWallet(this.newWalletName)
        }
      } catch (error) {
        console.error('Error creating or loading wallet:', error)
      }
    },

    // Log off the active wallet
    logOffWallet() {
      this.activeWallet = null
    },
    // Load an existing wallet
    async loadWallet(walletName) {
      this.activeWallet = { name: walletName, balance: 0 }
      this.fetchWalletBalance()
    },

    // Fetch wallet balance
    async fetchWalletBalance() {
      try {
        const response = await axios.get('/api/get_balance', {
          params: { wallet_name: this.activeWallet.name },
        })
        this.activeWallet.balance = response.data.balance
      } catch (error) {
        console.error('Error fetching wallet balance:', error)
      }
    },

    // Mint a block to the active wallet
    async mintBlock() {
      try {
        const response = await axios.post('/api/mine', {
          wallet_name: this.activeWallet.name,
          num_blocks: 1,
        })
        alert(response.data.message)
        this.fetchWalletBalance() // Refresh balance after mining
      } catch (error) {
        console.error('Error mining block:', error)
      }
    },
  },
}
</script>

<style scoped>
.registry-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.section {
  margin-bottom: 30px;
}

h1,
h2 {
  color: #333;
}

textarea,
input {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 10px;
}

button:hover {
  background-color: #0056b3;
}

p {
  margin-top: 10px;
  color: #555;
}
</style>
