<script setup lang="ts">
import Logo from "@/assets/images/logo.svg";
import DropdownMenuLogin from "@/components/base/DropdownMenuLogin.vue";
import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore();
</script>

<template>
  <header class="fixed top-0 left-0 w-full h-20 bg-background/70 backdrop-blur-sm z-50">
    <div class="mx-auto w-full max-w-[1420px] h-full px-4">

      <nav class="relative flex items-center justify-center h-full">
        <!-- Логотип (cлева) -->
        <div class="absolute left-0 flex items-center">
          <NuxtLink to="/" class="flex items-center space-x-2">
            <Logo class="w-12 h-auto fill-primary" />
            <span class="font-extrabold text-lg text-text">KINOLYAP</span>
          </NuxtLink>
        </div>

        <!-- Навигация (по центру) -->
        <ul class="flex space-x-16 font-medium text-base text-text">
          <li><NuxtLink to="/movies">Фильмы</NuxtLink></li>
          <li><NuxtLink to="/serials">Сериалы</NuxtLink></li>
          <li><NuxtLink to="/favorites">Избранное</NuxtLink></li>
          <li><NuxtLink to="/watchlist">Watchlist</NuxtLink></li>
        </ul>

        <!-- Справа: Вход/Выход -->
        <div class='absolute right-0 flex items-center'>

          <div v-if="!auth.initialized">
            <NuxtSkeleton class="h-10 w-[127px] bg-white/10 backdrop-blur-sm" />
          </div>

          <div v-else>
            <template v-if='auth.isLoggedIn()'>
              <NuxtLink to='/profile'>
                  <NuxtButton variant="ghost" size="xl" color='text' icon="tabler:user">Профиль</NuxtButton>
              </NuxtLink>
            </template>
            <template v-else>
              <DropdownMenuLogin />
            </template>
          </div>

        </div>
      </nav>
    </div>
  </header>
</template>
