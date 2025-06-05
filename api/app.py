import os
import random
from flask import Flask, request, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_cors import CORS

from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, current_user, login_required, logout_user

from .models import User, Movie, Review
from .extensions import db, migrate, login_manager
# from .routes import register_blueprints

load_dotenv()

app = Flask(__name__)

# register_blueprints(app)

app.config.update(
    SECRET_KEY=os.getenv("FLASK_SECRET_KEY") or "19d8ebe35348bdc027d1f8ebac368353afdd4e47e4cf138da581e437595deaf84dd504974e5a8df2d86c1673420d27fc8d47fc87c01a603d4c6c4d2fbbf288ad",
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=False      # ← включите True после перехода на https
)

app.config["CORS_SUPPORTS_CREDENTIALS"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

CORS(
    app,
    supports_credentials=True,
    resources={r"/api/*": {"origins": "http://localhost:3000"}}
)

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

db.init_app(app)
migrate.init_app(app, db)

@app.route("/api/register", methods=["POST"])
def register():
    if current_user.is_authenticated:
        return jsonify({"error": "Вы уже авторизованы"}), 400

    data = request.json

    if not data:
        return jsonify({"message": "Нет данных"}), 400

    email = (data.get("email") or "").strip()
    password = (data.get("password") or "").strip()
    login = (data.get("login") or "").strip()
    username = (data.get("username") or "").strip()

    if not all([email, password, login, username]):
        return jsonify({"message": "Все поля обязательны"}), 400

    existing_email = User.query.filter_by(email=email).first()
    existing_login = User.query.filter_by(login=login).first()

    if existing_email:
        return jsonify({"message": "такой Email уже зарегистрирован"}), 409
    if existing_login:
        return jsonify({"message": "такой Login уже занят"}), 409

    hashed_password = generate_password_hash(password)
    user = User(email=email,username=username,login=login,password=hashed_password)
    db.session.add(user)
    db.session.commit()

    login_user(user)
    return jsonify({"message": "успешная регистрация"}), 201


@app.route("/api/login", methods=["POST"])
def login():

    data = request.get_json() or {}
    login = data.get("login", "").strip()
    password = data.get("password", "")

    if not login or not password:
        return jsonify({"error": "Логин и пароль обязательны"}), 400

    user = User.query.filter_by(login=login).first()

    if user is None or not check_password_hash(user.password, password):
        return jsonify({"error": "Неверный логин или пароль"}), 401

    login_user(user)

    return jsonify({
        "message": "Успешно",
        "user": {
            "id": user.id,
            "login": user.login,
            "username": user.username,
            "email": user.email
        }
    }), 200


@app.route("/api/profile", methods=['GET'])
@login_required
def profile():
    return jsonify({
        "id": current_user.id,
        "login": current_user.login,
        "username": current_user.username,
        "email": current_user.email,
        "date_joined": current_user.date_joined.isoformat()
    })

@app.route("/api/me", methods=["GET"])
@login_required
def get_current_user():
    if not current_user.is_authenticated:
        return jsonify({"error": "Не авторизован"}), 401

    user = current_user
    return jsonify({
        "user": {
            "id": user.id,
            "login": user.login,
            "username": user.username,
            "email": user.email
        }
    }), 200


@app.route("/api/profile_change", methods=["POST"])
@login_required
def profile_change():
    data = request.json
    username = data.get("name")
    return jsonify({   
    })


@app.route("/api/logout")
@login_required
def logout_route():
    logout_user()
    return jsonify({"message": "вы вышли из аккаунта"})


@app.route("/api/delete")
@login_required
def delete_profile():
    db.session.delete(current_user)
    db.session.commit()
    logout_user()
    return jsonify({"message": "Профиль успешно удален"}), 200


@app.route("/api/movies")
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


@app.route("/api/roulette/favorite")
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


@app.route("/api/roulette/all")
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

@app.route("/api/favorites")
@login_required
def favorites():
    favorites_movies = current_user.favorite_movies
    result = [movie.to_dict() for movie in favorites_movies]
    return jsonify(result)


# Выводит все фильмы из watchlist'а юзера
@app.route("/api/watchlist")
@login_required
def show_watchlist():
    watch_movies = current_user.watchlist
    result = [movie.to_dict() for movie in watch_movies]
    return jsonify(result)


@app.route("/api/add_remove_favorite/<int:movie_id>", methods=["POST"])
@login_required
def add_favorite(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if movie in current_user.favorite_movies:
        current_user.favorite_movies.remove(movie)
        db.session.commit()
        return jsonify({"message": "Фильм удален из избранного", "status": "removed"})
    current_user.favorite_movies.append(movie)
    db.session.commit()
    return jsonify({"message":"Фильм добавлен в избранное", "status": "added"})


# Проверка добовлен ли в избранное
@app.route("/api/is_favorite/<int:movie_id>", methods=["GET"])
@login_required
def is_favorite(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    is_fav = movie in current_user.favorite_movies
    return({"favorite": is_fav})


@app.route("/api/add_remove_watchlist/<int:movie_id>", methods=["POST"])
@login_required
def add_remove_watchlist(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if movie in current_user.watchlist:
        current_user.watchlist.remove(movie)
        db.session.commit()
        return jsonify({"message": "Фильм удален из списка", "status": "removed"})
    current_user.watchlist.append(movie)
    db.session.commit()
    return jsonify({"message": "Фильм добавлен в список", "status": "added"})

@app.route("/api/is_watchlist/<int:movie_id>", methods=["GET"])
@login_required
def is_watchlisted(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    is_watchlisted = movie in current_user.watchlist
    return({"watchlist": is_watchlisted})


# @app.route("api/reviews")
# @login_required
# def reviews():
#     reviews = Review.query.filter_by(user_id=current_user.id).all()
#     return jsonify({
#         "text": reviews.review_text,
#         "rating": reviews.review_rating
#     })


# @app.route("api/add_review<int:movie_id>")
# @login_required
# def add_review(movie_id):
#     data = request.json
#     text = data.get("text")
#     rating = int(data.get("rating"))
#     review = Review(
#         user_id=current_user.id,
#         movie_id=movie.id,
#         review_text=text,
#         review_rating=rating
#         )
#     db.session.add(review)
#     db.session.commit()
#     return jsonify({"message": "рецензия оставлена"})


if __name__ == "__main__":
    app.run(debug=True)