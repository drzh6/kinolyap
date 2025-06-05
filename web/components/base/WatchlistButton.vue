<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'

const isWatchlist = ref(false)
// Флаг, что ответ с is_watchlist уже пришёл
const isFetched = ref(false)

const props = defineProps({
  movieId: Number
})

defineOptions({
  inheritAttrs: false
})


const fetchIsWatchlist = async () => {
  try {
    const res = await axios.get(`http://localhost:5000/api/is_watchlist/${props.movieId}`, { withCredentials: true })
    isWatchlist.value = res.data.watchlist;
  }
  catch (error) {
    console.error('Failed to fetch the watchlist!', error);
  }
  finally {
    // Независимо от успеха/ошибки ставим флаг, что загрузка завершена
    isFetched.value = true
  }
}

const fetchWatchlist = async () => {
  try {
    const res = await axios.post(`http://localhost:5000/api/add_remove_watchlist/${props.movieId}`, {}, { withCredentials: true })
    if (res.data.status === 'added') {
      isWatchlist.value = true
    } else if (res.data.status === 'removed') {
      isWatchlist.value = false
    }
  }
  catch (error) {
    console.error('Failed to fetch the watchlist!', error);
  }
}

onMounted(() => {
  fetchIsWatchlist()
})
</script>

<template>
  <div v-if='isFetched'>
  <label class="cont">
    <input type="checkbox" v-model='isWatchlist' @change="fetchWatchlist()" />
    <svg :class='{ watchlist: isWatchlist }' v-bind="$attrs" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <g fill="none" stroke="#666" >
        <path d="M3 13c3.6-8 14.4-8 18 0" />
        <path fill="#666" d="M12 17a3 3 0 1 1 0-6a3 3 0 0 1 0 6" />
      </g>
    </svg>
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
  fill: #666
}

.cont svg:hover {
  transform: scale(1.1);
}

svg.watchlist path {
  stroke: var(--ui-warning);
}
svg.watchlist path:last-child {
  fill: var(--ui-warning);
}
</style>