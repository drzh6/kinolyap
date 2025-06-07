from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from datetime import datetime

from ...models import Movie, Review, User
from ...extensions import db

movie_bp = Blueprint("movie", __name__, url_prefix="/api")

# Выводит все фильмы из БД
@movie_bp.route("/movies")
def movies():
    movies = Movie.query.all()
    return jsonify(
        [movie.to_dict()
        for movie in movies]
        )

# Выводит определенный фильм
@movie_bp.route("/movie/<int:movie_id>")
def exact_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    return jsonify(movie.to_dict())

# показывает общие фильмы из watchlist'а
@movie_bp.route("/match_films/<int:id>")
@login_required
def match_films(id):
    user = User.query.get_or_404(id)
    user_movies = user.watchlist
    my_movies = current_user.watchlist
    movies = []

    if not user_movies:
        return jsonify({"message":"У пользователя нет фильмов"})
    if not my_movies:
        return jsonify({"message":"У вас нет фильмов"})
    
    for element in user_movies:
        if element in my_movies:
            movies.append(element)

    return jsonify([movie.to_dict() for movie in movies])
 













