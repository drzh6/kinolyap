from flask import Blueprint, jsonify
from flask_login import login_required, current_user

from ..models import User
from ..extensions import db


subs_bp = Blueprint("subs", __name__, url_prefix="/api")

@subs_bp.route("/follow/<int:user_id>", methods=["POST", "GET"])
@login_required
def follow_user(user_id):
    user_to = User.query.get_or_404(user_id)
    if user_to == current_user:
        return jsonify({"message":"Нельзя подписаться на самого себя"})
    
    if user_to not in current_user.following:
        current_user.following.append(user_to)
        db.session.commit()
        return jsonify({"message":f"вы подписались на {user_to.username}"})

    current_user.following.remove(user_to)
    db.session.commit()
    return jsonify({"message": f"Вы отписались от {user_to.username}"})



@subs_bp.route("/is_follow/<int:user_id>")
@login_required
def is_follow(user_id):
    user_to = User.query.get_or_404(user_id)
    is_following = user_to in current_user.following
    return jsonify({"following": is_following})


@subs_bp.route("/get_followers/<int:user_id>", methods=["GET"])
@login_required
def get_followers(user_id):
    user = User.query.get_or_404(user_id)
    following_list = user.following
    return jsonify([element.to_dict() for element in following_list])


    










