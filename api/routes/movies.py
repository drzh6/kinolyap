from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from datetime import datetime
from random import random
from sqlalchemy import insert

from ..models import Movie, Review, favorites
from ..extensions import db

movies_bp = Blueprint("movies", __name__, url_prefix="/api")


@movies_bp.route("/movies")
def movies():
    movies = Movie.query.all()
    return jsonify([{
        "id": movie.id,
        "title": movie.title,
        "description": movie.description,
        "genre": movie.genre,
        "year": movie.year,
        "rating": movie.rating,
        "poster_url": movie.poster_url,
        "director": movie.director
    }
        for movie in movies
    ])


@movies_bp.route("/add_favorite/<int:movie_id>", methods=["POST"])
@login_required
def add_favorite(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if movie in current_user.favorite_movie:
        return jsonify({"message": "Фильм уже добавлен"})
    
    stmt = insert(favorites).values(
        user_id=current_user.id,
        movie_id=movie.id,
        date_added=datetime.now()
    )
    db.session.execute(stmt)
    db.session.commit()
    return jsonify({"message":"Фильм добавлен в избранное"})
    


@movies_bp.route("/movie/<int:movie_id>", methods=["POST"])
def exact_movie(movie_id):
    if current_user.is_authenticated:
        existing_review = Review.query.filter_by(user_id=current_user.id, movie_id=movie_id).first()
        if existing_review:
            return jsonify({"message": "Вы уже оставили отзыв."})
        
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
        
        rating = float(rating)

        review = Review(
        user_id=current_user.id,
        movie_id=movie_id,
        review_text=text,
        review_rating=rating,
        review_date=review_date
        )

        db.session.add(review)
        db.session.commit()
        return jsonify({"message": "сохранено"})
    
    movie = Movie.query.get_or_404(movie_id)

    # return jsonify({
    #     "id": movie.id,
    #     "title": movie.title,
    #     "description": movie.description,
    #     "genre": movie.genre,
    #     "year": movie.year,
    #     "rating": movie.rating,
    #     "poster_url": movie.poster_url,
    #     "director": movie.director 
    # })


@movies_bp.route("reviews")
@login_required
def user_reviews():

    return


@movies_bp.route("/roulette_all")
def roulette_all():
    movies = Movie.query.all()
    rand_movie = random.choice(movies)
    return jsonify({
        "id": rand_movie.id,
        "title": rand_movie.title,
        "description": rand_movie.description,
        "genre": rand_movie.genre,
        "year": rand_movie.year,
        "rating": rand_movie.rating,
        "poster_url": rand_movie.poster_url,
        "director": rand_movie.director 
    })


@movies_bp.route("/roulette_favorite")
@login_required
def roulette_favotite():
    movies = current_user.favorite_movies.all()
    if not movies:
        return jsonify({"message": "У вас нет фильмов в избранном."}), 404
    
    movie = random.choice(movies)
    return jsonify({
        "id": movie.id,
        "title": movie.title,
        "description": movie.description,
        "genre": movie.genre,
        "year": movie.year,
        "rating": movie.rating,
        "poster_url": movie.poster_url,
        "director": movie.director 
    })


@movies_bp.route("/favorites", methods=["POST"])
@login_required
def favorites():
    favorites_movies = current_user.favorite_movies
    result = [movie.to_dict() for movie in favorites_movies]
    return jsonify(result)


@movies_bp.route("/api/unfavorite/<int:movie_id>", methods=["POST"])
@login_required
def unfavorite(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if movie in current_user.favorite_movies:
        current_user.favorite_movies.remove(movie)
        db.session.commit()
    return jsonify({"message": "Фильм удален из избранных"})





