<!-- pages/users/[id].vue -->
<script setup lang="ts">
import axios from "axios"
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute();
const loading = ref(true);

const publicProfile = ref();
const id = route.params.id;

const fetchUserProfile = async () => {
  try {
    const res = await axios.get(`http://localhost:5000/api/user_profile_info/${id}`, { withCredentials: true })
    publicProfile.value = await res.data
  }
  catch (error) {
    console.error(error)
  }
  finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchUserProfile()
})
</script>

<template>
  <div v-if="loading">
    <p>Загрузка профиля...</p>
  </div>

  <div v-else-if="publicProfile">
    <h1>{{ publicProfile.username }}</h1>


    <p>Дата регистрации: {{ new Date(publicProfile.date_joined).toLocaleDateString() }}</p>


  </div>
  <div v-else>
    <p>Пользователь не найден.</p>
  </div>
</template>
