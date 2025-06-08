from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from datetime import datetime

from ...models import Review
from ...extensions import db


review_bp = Blueprint("review", __name__, url_prefix="/api")


# Выводит из бд все отзывы пользователей к определенному фильму
@review_bp.route("/movie_reviews/<int:movie_id>")
def show_movie_reviews(movie_id):
    reviews = Review.query.filter_by(movie_id=movie_id).all()
    if not reviews:
        return jsonify({"message":"Пока отзывов нет"})
    result = []
    for review in reviews:
        result.append({
        "text": review.review_text,
        "rating": review.review_rating,
        "date_added": review.review_date,
        "author": review.author.username
        })
    return jsonify(result)

# Дает возможность написать отзыв к определенному фильму
@review_bp.route("/add_review/<int:movie_id>", methods=["POST"])
@login_required
def add_review(movie_id):
    existing_review = Review.query.filter_by(user_id=current_user.id, movie_id=movie_id).first()
    if existing_review:
        return jsonify({"message": "Вы уже оставили отзыв про этот фильм."})
    
    data = request.json
    text = data.get("text")
    rating = data.get("rating")
    review_date = datetime.utcnow()
    
    if not rating or not text:
        return jsonify({"message": "Вы не ввели данные."}), 400
    
    try:
        rating = float(rating)  
    except (ValueError, TypeError):
        return jsonify({"message": "Рейтинг должен быть числом."}), 400

    review = Review(
    user_id=current_user.id,
    movie_id=movie_id,
    review_text=text,
    review_rating=rating,
    review_date=review_date
    )

    db.session.add(review)
    db.session.commit()
    return jsonify({"message": "Отзыв оставлен"})

# Удаляет отзыв (проверка чтобы другой бзер не могу удалить)
@review_bp.route("/delete_review/<int:review_id>")
@login_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)

    if not review:
        return jsonify({"error": "Отзыв не найден"}), 404
    if review.user_id != current_user.id:
        return jsonify({"error": "Нет доступа"}), 403

    db.session.delete(review)
    db.session.commit()
    return jsonify({"message":"Отзыв удален!"})