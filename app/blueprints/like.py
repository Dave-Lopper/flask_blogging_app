# app/blueprints/like.py
from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required

from app.models import Like, Post, User
from app.boot import DB


like = Blueprint("like", __name__)


@like.route("/like_post/<post_id>/<user_id>")
@login_required
def like_post(post_id, user_id):
    """Post liking endpoint

    Inserts likes in DB

    :return: redirect Flask method to main.index
    :rtype: werkzeug.wrappers.response.Response
    """
    post = Post.query.get(int(post_id))
    user = User.query.get(int(user_id))
    if post is None or user is None:
        return render_template("404.j2.html"), 404
    like = Like(
        user_id=user.id,
        post_id=post.id,
        user=user,
        post=post
    )
    DB.session.add(like)
    DB.session.commit()
    if request.referrer:
        return redirect(request.referrer)
    return redirect(url_for('main.index'))


@like.route("/unlike_post/<post_id>/<user_id>")
@login_required
def unlike_post(post_id, user_id):
    """Post liking endpoint

    Inserts likes in DB

    :return: redirect Flask method to main.index
    :rtype: werkzeug.wrappers.response.Response
    """
    like = Like.query \
        .filter_by(post_id=post_id) \
        .filter_by(user_id=user_id) \
        .first()

    if like is None:
        return render_template("404.j2.html"), 404

    DB.session.query(Like) \
        .filter_by(post_id=post_id) \
        .filter_by(user_id=user_id) \
        .delete()
    DB.session.commit()
    if request.referrer:
        return redirect(request.referrer)
    return redirect(url_for('main.index'))
