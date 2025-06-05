from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user


profile_bp = Blueprint("profile", __name__, url_prefix="/api")


@profile_bp.route("/profile")
@login_required
def profile():
    user = current_user
    return jsonify({
        "id": user.id,
        "email": user.email,
        "login": user.login,
        "username": user.username,
        "date_joined": user.date_joined
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


@profile_bp.route("/reviews")
@login_required
def user_reviews():
    reviews = current_user.review
    result = []
    for review in reviews:
        result.append({
            "movie_id": review.movie_id,
            "text": review.review_text,
            "rating": review.review_rating,
            "date": review.review_date.isoformat()
        })
    return jsonify(result)











