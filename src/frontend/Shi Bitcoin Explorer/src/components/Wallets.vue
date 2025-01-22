<template>
  <div class="wallets">
    <h2>Wallets</h2>

    <!-- Create or Load Wallet -->
    <div class="create-wallet">
      <h3>Create or Load Wallet</h3>
      <input v-model="newWalletName" placeholder="Wallet Name" />
      <button @click="createOrLoadWallet">Create or Load Wallet</button>
    </div>

    <!-- Wallet Info -->
    <div v-if="activeWallet" class="wallet-info">
      <h3>Active Wallet: {{ activeWallet.name }} (Balance: {{ activeWallet.balance }} BTC)</h3>
      <button @click="logOffWallet">Log Off Wallet</button>
    </div>

    <!-- API Call Logs -->
    <div v-if="apiLogs.length > 0" class="api-logs">
      <h4>API Call Logs</h4>
      <ul>
        <li v-for="(log, index) in apiLogs" :key="index">
          <strong>{{ log.action }}:</strong> {{ log.message }}
        </li>
      </ul>
    </div>

    <!-- Generate Addresses -->
    <div v-if="activeWallet" class="generate-addresses">
      <h3>Generate Addresses</h3>
      <input
        v-model="addressCount"
        type="number"
        min="1"
        max="5"
        placeholder="Number of addresses (1-5)"
      />
      <button @click="generateAddresses">Generate Addresses</button>
      <div v-if="generatedAddresses.length > 0">
        <h4>Generated Addresses:</h4>
        <ul>
          <li v-for="(address, index) in generatedAddresses" :key="index">
            {{ address }}
          </li>
        </ul>
      </div>
    </div>

    <!-- Mint Block -->
    <div v-if="activeWallet" class="mint-block">
      <h3>Mint Block</h3>
      <button @click="mintBlock">Mint 1 Block</button>
    </div>

    <!-- Transfer Funds -->
    <div v-if="activeWallet" class="transfer-funds">
      <h3>Transfer Funds</h3>
      <input v-model="transferToAddress" placeholder="Recipient Address" />
      <input
        v-model="transferAmount"
        type="number"
        step="0.000001"
        placeholder="Amount (up to 6 decimals)"
      />
      <button @click="transferFunds">Transfer</button>
    </div>

    <!-- List Existing Wallets -->
    <div class="existing-wallets">
      <h3>Existing Wallets</h3>
      <div v-if="wallets.length === 0">No wallets found.</div>
      <ul v-else>
        <li v-for="wallet in wallets" :key="wallet">{{ wallet }}</li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  props: {
    wallets: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      newWalletName: '', // Input for new wallet name
      activeWallet: null, // Track the active wallet (name and balance)
      addressCount: 1, // Number of addresses to generate (1-5)
      generatedAddresses: [], // List of generated addresses
      transferToAddress: '', // Recipient address for transfer
      transferAmount: 0, // Amount to transfer (up to 6 decimals)
      apiLogs: [], // Logs for API calls
    }
  },
  methods: {
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
          this.addApiLog('Load Wallet', `Wallet "${this.newWalletName}" loaded successfully.`)
        } else {
          // Wallet does not exist, create it
          await this.createWallet(this.newWalletName)
          this.addApiLog('Create Wallet', `Wallet "${this.newWalletName}" created successfully.`)
        }
      } catch (error) {
        console.error('Error creating or loading wallet:', error)
        this.addApiLog('Error', `Failed to create or load wallet: ${error.message}`)
      }
    },

    // Create a new wallet
    async createWallet(walletName) {
      const response = await axios.post('/api/create_wallet', { wallet_name: walletName })
      this.activeWallet = { name: walletName, balance: 0 }
      this.fetchWalletBalance()
      this.$emit('create-wallet', walletName) // Emit event to parent
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
        this.addApiLog('Error', `Failed to fetch wallet balance: ${error.message}`)
      }
    },

    // Generate addresses for the active wallet
    async generateAddresses() {
      if (this.addressCount < 1 || this.addressCount > 5) {
        alert('Please enter a number between 1 and 5.')
        return
      }
      try {
        const response = await axios.post('/api/generate_multi_address', {
          wallet_name: this.activeWallet.name,
          num_addresses: this.addressCount,
        })
        this.generatedAddresses = response.data.addresses
        this.addApiLog(
          'Generate Addresses',
          `${this.addressCount} address(es) generated successfully.`,
        )
      } catch (error) {
        console.error('Error generating addresses:', error)
        this.addApiLog('Error', `Failed to generate addresses: ${error.message}`)
      }
    },

    // Mint a block to the active wallet
    async mintBlock() {
      try {
        const response = await axios.post('/api/mine', {
          wallet_name: this.activeWallet.name,
          num_blocks: 1,
        })
        this.addApiLog('Mint Block', `Block mined successfully: ${response.data.blockHash}`)
        this.fetchWalletBalance() // Refresh balance after mining
      } catch (error) {
        console.error('Error mining block:', error)
        this.addApiLog('Error', `Failed to mint block: ${error.message}`)
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
        this.addApiLog('Transfer Funds', `Transaction sent successfully: ${response.data.txid}`)
        this.fetchWalletBalance() // Refresh balance after transfer
      } catch (error) {
        console.error('Error transferring funds:', error)
        this.addApiLog('Error', `Failed to transfer funds: ${error.message}`)
      }
    },

    // Log off the active wallet
    logOffWallet() {
      this.activeWallet = null
      this.generatedAddresses = []
      this.transferToAddress = ''
      this.transferAmount = 0
      this.addApiLog('Log Off', 'Wallet logged off successfully.')
    },

    // Add a log entry for API calls
    addApiLog(action, message) {
      this.apiLogs.push({ action, message })
    },
  },
}
</script>

<style scoped>
.wallets {
  padding: 1rem;
  background-color: #f5f5f5;
  border-radius: 8px;
  border: 1px solid #ddd;
}

.create-wallet,
.wallet-info,
.generate-addresses,
.mint-block,
.transfer-funds,
.existing-wallets,
.api-logs {
  margin-bottom: 1.5rem;
}

h3 {
  margin-bottom: 0.5rem;
  font-size: 1.2rem;
  color: #333;
}

input {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-right: 0.5rem;
  width: 200px;
}

button {
  padding: 0.5rem 1rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 0.5rem;
}

button:hover {
  background-color: #0056b3;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  padding: 0.5rem;
  background-color: #fff;
  border-radius: 4px;
  border: 1px solid #eee;
  margin-bottom: 0.5rem;
}

.api-logs {
  background-color: #fff;
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid #ddd;
}

.api-logs ul {
  margin: 0;
}

.api-logs li {
  margin-bottom: 0.5rem;
}
</style>
