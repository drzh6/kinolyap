<script setup lang="ts">
import MovieCard from './MovieCard.vue'

defineProps<{
  title: string
  movies: Array<{
    id: number
    name_ru: string
    poster_url: string
    rating_kinopoisk: number
    year: number
    genres: string
  }>
  getPreferredGenre: (genre: string) => string
}>()
</script>

<template>
  <div v-if="movies.length" class="w-full max-w-[1280px] mx-auto bg-background h-full py-8">
    <p class="text-text text-lg font-semibold mb-8">{{ name_ru }}</p>
    <NuxtCarousel
        v-slot="{ item }"
        :items="movies"
        loop
        arrows
        :ui="{ item: 'basis-1/7' }"
    >
      <MovieCard :movie="item" :getPreferredGenre="getPreferredGenre" />
    </NuxtCarousel>
  </div>
</template>
