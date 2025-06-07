from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import JSON

from .extensions import db

subscriptions = db.Table(
    "subscriptions",
    db.Column("follower_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("followed_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("time_followed", db.DateTime, default=datetime.now)
    )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    login = db.Column(db.String(32), unique=True, nullable=False)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_joined = db.Column(db.DateTime, default=datetime.now, nullable=False)
    avatar = db.Column(db.Integer, nullable=False)

    favorite_movies = db.relationship("Movie", secondary="favorites")
    watchlist = db.relationship("Movie", secondary="watchlist")
    review = db.relationship("Review", backref="author")
    following = db.relationship(
        "User",
        secondary=subscriptions,
        primaryjoin=(subscriptions.c.follower_id == id),
        secondaryjoin=(subscriptions.c.followed_id == id),
        backref="followers",
        lazy="dynamic"
    )

    
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "login": self.login,
            "username": self.username,
            "date_joined": self.date_joined.isoformat(),
            "last_joined": self.last_joined.isoformat(),
            "avatar": self.avatar
        }

    def set_password(self, password):
            self.password = generate_password_hash(password)

    def check_password(self, password):
            return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f"<User {self.login}>"

    def follow(self, user):
        if user not in self.following:
            self.following.append(user)

    def unfollow(self, user):
        if user in self.following:
            self.following.remove(user)

    def is_following(self, user):
        return self.following.filter(subscriptions.c.followed_id == user.id).count() > 0


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kinopoisk_id = db.Column(db.Integer, unique=True, nullable=False)
    imdb_id = db.Column(db.String(20), unique=True, nullable=True)
    name_ru = db.Column(db.String(256), nullable=False)
    name_en = db.Column(db.String(256), nullable=True)
    name_original = db.Column(db.String(256), nullable=True)
    countries = db.Column(db.String(256), nullable=True)
    genres = db.Column(db.String(256), nullable=True)
    rating_kinopoisk = db.Column(db.Float, nullable=True)
    rating_imdb = db.Column(db.Float, nullable=True)
    year = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    poster_url = db.Column(db.String(512), nullable=True)
    poster_url_preview = db.Column(db.String(512), nullable=True)
    cover_url = db.Column(db.String(512), nullable=True)
    logo_url = db.Column(db.String(512), nullable=True)
    description = db.Column(db.Text, nullable=True)
    rating_age_limits = db.Column(db.String(20), nullable=True)
    director_name_ru = db.Column(db.String(256), nullable=True)
    director_name_en = db.Column(db.String(256), nullable=True)
    director_poster_url = db.Column(db.String(512), nullable=True)


    def to_dict(self):
        return {
            "id": self.id,
            "kinopoiskId": self.kinopoisk_id,
            "imdbId": self.imdb_id,
            "nameRu": self.name_ru,
            "nameEn": self.name_en,
            "nameOriginal": self.name_original,
            "countries": self.countries,
            "genres": self.genres,
            "ratingKinopoisk": self.rating_kinopoisk,
            "ratingImdb": self.rating_imdb,
            "year": self.year,
            "type": self.type,
            "posterUrl": self.poster_url,
            "posterUrlPreview": self.poster_url_preview,
            "coverUrl": self.cover_url,
            "logoUrl": self.logo_url,
            "description": self.description,
            "ratingAgeLimits": self.rating_age_limits,
            "directorNameRu": self.director_name_ru,
            "directorNameEn": self.director_name_en,
            "directorPosterUrl": self.director_poster_url
        }

    def __repr__(self):
        return f"<Movie {self.name_ru} ({self.year})>"


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"), nullable=False)
    review_text = db.Column(db.Text, nullable=False)
    review_rating = db.Column(db.Float, nullable=False)
    review_date = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def __repr__(self):
        return f"Review = {self.user_id} movie = {self.movie_id}>"


favorites = db.Table(
    "favorites",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("movie_id", db.Integer, db.ForeignKey("movie.id"), primary_key=True),
    db.Column("date_added", db.DateTime, default=datetime.utcnow, nullable=False)
)


watchlist = db.Table(
    "watchlist",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("movie_id", db.Integer, db.ForeignKey("movie.id"), primary_key=True),
    db.Column("date_added", db.DateTime, default=datetime.utcnow, nullable=False)
)








