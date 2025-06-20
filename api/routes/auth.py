from flask import Blueprint, request, jsonify, redirect
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from ..extensions import db
from ..models import User


auth_bp = Blueprint("auth", __name__, url_prefix="/api")


@auth_bp.route("/register", methods=["POST"])
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
    avatar = (data.get("avatar"))

    if not all([email, password, login, username]):
        return jsonify({"message": "Все поля обязательны"}), 400

    existing_email = User.query.filter_by(email=email).first()
    existing_login = User.query.filter_by(login=login).first()

    if existing_email:
        return jsonify({"message": "такой Email уже зарегистрирован"}), 409
    if existing_login:
        return jsonify({"message": "такой Login уже занят"}), 409

    hashed_password = generate_password_hash(password)
    user = User(email=email,username=username,login=login,password=hashed_password, avatar=avatar)
    db.session.add(user)
    db.session.commit()

    login_user(user)
    return jsonify({"message": "успешная регистрация"}), 201


@auth_bp.route("/login", methods=["POST"])
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

    current_user.last_joined = datetime.utcnow()
    db.session.commit()

    return jsonify({
        "message": "Успешно",
        "user": {
            "id": user.id,
            "login": user.login,
            "username": user.username,
            "email": user.email
        }
    }), 200


@auth_bp.route("/logout")
@login_required
def logout_route():
    logout_user()
    return jsonify({"message": "вы вышли из аккаунта"})


@auth_bp.route("/delete")
@login_required
def delete_profile():
    db.session.delete(current_user)
    db.session.commit()
    logout_user()
    return jsonify({"message": "Профиль успешно удален"}), 200











