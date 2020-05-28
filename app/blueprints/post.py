# app/blueprints/post.py
import datetime

from flask import Blueprint, redirect, request, url_for
from flask_login import login_required, current_user

from app.models import Post
from app.boot import DB


post = Blueprint("post", __name__)


@post.route("/write_post", methods=["POST"])
@login_required
def write_post():
    """Post writing endpoint

    Inserts the given post in DB

    :return: redirect Flask method to main.index
    :rtype: werkzeug.wrappers.response.Response
    """
    content = request.form.get("write_post_content")
    post = Post(
        content=content,
        posted_at=datetime.datetime.now(),
        user=current_user,
        user_id=current_user.id
    )
    DB.session.add(post)
    DB.session.commit()
    return redirect(url_for('main.index'))
