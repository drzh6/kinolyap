// stores/profileStore.ts
import { defineStore } from "pinia";
import { ref } from "vue";

export const useProfileStore = defineStore("profile", () => {
    const profile = ref<null | {
        username: string;
        login: string;
        email: string;
        date_joined: string;
    }>(null);

    const loading = ref(false);
    const error = ref("");

    async function fetchProfile() {
        loading.value = true;
        error.value = "";

        try {
            const res = await fetch("http://localhost:5000/api/profile", {
                credentials: "include",
            });

            if (!res.ok) {
                throw new Error("Ошибка получения профиля");
            }

            profile.value = await res.json();
        } catch (err: any) {
            error.value = err.message || "Неизвестная ошибка";
            profile.value = null;
        } finally {
            loading.value = false;
        }
    }

    async function updateProfile(data: Partial<{ username: string; password: string }>) {
        loading.value = true;
        error.value = "";

        try {
            const res = await fetch("http://localhost:5000/api/profile_update", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                credentials: "include",
                body: JSON.stringify(data),
            });

            if (!res.ok) {
                throw new Error("Не удалось обновить профиль");
            }

            const updated = await res.json();
            profile.value = { ...profile.value, ...updated };
        } catch (err: any) {
            error.value = err.message || "Ошибка при обновлении профиля";
        } finally {
            loading.value = false;
        }
    }

    return {
        profile,
        loading,
        error,
        fetchProfile,
        updateProfile,
    };
});
