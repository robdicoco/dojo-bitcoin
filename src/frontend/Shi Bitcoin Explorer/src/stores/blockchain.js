import { defineStore } from 'pinia'
import axios from 'axios'

export const useBlockchainStore = defineStore('blockchain', {
  state: () => ({
    blockchainInfo: null,
    balance: null,
    blockHash: null,
    block: null,
    transaction: null,
    rawTransaction: null,
    searchQuery: '',
  }),
  actions: {
    async fetchBlockchainInfo() {
      try {
        const response = await axios.get('http://172.236.149.45/getblockchaininfo')
        this.blockchainInfo = response.data
      } catch (error) {
        console.error('Error fetching blockchain info:', error)
        this.blockchainInfo = null
      }
    },
    async fetchBalance(address) {
      try {
        const response = await axios.get(`http://172.236.149.45/getbalance?address=${address}`)
        this.balance = response.data
      } catch (error) {
        console.error('Error fetching balance:', error)
        this.balance = null
      }
    },
    async fetchBlockHash(height) {
      try {
        const response = await axios.get(`http://172.236.149.45/getblockhash?height=${height}`)
        this.blockHash = response.data
      } catch (error) {
        console.error('Error fetching block hash:', error)
        this.blockHash = null
      }
    },
    async fetchBlock(hash) {
      try {
        const response = await axios.get(`http://172.236.149.45/getblock?hash=${hash}`)
        this.block = response.data
      } catch (error) {
        console.error('Error fetching block:', error)
        this.block = null
      }
    },
    async fetchTransaction(txid) {
      try {
        const response = await axios.get(`http://172.236.149.45/gettransaction?txid=${txid}`)
        this.transaction = response.data
      } catch (error) {
        console.error('Error fetching transaction:', error)
        this.transaction = null
      }
    },
    async fetchRawTransaction(txid) {
      try {
        const response = await axios.get(`http://172.236.149.45/getrawtransaction?txid=${txid}`)
        this.rawTransaction = response.data
      } catch (error) {
        console.error('Error fetching raw transaction:', error)
        this.rawTransaction = null
      }
    },
  },
})
