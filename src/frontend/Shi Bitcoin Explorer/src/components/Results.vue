<template>
  <div>
    <h2>Search Results</h2>
    <pre>{{ JSON.stringify(searchResults, null, 2) }}</pre>
  </div>
</template>

<script>
export default {
  props: {
    searchResults: Object,
  },
}
</script>
