from flask import Blueprint, jsonify
from flask_login import login_required, current_user

from ...models import Movie
from ...extensions import db


watchlist_bp = Blueprint("watchlist", __name__, url_prefix="/api")


# Добавляет и удаляет фильм из вочлиста
@watchlist_bp.route("/add_remove_watchlist/<int:movie_id>")
@login_required
def add_remove_watchlist(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if movie in current_user.watchlist:
        current_user.watchlist.remove(movie)
        db.session.commit()
        return jsonify({"message": "Фильм удален из списка"})
    current_user.watchlist.append(movie)
    db.session.commit()
    return jsonify({"message": "Фильм добавлен в список"})

# Проверка добовлен ли в watchlist
@watchlist_bp.route("/is_watchlist/<int:movie_id>", methods=["GET"])
@login_required
def is_watchlisted(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    is_watchlisted = movie in current_user.watchlist
    return({"watchlist": is_watchlisted})

# Выводит все фильмы из watchlist'а юзера 
@watchlist_bp.route("/watchlist")
@login_required
def show_watchlist():
    movies = current_user.watchlist
    result = [movie.to_dict() for movie in movies]
    return jsonify(result)

