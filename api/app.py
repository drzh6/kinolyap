import os
from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS

from .models import User
from .extensions import db, migrate, login_manager
from .routes import register_blueprints


app = Flask(__name__)

load_dotenv()
register_blueprints(app)

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
db.init_app(app)
migrate.init_app(app, db)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


if __name__ == "__main__":
    app.run(debug=True)