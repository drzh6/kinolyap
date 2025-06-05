import { defineStore } from 'pinia'
import { ref } from 'vue'

interface Movie {
    id: number
    title: string
    year: number
    rating: number
    poster_url: string
    director: string
}

export const useMovieStore = defineStore('movieStore', () => {
    const movies = ref<Movie[]>([])
    const loaded = ref(false)

    async function fetchMovies() {
        if (loaded.value) return
        const res = await fetch('http://localhost:5000/api/movies')
        movies.value = await res.json()
        loaded.value = true
    }

    return { movies, loaded, fetchMovies }
})