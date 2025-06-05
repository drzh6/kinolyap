#Обновляет фильмы если поменять что-то в джсон файле то он обновит данные в бд(без дубликатов)

import json

from app import app
from models import Movie
from extensions import db


with app.app_context():
    with open("movies.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    for item in data:
        existing = db.session.get(Movie, item["id"])
        if existing:
            existing.title = item["title"]
            existing.description = item["description"]
            existing.genre = ", ".join(item["genre"])
            existing.year = item["year"]
            existing.rating = item["rating"]
            existing.poster_url = item["poster_url"]
            existing.director = item["director"]
        else:
            movie = Movie(
                id=item["id"],
                title=item["title"],
                description=item["description"],
                genre=", ".join(item["genre"]),
                year=item["year"],
                rating=item["rating"],
                poster_url=item["poster_url"],
                director=item["director"]
            )
            db.session.add(movie)
    
    db.session.commit()
    print("✅ Фильмы успешно загружены в базу данных.")