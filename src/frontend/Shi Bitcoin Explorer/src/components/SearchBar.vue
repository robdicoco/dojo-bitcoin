<template>
  <div class="search-bar">
    <input
      v-model="inputValue"
      placeholder="Enter block height, block hash, transaction ID, or address"
    />
    <button @click="fetchData">Search</button>
    <p v-if="error" class="error-message">{{ error }}</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      inputValue: '', // User input value
      error: '', // Error message
      rawTransaction: null,
    }
  },
  methods: {
    // Function to detect the type of input
    async detectInputType(input) {
      input = input.trim()

      // Check if input is a block height (numeric)
      if (/^\d+$/.test(input)) {
        return 'blockheight'
      }

      // Check if input is a block hash (64-character hex string)
      if (/^[a-fA-F0-9]{64}$/.test(input)) {
        // Check if the input is a block hash or transaction ID
        // (Block hashes and transaction IDs are both 64-character hex strings)
        // For now, assume it's a transaction ID if it starts with '3b' (common for regtest txids)

        await this.fetchRawTransaction(input)
        if (this.rawTransaction == null) {
          return 'blockhash'
        } else {
          return 'txid'
        }
      }

      // Check if input is a Bitcoin address (starts with 'bcrt1' for regtest)
      if (/^bcrt1[a-zA-HJ-NP-Z0-9]{25,39}$/.test(input)) {
        return 'address'
      }

      // If no match, return unknown
      return 'unknown'
    },

    async fetchData() {
      this.error = '' // Clear previous errors

      // Validate input
      if (!this.inputValue || this.inputValue.trim() === '') {
        this.error = 'Please enter a value.'
        return
      }

      // Detect the input type
      const inputType = await this.detectInputType(this.inputValue)

      // Determine the API endpoint based on the input type
      let endpoint = ''
      let params = {}

      switch (inputType) {
        case 'blockheight':
          endpoint = 'getblockhash'
          params = { height: this.inputValue }
          break
        case 'blockhash':
          endpoint = 'getblock'
          params = { hash: this.inputValue }
          break
        case 'txid':
          endpoint = 'gettransaction'
          params = { txid: this.inputValue }
          break
        case 'address':
          endpoint = 'get_address_balance'
          params = { address: this.inputValue }
          break
        default:
          this.error =
            'Invalid input. Please enter a valid block height, block hash, transaction ID, or address.'
          return
      }
      console.info('endpoint:', endpoint)
      try {
        // Make the API call
        const response = await axios.get(`/api/${endpoint}`, { params })

        // Handle raw string responses (e.g., block hash)
        let data = response.data
        if (typeof data === 'string') {
          data = { result: data } // Wrap the string in a JSON object
        }

        // Emit the fetched data
        this.$emit('data-fetched', data)
      } catch (error) {
        console.error('Error fetching data:', error)
        if (error.response) {
          // The request was made and the server responded with a status code
          this.error = `Error: ${error.response.status} - ${error.response.data}`
        } else if (error.request) {
          // The request was made but no response was received
          this.error = 'No response from the server.'
        } else {
          // Something happened in setting up the request
          this.error = 'Error setting up the request.'
        }
      }
    },

    async fetchRawTransaction(txid) {
      try {
        const response = await axios.get('/api/getrawtransaction', {
          params: { txid: txid },
        })
        this.rawTransaction = response.data
      } catch (error) {
        console.info('Error fetching raw transaction:', error)
        this.rawTransaction = null
      }
    },
  },
}
</script>

<style scoped>
.search-bar {
  display: flex;
  gap: 10px;
  margin-bottom: 2rem;
  align-items: center;
}

input {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  flex-grow: 1;
  font-size: 1rem;
  max-width: 500px;
  width: 100%;
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

.error-message {
  color: red;
  margin-top: 0.5rem;
}
</style>
