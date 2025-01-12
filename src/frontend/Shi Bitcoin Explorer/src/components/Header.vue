<template>
  <div>
    <p>Blockchain Info: {{ blockchainInfoServer }}</p>
  </div>
</template>

<script>
import axios from 'axios'

axios.defaults.baseURL = 'http://127.0.0.1:5000'

export default {
  data() {
    return {
      blockchainInfoServer: {},
    }
  },
  created() {
    axios
      .get('api/getblockchaininfo')
      .then((response) => {
        this.blockchainInfo = response.data
        this.$emit('blockchain-info', this.blockchainInfo)
      })
      .catch((error) => {
        console.error('Error fetching blockchain info:', error)
      })
  },
}
</script>

<style scoped>
p {
  position: absolute;
  top: 10px;
  right: 10px;
}
</style>
