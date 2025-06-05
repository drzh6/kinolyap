<!-- layouts/default.vue -->

<script setup lang="ts">
import { onMounted } from "vue";
import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore();

onMounted(async () => {
  await auth.restore();
});
</script>

<template>
    <div class="flex flex-col min-h-screen bg-background text-text">
      <div class='w-full max-w-[1420px] mx-auto flex flex-col flex-1 px-4'>
        <LayoutHeader />
        <main class="flex flex-1 justify-center pt-20">
          <slot />
        </main>
        <LayoutFooter />
      </div>
    </div>
</template>


