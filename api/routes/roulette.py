from flask import Blueprint, jsonify
import random
from flask_login import login_required, current_user

from ..models import Movie, User
roulette_bp = Blueprint("roulette", __name__, url_prefix="/api")

# выбирает рандомный фильм из всех
@roulette_bp.route("/roulette_all")
def roulette_all():
    movies = Movie.query.all()
    movie = random.choice(movies)
    return jsonify(movie.to_dict())

# выбирает рандомный фильм из списка избранных
@roulette_bp.route("/roulette_favorite")
@login_required
def roulette_favotite():
    movies = current_user.favorite_movies
    if not movies:
        return jsonify({"message": "У вас нет фильмов в избранном."})
    
    movie = random.choice(movies)
    return jsonify(movie.to_dict())

# # выбирает рандомный фильм из watchlist'а
@roulette_bp.route("/roulette_watchlist")
@login_required
def roulette_watchlist():
    movies = current_user.watchlist
    if not movies:
        return jsonify({"message": "У вас нет фильмов в watchlist."})
    movie = random.choice(movies)
    return jsonify(movie.to_dict())


@roulette_bp.route("/roulette_for_2/<int:id>")
@login_required
def roulette_for_2(id):
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

    if not movies:
        return jsonify({"message":"У вас нет общих фильмов"})
    
    rand_movie = random.choice(movies)
    return jsonify(rand_movie.to_dict())











