<!--pages/movies/[id].vue-->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useMovieStore } from '~/stores/movieStore'
import FavoriteButton from '@/components/base/FavoriteButton.vue'
import WatchlistButton from "@/components/base/WatchlistButton.vue";

const route = useRoute()
const store = useMovieStore()
const loading = ref(true)

onMounted(async () => {
  if (!store.loaded) {
    await store.fetchMovies()
  }
  loading.value = false
})

const movie = computed(() =>
    store.movies.find(m => String(m.id) === route.params.id)
)
</script>

<template>
  <div v-if="loading">
    <p>Загрузка...</p>
  </div>

  <div v-else-if="movie" class='bg-background flex flex-row justify-center w-full space-x-16 pt-8'>
    <div>
      <img :src="movie.poster_url" alt="Poster" class='w-full h-auto rounded-xl'/>
    </div>
    <div class='w-full'>
      <h1 class='text-text text-[72px]'>{{ movie.title }}</h1>
      <div class='flex flex-row gap-4 pl-1'>
        <p class='mb-8'>{{ movie.year }}</p>
        <span>/</span>
        <p class='mb-8'>{{ movie.genre }}</p>
      </div>

      <div class='flex flex-row items-center gap-16 mb-8'>
        <WatchlistButton :movieId='movie.id' class="w-[46px] h-[46px]"/>
        <FavoriteButton :movieId='movie.id' class="w-[40px] h-[40px]"/>
        <div class='text-text flex flex-row items-center gap-2'>
          <NuxtIcon name='tabler:star-filled'  class="size-[40px] text-warning" />
          <p>{{ movie.rating.toFixed(2) }}</p>
        </div>
      </div>
      <p class='text-justify text-text text-[18px]'>{{ movie.description }}</p>
    </div>
  </div>
  <div v-else>
    <p>Фильм не найден.</p>
  </div>
</template>

<style scoped>
img {
  margin-bottom: 1em;
}
</style>
