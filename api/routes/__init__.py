from .auth import auth_bp
from .profile import profile_bp
from .movies import movies_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(movies_bp)