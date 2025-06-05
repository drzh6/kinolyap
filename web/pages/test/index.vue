<script setup>
import { ref } from 'vue'

const result = ref('')

const apiUrl = 'http://localhost:5000/api'                       // .env не работает, добавить

const fetchPing = async () => {
  const res = await fetch(`${apiUrl}/ping`)
  const data = await res.json()
  result.value = data.message
}

</script>

<template>
  <div>
    <button @click="fetchPing">Пинг API</button>
    <div>{{ result }}</div>
  </div>
</template>

<style scoped>

</style>