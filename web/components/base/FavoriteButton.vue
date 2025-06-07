<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'

const isFavorite = ref(false)
const isFetched = ref(false)

const props = defineProps({
  movieId: Number
})

defineOptions({
  inheritAttrs: false
})

const fetchIsFavorite = async () => {
  try {
    const res = await axios.get(`http://localhost:5000/api/is_favorite/${props.movieId}`, { withCredentials: true });
    isFavorite.value = res.data.favorite;
  }
  catch (error) {
    console.error(error)
  }
  finally {
    // Независимо от успеха/ошибки ставим флаг, что загрузка завершена
    isFetched.value = true
  }
}

const fetchFavorite = async () => {
  try {
    const res = await axios.get(`http://localhost:5000/api/add_remove_favorite/${props.movieId}`, { withCredentials: true });
    if (res.data.status === 'added') {
      isFavorite.value = true
    } else if (res.data.status === 'removed') {
      isFavorite.value = false
    }
  }
  catch (error) {
    console.error('Failed to fetch the favorite!', error);
  }
}

onMounted(() => {
  fetchIsFavorite()
})

</script>


<template>
  <div v-if='isFetched'>
  <label class="cont">
    <input type="checkbox" v-model='isFavorite' @change="fetchFavorite()" />
    <svg :class='{favorite: isFavorite}' v-bind="$attrs" id="Layer_1" version="1.0" viewBox="0 0 24 24" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><path d="M16.4,4C14.6,4,13,4.9,12,6.3C11,4.9,9.4,4,7.6,4C4.5,4,2,6.5,2,9.6C2,14,12,22,12,22s10-8,10-12.4C22,6.5,19.5,4,16.4,4z"></path></svg>
  </label>
  </div>
  <div v-else>
    <NuxtSkeleton v-bind="$attrs" class="rounded-full bg-white/10 backdrop-blur-sm" />
  </div>
</template>

<style scoped>
.cont input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

.cont {
  display: block;
  position: relative;
  cursor: pointer;
  user-select: none;
}

.cont svg {
  position: relative;
  top: 0;
  left: 0;
  transition: all 0.3s;
  fill: #666;
}

.cont svg:hover {
  transform: scale(1.1);
}

svg.favorite {
  fill: #E3474F;
}
</style>