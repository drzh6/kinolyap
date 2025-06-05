<template>
  <div class="min-h-screen bg-background text-text p-layout">
    <button
        @click="toggleColorMode"
        class="px-4 py-2 rounded text-green-500 bg-neutral mt-4"
    >
      Сменить тему
    </button>
  </div>
</template>

<script setup>
const colorMode = useColorMode()

function toggleColorMode() {
  colorMode.preference = colorMode.preference === 'dark' ? 'light' : 'dark'
}
</script>
