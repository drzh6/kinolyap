<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import FavoriteButton from '@/components/base/FavoriteButton.vue';
import WatchlistButton from '@/components/base/WatchlistButton.vue';

const favorites = ref([])

const config = useRuntimeConfig()
const baseUrl = config.public.baseURL

onMounted(async () => {
  try {
    const res = await axios.get(`${baseUrl}/favorites`, {
      withCredentials: true
    })
    favorites.value = res.data
  }
  catch (error) {
    console.error('Не удалось загрузить favorites:', error)
  }
})

</script>

<template>
  <div class='flex flex-col w-full'>
    <h2 class="text-xl font-bold my-8">Мои любимые фильмы</h2>

    <div>

      <!-- Если список пуст, показываем сообщение -->
      <div v-if="favorites.length === 0">Нет сохранённых фильмов</div>

      <!-- Иначе выводим каждый фильм в списке -->

      <div v-else >
        <div class='p-4 mb-4 w-full h-[200px] overflow-hidden rounded-xl bg-black/20'
             v-for="movie in favorites"
             :key="movie.id"
        >
          <div class='flex flex-row items-center'>
            <div class='flex flex-row gap-10'>
              <NuxtLink :to="`/movies/${movie.id}`">
              <div class='w-[110px]'>
                <img :src="movie.poster_url" alt='Poster' class='w-full object-cover rounded-xl'>
              </div>
                </NuxtLink>
            </div>
            <div class='flex flex-col gap-2 pl-4'>
              <div class='flex flex-col gap-2'>
                {{movie.title}}
                <div class='flex fle-row text-white/70 text-xs gap-2'>
                  {{movie.year}}
                  <span>/</span>
                  {{movie.director}}
                </div>
                <div class='flex flex-row gap-4'>
                  <div class='flex flex-row items-center gap-1 text-xs'>
                    <NuxtIcon name='tabler:star-filled' class='size-3 text-warning'></NuxtIcon>
                    <p>{{ movie.rating.toFixed(2) }}</p>
                  </div>
                  <WatchlistButton :movieId='movie.id' class="w-6 h-6"/>
                  <FavoriteButton :movieId='movie.id' class="w-6 h-6"/>
                </div>
              </div>
              <div class='text-sm text-justify'>
                {{movie.description}}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>