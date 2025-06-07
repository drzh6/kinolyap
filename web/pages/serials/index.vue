<template>
  <div class='flex items-center justify-center'>


  <div class="heart-wrapper" ref="wrapper">
    <button class="heart-btn" @click="handleClick">
      ❤️
    </button>
    <div class="heart-animation-container">
      <div
          v-for="(heart, index) in hearts"
          :key="heart.id"
          class="flying-heart"
          :style="{
          left: heart.left + 'px',
          top: heart.top + 'px',
          animationDelay: heart.delay + 's'
        }"
      >
        {{ heart.symbol }}
      </div>
    </div>
  </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const hearts = ref([])
const wrapper = ref(null)

function handleClick() {
  // Запускаем анимацию сразу, без запроса на сервер
  triggerAnimation()
}

function triggerAnimation() {
  const symbols = ['❤️', '❤️', '❤️']
  for (let i = 0; i < 3; i++) {
    const id = Date.now() + Math.random()
    const randomOffset = Math.random() * 40 - 20
    const delay = i * 0.15
    hearts.value.push({
      id,
      left: randomOffset,
      top: 0,
      symbol: symbols[i % symbols.length],
      delay
    })

    // Удаление после завершения анимации
    setTimeout(() => {
      hearts.value = hearts.value.filter(h => h.id !== id)
    }, 3000)
  }
}
</script>

<style scoped>
.heart-wrapper {
  position: relative;
  display: inline-block;
}

.heart-btn {
  background: none;
  border: none;
  font-size: 28px;
  cursor: pointer;
  position: relative;
  z-index: 2;
}

.heart-animation-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100px;
  height: 100px;
  pointer-events: none;
  z-index: 1;
}

.flying-heart {
  position: absolute;
  font-size: 24px;
  animation: flyUp 2s ease-out forwards;
  opacity: 0.9;
}

@keyframes flyUp {
  0% {
    opacity: 1;
    transform: translateY(0px) scale(1);
  }
  100% {
    opacity: 0;
    transform: translateY(-80px) scale(1.5);
  }
}
</style>
