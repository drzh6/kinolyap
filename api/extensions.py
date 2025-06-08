from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_caching import Cache


login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
cache = Cache()
