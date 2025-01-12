<template>
  <div class="blockchain-info">
    <h2>Shi(し) Satoshi - Blockchain Info</h2>
    <vue-json-pretty :data="blockchainInfo" />
  </div>
</template>

<script>
import axios from 'axios'
import VueJsonPretty from 'vue-json-pretty'
import 'vue-json-pretty/lib/styles.css'

export default {
  components: {
    VueJsonPretty,
  },
  data() {
    return {
      blockchainInfo: {}, // Holds the blockchain data
    }
  },
  created() {
    // Fetch blockchain info from the API
    axios
      .get('/api/getblockchaininfo')
      .then((response) => {
        try {
          // Check if the response is a string
          if (typeof response.data === 'string') {
            this.blockchainInfo = JSON.parse(response.data) // Convert string to object
          } else {
            this.blockchainInfo = response.data // Already an object
          }
          console.log('Blockchain Info:', this.blockchainInfo) // Log the parsed data
        } catch (error) {
          console.error('Error parsing JSON:', error)
        }
      })
      .catch((error) => {
        console.error('Error fetching blockchain info:', error)
      })
  },
}
</script>

<style scoped>
.blockchain-info {
  position: absolute;
  top: 20px;
  right: 20px;
  background-color: #f5f5f5;
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid #ddd;
  max-width: 400px;
  font-family: Arial, sans-serif;
}

h2 {
  margin-bottom: 1rem;
  font-size: 1.2rem;
  color: #333;
}
</style>
