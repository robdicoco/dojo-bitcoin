<template>
  <div class="search-bar">
    <select v-model="selectedApi">
      <option value="getbalance">Get Balance</option>
      <option value="getblockhash">Get Block Hash</option>
      <option value="getblock">Get Block</option>
      <option value="gettransaction">Get Transaction</option>
      <option value="getrawtransaction">Get Raw Transaction</option>
    </select>
    <input v-model="inputValue" :placeholder="placeholderText" />
    <button @click="fetchData">Search</button>
    <p v-if="error" class="error-message">{{ error }}</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      selectedApi: 'getbalance', // Default selected API
      inputValue: '', // User input value
      error: '', // Error message
    }
  },
  computed: {
    placeholderText() {
      // Dynamic placeholder based on selected API
      switch (this.selectedApi) {
        case 'getbalance':
          return 'Enter Bitcoin address'
        case 'getblockhash':
          return 'Enter block height'
        case 'getblock':
          return 'Enter block hash'
        case 'gettransaction':
          return 'Enter transaction ID'
        case 'getrawtransaction':
          return 'Enter transaction ID'
        default:
          return 'Enter value'
      }
    },
  },
  methods: {
    async fetchData() {
      this.error = '' // Clear previous errors

      // Validate input
      if (!this.inputValue || this.inputValue.trim() === '') {
        this.error = 'Please enter a value.'
        return
      }

      // Construct the API URL and parameters
      let url = `/api/${this.selectedApi}` // Use /api prefix for proxy
      let params = {}

      // Set parameters based on the selected API
      switch (this.selectedApi) {
        case 'getbalance':
          params.address = this.inputValue
          break
        case 'getblockhash':
          params.height = this.inputValue
          break
        case 'getblock':
          params.hash = this.inputValue
          break
        case 'gettransaction':
          params.txid = this.inputValue
          break
        case 'getrawtransaction':
          params.txid = this.inputValue
          break
        default:
          this.error = 'Unknown API selected.'
          return
      }

      try {
        // Make the API call
        const response = await axios.get(url, { params })

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

select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

input {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  flex-grow: 1;
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
