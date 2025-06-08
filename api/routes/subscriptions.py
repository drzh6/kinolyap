from flask import Blueprint, jsonify
from flask_login import login_required, current_user

from ..models import User
from ..extensions import db


subs_bp = Blueprint("subs", __name__, url_prefix="/api")

# Дает возможность подписаться на пользователя
@subs_bp.route("/follow/<int:user_id>")
@login_required
def follow_user(user_id):
    user_to_do = User.query.get_or_404(user_id)
    if user_to_do == current_user:
        return jsonify({"message":"Нельзя подписаться на самого себя"})
    
    if user_to_do not in current_user.following:
        current_user.following.append(user_to_do)
        db.session.commit()
        return jsonify({"message":f"вы подписались на {user_to_do.username}"})

# Дает возможность отписаться от пользователя
@subs_bp.route("/unfollow/<int:user_id>")
@login_required
def unfollow(user_id):
    user_to_do = User.query.get_or_404(user_id)
    if user_to_do == current_user:
        return jsonify({"message":"Нельзя отписаться от самого себя"})
    
    if user_to_do in current_user.followig:
        current_user.following.remove(user_to_do)
        db.session.commit()
        return jsonify({"message": f"Вы отписались от {user_to_do.username}"})

# Проверка подписан ли пользователь
@subs_bp.route("/is_follow/<int:user_id>")
@login_required
def is_follow(user_id):
    user_to = User.query.get_or_404(user_id)
    is_following = user_to in current_user.following
    return jsonify({"following": is_following})

# Выводит ваших подписчиков 
@subs_bp.route("/get_my_followers")
@login_required
def get_my_followers():
    followers = current_user.following
    return jsonify([follower.to_dict() for follower in followers])

# Выводит всех подписчиков 
@subs_bp.route("/get_followers/<int:user_id>")
@login_required
def get_followers(user_id):
    user = User.query.get_or_404(user_id)
    followers = user.following.all()
    return jsonify([follower.to_dict() for follower in followers])



    










