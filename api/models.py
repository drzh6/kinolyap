from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from .extensions import db

subscriptions = db.Table(
    "subscriptions",
    db.Column("follower_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("fillowed_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
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

    favorite_movies = db.relationship("Movie", secondary="favorites")
    watchlist = db.relationship("Movie", secondary="watchlist")
    review = db.relationship("Review", backref="author")
    following = db.relationship(
        "User",
        secondary=subscriptions,
        primaryjoin=(subscriptions.c.follower_id == id),
        secondaryjoin=(subscriptions.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "login": self.login,
            "username": self.username,
            "date_joined": self.date_joined.isoformat(),
            "last_joined": self.last_joined.isoformat()
        }

    def set_password(self, password):
            self.password = generate_password_hash(password)

    def check_password(self, password):
            return check_password_hash(self.password, password)
    def __repr__(self):

        return f"<User {self.login}>"


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256),  nullable=False)
    description = db.Column(db.Text, nullable=True)
    genre = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    poster_url = db.Column(db.String(256))
    director = db.Column(db.String(100), nullable=False)


    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "genre": self.genre,
            "year": self.year,
            "rating": self.rating,
            "poster_url": self.poster_url,
            "director": self.director
        }
    
    def __repr__(self):
        return f"<Movie {self.title}>"


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








