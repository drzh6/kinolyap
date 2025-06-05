from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user


profile_bp = Blueprint("profile", __name__, url_prefix="/api")


@profile_bp.route("/profile", methods=['GET'])
@login_required
def profile():
    return jsonify({
        "id": current_user.id,
        "login": current_user.login,
        "username": current_user.username,
        "email": current_user.email,
        "date_joined": current_user.date_joined.isoformat()
    })


@profile_bp.route("/me", methods=["POST"])
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


@profile_bp.route("/profile_change", methods=["POST"])
@login_required
def profile_change():
    data = request.json
    username = data.get("name")
    return jsonify({"username": username})





