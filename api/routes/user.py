# отображение профилей других пользователей

from flask import Blueprint, jsonify
from flask_login import login_required

from ..models import User

user_bp = Blueprint("user", __name__, url_prefix="/api")

# Выгружает данные об юзере
@user_bp.route("/user_profile_info/<int:id>")
@login_required
def show_user_profile(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())

# Выгружает избранные фильмы опеределенного юзера
@user_bp.route("/user_profile_favorited/<int:id>")
@login_required
def show_user_favorited(id):
    user = User.query.get_or_404(id)
    movies = user.favorite_movies
    return jsonify([movie.to_dict() for movie in movies])

# Выгружает фильмы из watchlist'а опеределенного юзера
@user_bp.route("/user_profile_watchlist/<int:id>")
@login_required
def how_user_watchlist(id):
    user = User.query.get_or_404(id)
    movies = user.watchlist
    return jsonify([movie.to_dict() for movie in movies])








