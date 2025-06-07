<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useMovieStore } from '~/stores/movieStore'
import MovieCarousel from '@/components/base/MovieCarousel.vue'

const store = useMovieStore()

onMounted(() => {
  store.fetchMovies()
})

const carouselTopMovies = computed(() =>
    store.movies.filter((movie) => movie.id >= 501 && movie.id <= 515)
)

const carouselFavoriteMovies = computed(() =>
    store.movies.filter((movie) => movie.id >= 516 && movie.id <= 530)
)

const carouselComedyMovies = computed(() =>
    store.movies.filter((movie) => movie.genres.toLowerCase().split(',').map(g => g.trim()).includes('комедия')
))

const carouselActionMovies = computed(() =>
    store.movies.filter((movie) => movie.genres.toLowerCase().split(',').map(g => g.trim()).includes('боевик')
    ))

const getPreferredGenre = (genreStr: string) => {
  const genres = genreStr.split(',').map(g => g.trim())
  return genres[1] || genres[0] || genres[2] || 'Жанр неизвестен'
}

const ComedyGenre = () => 'комедия'
const ActionMovieGenre = () => 'боевик'

</script>

<template>
  <div class='flex flex-col'>
    <MovieCarousel
      title="Лучшие фильмы"
      :movies="carouselTopMovies"
      :getPreferredGenre="getPreferredGenre"
    />
    <MovieCarousel
        title="Избранное"
        :movies="carouselFavoriteMovies"
        :getPreferredGenre="getPreferredGenre"
    />
    <MovieCarousel
        title="Комедии"
        :movies="carouselComedyMovies"
        :getPreferredGenre="ComedyGenre"
    />
    <MovieCarousel
        title="Боевики"
        :movies="carouselActionMovies"
        :getPreferredGenre="ActionMovieGenre"
    />
  </div>
</template>
