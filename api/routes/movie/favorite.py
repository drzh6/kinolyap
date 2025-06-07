from flask import Blueprint, jsonify
from flask_login import login_required, current_user

from ...models import Movie
from ...extensions import db

favorite_bp = Blueprint("favorite", __name__, url_prefix="/api")


# Добавляет и удаляет фильм из избранного
@favorite_bp.route("/add_remove_favorite/<int:movie_id>")
@login_required
def add_favorite(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if movie in current_user.favorite_movies:
        current_user.favorite_movies.remove(movie)
        db.session.commit()
        return jsonify({"message": "Фильм удален из избранного"})
    
    current_user.favorite_movies.append(movie)
    db.session.commit()
    return jsonify({"message":"Фильм добавлен в избранное"})

# Проверка добовлен ли в избранное!!!
@favorite_bp.route("/is_favorite/<int:movie_id>", methods=["GET"])
@login_required
def is_favorite(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    is_fav = movie in current_user.favorite_movies
    return({"favorite": is_fav})
    
# Выводит все избранные фильмы авторизированного юзера
@favorite_bp.route("/favorites", methods=["POST"])
@login_required
def favorites():
    movies = current_user.favorite_movies
    result = [movie.to_dict() for movie in movies]
    return jsonify(result)
