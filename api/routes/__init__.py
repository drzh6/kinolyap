from .auth import auth_bp
from .profile import profile_bp
from .movie import movie_bp
from .roulette import roulette_bp
from .user import user_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(movie_bp)
    app.register_blueprint(roulette_bp)
    app.register_blueprint(user_bp)