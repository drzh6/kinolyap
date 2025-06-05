<script setup>
import axios from 'axios'
import { onMounted, ref } from 'vue'
import FavoriteButton from '~/components/base/FavoriteButton.vue';
import WatchlistButton from '~/components/base/WatchlistButton.vue';

const config = useRuntimeConfig()
const baseUrl = config.public.baseURL

const roulette = ref()

const rouletteFetch = async () => {
  const res = await axios.post(`${baseUrl}/roulette`, {}, {
    withCredentials: true,
  })
}

</script>

<template>
  <div class='flex flex-col w-full'>
    <h2 class="text-xl font-bold my-8">Мой watchlist</h2>
  </div>
</template>

<style scoped>

</style>