<template>
  <div>
    <select v-model="selectedApi">
      <option value="getbalance">Get Balance</option>
      <option value="getblockhash">Get Block Hash</option>
      <option value="getblock">Get Block</option>
      <option value="gettransaction">Get Transaction</option>
      <option value="getrawtransaction">Get Raw Transaction</option>
    </select>
    <input v-model="inputValue" :placeholder="placeholderText" />
    <button @click="fetchData">Search</button>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      selectedApi: 'getbalance',
      inputValue: '',
    }
  },
  computed: {
    placeholderText() {
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
    fetchData() {
      let url = `/${this.selectedApi}?`
      let params = {}

      switch (this.selectedApi) {
        case 'getbalance':
          params.address = this.inputValue
          break
        case 'getblockhash':
          params.height = this.inputValue
          break
        case 'getblock':
          params.block_hash = this.inputValue
          break
        case 'gettransaction':
          params.txid = this.inputValue
          break
        case 'getrawtransaction':
          params.txid = this.inputValue
          break
        default:
          console.error('Unknown API selected.')
          return
      }

      url += new URLSearchParams(params)
      axios
        .get(url)
        .then((response) => {
          this.$emit('data-fetched', response.data)
        })
        .catch((error) => {
          console.error('Error fetching data:', error)
        })
    },
  },
}
</script>
