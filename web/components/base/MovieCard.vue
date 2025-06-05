<script setup lang="ts">
defineProps<{
  movie: {
    id: number
    title: string
    poster_url: string
    rating: number
    year: number
    genre: string
  }
  getPreferredGenre: (genre: string) => string
}>()
</script>

<template>
  <NuxtLink
      :to="`/movies/${movie.id}`"
      class="overflow-hidden w-[260px] max-w-full"
  >
    <img
        :src="movie.poster_url"
        alt="Poster"
        class="w-full object-cover rounded-xl"
    />
    <div class="flex flex-col justify-start items-center h-full overflow-hidden rounded-[10px] w-full">
      <p class="truncate text-text text-sm font-base w-full font-bold py-2">
        {{ movie.title }}
      </p>
      <div class="w-full flex flex-row justify-between space-x-2 pb-2 text-primary text-sm space-x-4">
        <p>{{ movie.year }}</p>
<!--        <p>{{ getPreferredGenre(movie.genre) }}</p>-->
        <div class='flex flex-row justify-between items-center gap-1'>
          <Icon name='tabler:star-filled'></Icon>
          <p>{{ movie.rating.toFixed(2) }}</p>
        </div>

      </div>
    </div>
  </NuxtLink>
</template>
