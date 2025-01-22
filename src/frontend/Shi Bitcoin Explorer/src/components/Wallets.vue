<template>
  <div class="wallets">
    <h2>Wallets</h2>

    <!-- Create New Wallet -->
    <div class="create-wallet">
      <h3>Create New Wallet</h3>
      <input v-model="newWalletName" placeholder="Wallet Name" />
      <button @click="createWallet">Create Wallet</button>
    </div>

    <!-- Generate Addresses -->
    <div v-if="newWalletCreated" class="generate-addresses">
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
    <div v-if="newWalletCreated" class="mint-block">
      <h3>Mint Block</h3>
      <button @click="mintBlock">Mint 1 Block</button>
    </div>

    <!-- Transfer Funds -->
    <div v-if="newWalletCreated" class="transfer-funds">
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
      newWalletCreated: false, // Track if a new wallet is created
      addressCount: 1, // Number of addresses to generate (1-5)
      generatedAddresses: [], // List of generated addresses
      transferToAddress: '', // Recipient address for transfer
      transferAmount: 0, // Amount to transfer (up to 6 decimals)
    }
  },
  methods: {
    // Create a new wallet
    async createWallet(walletName) {
      try {
        const response = await axios.post('/api/create_wallet', { wallet_name: walletName })
        this.fetchWallets() // Refresh the wallet list
        return response.data
      } catch (error) {
        console.error('Error creating wallet:', error)
        throw error
      }
    },

    // Generate multiple addresses
    async generateAddresses({ walletName, count }) {
      try {
        const response = await axios.post('/api/generate_multi_address', {
          wallet_name: walletName,
          num_addresses: count,
        })
        return response.data
      } catch (error) {
        console.error('Error generating addresses:', error)
        throw error
      }
    },

    // Mint a block
    async mintBlock(walletName) {
      try {
        const response = await axios.post('/api/mine', { wallet_name: walletName, num_blocks: 1 })
        return response.data
      } catch (error) {
        console.error('Error mining block:', error)
        throw error
      }
    },

    // Transfer funds
    async transferFunds({ walletName, toAddress, amount }) {
      try {
        const response = await axios.post('/api/send_transaction', {
          wallet_name: walletName,
          to_address: toAddress,
          amount: amount,
        })
        return response.data
      } catch (error) {
        console.error('Error transferring funds:', error)
        throw error
      }
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
.generate-addresses,
.mint-block,
.transfer-funds,
.existing-wallets {
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
</style>
