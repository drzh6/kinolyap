// middleware/auth.ts
import { useAuthStore } from '~/stores/auth'

export default defineNuxtRouteMiddleware(async (to) => {
    const auth = useAuthStore()

    // Проверяем, что код выполняется на клиенте
    if (process.client) {
        if (!auth.initialized) {
            await auth.restore()
        }

        if (!auth.isLoggedIn()) {
            return navigateTo('/')
        }
    }
})
