import requests
import time

API_KEY = "6421cb9c6e57208365ada0a36a6ac516"
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_URL = "https://image.tmdb.org/t/p/w500"
LANGUAGE = "ru-RU"

# Получение словаря жанров
def get_genres():
    url = f"{BASE_URL}/genre/movie/list"
    params = {"api_key": API_KEY, "language": LANGUAGE}
    res = requests.get(url, params=params)
    genres_data = res.json().get("genres", [])
    return {genre["id"]: genre["name"] for genre in genres_data}

# Получение режиссёра по ID фильма
def get_director(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/credits"
    params = {"api_key": API_KEY, "language": LANGUAGE}
    res = requests.get(url, params=params)
    crew = res.json().get("crew", [])
    for person in crew:
        if person.get("job") == "Director":
            return person.get("name")
    return "Неизвестен"

# Получение топ-500 фильмов
def fetch_top_movies():
    genre_map = get_genres()
    counter = 1

    with open("top_movies.txt", "w", encoding="utf-8") as f:
        for page in range(1, 26):  # 25 страниц × 20 фильмов = 500
            print(f"Загрузка страницы {page}...")
            url = f"{BASE_URL}/movie/top_rated"
            params = {"api_key": API_KEY, "language": LANGUAGE, "page": page}
            res = requests.get(url, params=params)
            res.raise_for_status()
            movies = res.json().get("results", [])

            for movie in movies:
                title = movie.get("title")
                description = movie.get("overview", "")
                genre_ids = movie.get("genre_ids", [])
                genre_names = [genre_map.get(gid, "Неизвестно") for gid in genre_ids]
                genre = ", ".join(genre_names)
                year = movie.get("release_date", "")[:4]
                rating = movie.get("vote_average", 0)
                poster_path = movie.get("poster_path")
                poster_url = IMAGE_URL + poster_path if poster_path else "Нет постера"

                try:
                    director = get_director(movie.get("id"))
                    time.sleep(0.3)  # Задержка для API-лимитов
                except:
                    director = "Ошибка при получении режиссёра"

                f.write(f"id: {counter}\n")
                f.write(f"title: {title}\n")
                f.write(f"description: {description}\n")
                f.write(f"genre: {genre}\n")
                f.write(f"year: {year}\n")
                f.write(f"rating: {rating}\n")
                f.write(f"poster_url: {poster_url}\n")
                f.write(f"director: {director}\n")
                f.write("\n")

                counter += 1

    print(f"✅ Сохранено {counter - 1} фильмов в файл top_movies.txt")

if __name__ == "__main__":
    try:
        fetch_top_movies()
    except Exception as e:
        print(f"❌ Ошибка: {e}")
