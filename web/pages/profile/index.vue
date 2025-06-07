<script setup lang="ts">
import { onMounted } from 'vue'
import { useProfileStore } from "@/stores/profileStore";
import { useAuthStore } from '@/stores/auth'

const profileStore = useProfileStore();
const auth = useAuthStore();

definePageMeta({
  middleware: ['auth']
})

onMounted(() => {
  profileStore.fetchProfile();
});

const avatars = [
  'fxemoji:wolfface',
  'fxemoji:pandaface',
  'fxemoji:hampster',
  'fxemoji:koala',
  'fxemoji:tiger',
  'fxemoji:foxwry',
  'fxemoji:cat',
  'fxemoji:bear',
  'fxemoji:monkeyface',
  'fxemoji:chicken',
  'fxemoji:horseface',
  'fxemoji:bunny',
  'fxemoji:boar',
  'fxemoji:dog'
];

</script>

<template>
  <div v-if="profileStore.profile">
    <h1>Добро пожаловать, {{ profileStore.profile.username }}</h1>
    <p>Дата регистрации: {{ profileStore.profile.date_joined }}</p>
    <p class='mb-4'>Email: {{ profileStore.profile.email }}</p>
    <NuxtButton @click='auth.logout()' class='w-20 h-8 text-text flex justify-center'>Выйти</NuxtButton>
  </div>
</template>

<style scoped>
</style>
