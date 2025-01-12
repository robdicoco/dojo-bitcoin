<template>
  <div>
    <input v-model="query" placeholder="Search" />
    <button @click="search">Search</button>
    <p v-if="result">Result: {{ result }}</p>
  </div>
</template>

<script>
import api from '@/services/api'

export default {
  data() {
    return {
      query: '',
      result: null,
    }
  },
  methods: {
    async search() {
      try {
        const response = await api.getBalance(this.query) // Change this to your required search method
        this.result = response.data
      } catch (error) {
        console.error(error)
      }
    },
  },
}
</script>

<style scoped>
input {
  margin-right: 10px;
}
</style>
