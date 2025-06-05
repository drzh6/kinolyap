from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from datetime import datetime

from ..models import Movie, Review, User
from ..extensions import db

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

# Добавляет и удаляет фильм из избранного
@movie_bp.route("/add_remove_favorite/<int:movie_id>", methods=["POST"])
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

# Проверка добовлен ли в избранное
@movie_bp.route("/is_favorite/<int:movie_id>", methods=["GET"])
@login_required
def is_favorite(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    is_fav = movie in current_user.favorite_movies
    return jsonify({"favorite": is_fav})
    
# Выводит все избранные фильмы авторизированного юзера
@movie_bp.route("/favorites")
@login_required
def favorites():
    movies = current_user.favorite_movies
    result = [movie.to_dict() for movie in movies]
    return jsonify(result)

# Добавляет и удаляет фильм из вочлиста
@movie_bp.route("/add_remove_watchlist/<int:movie_id>", methods=["POST"])
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
@movie_bp.route("/is_watchlist/<int:movie_id>", methods=["GET"])
@login_required
def is_watchlisted(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    is_watchlisted = movie in current_user.watchlist
    return jsonify({"watchlist": is_watchlisted})


# Выводит все фильмы из watchlist'а юзера 
@movie_bp.route("/watchlist")
@login_required
def show_watchlist():
    movies = current_user.watchlist
    result = [movie.to_dict() for movie in movies]
    return jsonify(result)

# Выводит из бд все отзывы пользователей к определенному фильму
@movie_bp.route("/movie_reviews/<int:movie_id>")
def show_movie_reviews(movie_id):
    reviews = Review.query.filter_by(movie_id=movie_id).all()
    if not reviews:
        return jsonify({"message":"Пока отзывов нет"})
    result = []
    for review in reviews:
        result.append({
        "text": review.review_text,
        "rating": review.review_rating,
        "date_added": review.review_date,
        "author": review.author.username
        })
    return jsonify(result)

# Дает возможность написать отзыв к определенному фильму
@movie_bp.route("/add_review/<int:movie_id>", methods=["POST"])
def add_review(movie_id):
    existing_review = Review.query.filter_by(user_id=current_user.id, movie_id=movie_id).first()
    if existing_review:
        return jsonify({"message": "Вы уже оставили отзыв про этот фильм."})
    
    data = request.json
    text = data.get("text")
    rating = data.get("rating")
    review_date = datetime.utcnow()
    
    if not rating or not text:
        return jsonify({"message": "Вы не ввели данные."}), 400
    
    try:
        rating = float(rating)  
    except (ValueError, TypeError):
        return jsonify({"message": "Рейтинг должен быть числом."}), 400

    review = Review(
    user_id=current_user.id,
    movie_id=movie_id,
    review_text=text,
    review_rating=rating,
    review_date=review_date
    )

    db.session.add(review)
    db.session.commit()
    return jsonify({"message": "Отзыв оставлен"})

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
 













