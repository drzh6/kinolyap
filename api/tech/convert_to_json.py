#получает на вход txt и конвертирует данные в json (фильмы)

import json


movies = []

with open("top_movies.txt", "r", encoding="utf-8") as file:
    content = file.read()

# Разделение по пустым строкам между фильмами
elements = content.strip().split("\n\n")

for element in elements:
    movie = {}
    lines = element.strip().split("\n")
    for line in lines:
        if ':' in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()

            # Приведение типов
            if key == "id":
                movie[key] = int(value)
            elif key == "year":
                movie[key] = int(value)
            elif key == "rating":
                movie[key] = float(value)
            elif key == "genre":
                movie[key] = [g.strip() for g in value.split(",")]
            else:
                movie[key] = value
    movies.append(movie)

# Сохраняем в JSON-файл (менять)
with open("movies.json", "w", encoding="utf-8") as file:
    json.dump(movies, file, ensure_ascii=False, indent=4)

print("Фильмы успешно сохранены в json")