from .auth import auth_bp
from .profile import profile_bp
from .movie.roulette import roulette_bp
from .user import user_bp
from .movie.movie import movie_bp
from .subscriptions import subs_bp
from .movie.favorite import favorite_bp
from .movie.watchlist import watchlist_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(movie_bp)
    app.register_blueprint(roulette_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(subs_bp)
    app.register_blueprint(favorite_bp)
    app.register_blueprint(watchlist_bp)