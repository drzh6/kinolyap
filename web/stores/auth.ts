// stores/auth.ts

import { defineStore } from "pinia";
import { ref } from "vue";
import { useRouter } from "vue-router";

export const useAuthStore = defineStore("auth", () => {
    const user = ref<null | { id: number; login: string; username: string; email: string }>(null);

    const loadingUser = ref(false);
    const initialized = ref(false);

    const router = useRouter();
    const loading = ref(false);
    const error = ref("");

    function isLoggedIn() {
        return Boolean(user.value);
    }

    // 1) Проверяем session → /api/me
    async function restore() {
        if (initialized.value) return;

        const cached = localStorage.getItem("auth_user");

        if (cached) {
            try {
                user.value = JSON.parse(cached);
                initialized.value = true;
                return;
            } catch {
                // если повреждён
                localStorage.removeItem("auth_user");
            }
        }

        loadingUser.value = true;
        try {
            const res = await fetch("http://localhost:5000/api/me", {
                credentials: "include",  // ← здесь важно
            });
            if (res.ok) {
                const data = await res.json();
                user.value = data.user;
                localStorage.setItem("auth_user", JSON.stringify(data.user)); // кешируем
            } else {
                user.value = null;
                localStorage.removeItem("auth_user");
            }
        } catch {
            user.value = null;
            localStorage.removeItem("auth_user");
        } finally {
            initialized.value = true;
            loadingUser.value = false;
        }
    }

    // 2) POST /api/login
    async function login(loginVal: string, password: string) {
        loading.value = true;
        error.value = "";
        try {
            const res = await fetch("http://localhost:5000/api/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                credentials: "include",  // ← здесь тоже
                body: JSON.stringify({ login: loginVal, password }),
            });

            const data = await res.json();

            if (!res.ok) {
                error.value = data.error || "Неизвестная ошибка входа";
                loading.value = false;
                return false;
            }

            user.value = data.user;
            localStorage.setItem("auth_user", JSON.stringify(data.user)); // сохраняем
            await router.push("/profile");
            return true;
        } catch (e) {
            console.error(e);
            error.value = "Ошибка связи с сервером";
            return false;
        } finally {
            loading.value = false;
        }
    }

    // 3) GET /api/logout
    async function logout() {
        try {
            await fetch("http://localhost:5000/api/logout", {
                method: "GET",
                credentials: "include",
            });
        } catch {
            // даже если не дошло до сервера, очищаем локально
        } finally {
            user.value = null;
            localStorage.removeItem("auth_user");
            await router.push("/");
        }
    }

    return {
        user,
        loadingUser,
        initialized,
        loading,
        error,
        isLoggedIn,
        restore,
        login,
        logout,
    };
});
