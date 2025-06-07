import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

interface Movie {
    id: number
    nameRu: string
    year: number
    ratingKinopoisk: number
    posterUrl: string
    directorNameEn: string
    description: string
}

export const useMovieStore = defineStore('movieStore', () => {
    const movies = ref<Movie[]>([])
    const loaded = ref(false)

    async function fetchMovies() {
        if (loaded.value) return
        const res = await axios.get('http://localhost:5000/api/movies', {
            withCredentials: true
        })
        movies.value = await res.data
        loaded.value = true
    }

    return { movies, loaded, fetchMovies }
})