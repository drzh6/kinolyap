<script setup lang="ts">
import { reactive, ref } from 'vue'
import type { FormError, FormSubmitEvent } from '@nuxt/ui'

const apiUrl = 'http://localhost:5000/api'
const msg = ref('')
const msgType = ref<'success' | 'error' | ''>('')

const state = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  login: '',
  email: ''
})

const validate = (state: any): FormError[] => {
  const errors: FormError[] = []
  if (!state.username) errors.push({ name: 'username', message: 'Обязательное поле' })
  if (!state.login) errors.push({ name: 'login', message: 'Обязательное поле' })
  if (!state.email) errors.push({ name: 'email', message: 'Обязательное поле' })
  if (!state.password) errors.push({ name: 'password', message: 'Обязательное поле' })
  if (!state.confirmPassword) errors.push({ name: 'confirmPassword', message: 'Обязательное поле' })
  return errors
}

async function onSubmit(event: FormSubmitEvent<typeof state>) {
  msg.value = ''
  msgType.value = ''

  if (state.password && state.confirmPassword && state.password !== state.confirmPassword) {
    msg.value = 'Пароли не совпадают'
    msgType.value = 'error'
    return
  }

  try {
    const res = await fetch(`${apiUrl}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(event.data)
    })
    const data = await res.json()
    if (data.error) {
      msg.value = data.error
      msgType.value = 'error'
    } else {
      msg.value = data.message || 'Регистрация прошла успешно'
      msgType.value = 'success'
      state.username = ''
      state.login = ''
      state.email = ''
      state.password = ''
      state.confirmPassword = ''
    }
  } catch (e) {
    msg.value = 'Ошибка при регистрации'
    msgType.value = 'error'
  }
}
</script>

<template>
  <div>
    <h2 class="mb-4 text-xl font-semibold">Регистрация</h2>
    <NuxtForm
        @submit="onSubmit"
        :validate="validate"
        :state="state"
        class="max-w-[720px] flex flex-col space-y-8"
    >
      <NuxtInput v-model="state.username"
                 placeholder="Имя пользователя"
                 size="lg"
                 icon="tabler:user-square-rounded"
                 required
      />

      <NuxtInput v-model="state.login"
                 placeholder="Логин"
                 size="lg"
                 icon="tabler:user"
                 required
      />


      <NuxtInput v-model="state.email"
                 type="email"
                 placeholder="Email"
                 size="lg"
                 icon="tabler:mail"
                 required
      />


      <NuxtInput v-model="state.password"
                 type="password"
                 placeholder="Пароль"
                 size="lg"
                 icon="tabler:lock-password"
                 required
      />
      <NuxtInput v-model="state.confirmPassword"
                 type="password"
                 placeholder="Подтвердите пароль"
                 size="lg"
                 icon="tabler:lock-password"
                 required
      />

      <NuxtButton type="submit" block>
        Зарегистрироваться
      </NuxtButton>

      <div v-if="msg" :class="[
          msgType === 'success' ? 'text-success' : 'text-error',
          'text-center mt-2'
        ]" >{{ msg }}</div>
    </NuxtForm>
  </div>
</template>
