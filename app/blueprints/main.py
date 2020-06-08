# /app/blueprints/main.py
from flask import Blueprint, current_app, render_template, request
from flask_login import login_required, current_user

from app.models import Post, User

main = Blueprint("main", __name__)


@main.route("/")
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.posted_at.desc()).paginate(
        page, current_app.config["FEED_PAGE_SIZE"]
    )
    pages = pagination.iter_pages(left_current=5, right_current=5)
    return render_template(
        "index.j2.html",
        posts=pagination.items,
        page=page,
        pages=pages,
        nb_pages=pagination.pages,
        user=current_user
    )


@main.route("/signin")
def signin():
    return render_template("signin.j2.html")


@main.route("/profile")
@login_required
def profile():
    return render_template("profile.j2.html")


@main.route("/profile/change_password")
@login_required
def change_password():
    return render_template("change-password.j2.html")


@main.route("/post/<post_id>")
def post_detail(post_id):
    post = Post.query.get(int(post_id))
    if post is not None:
        return render_template(
            "post-detail.j2.html",
            post=post
        )
    else:
        return render_template("404.j2.html"), 404


@main.route("/user/<user_id>")
def user_detail(user_id):
    user = User.query.get(int(user_id))
    if user is not None:
        return render_template(
            "user-detail.j2.html",
            user=user
        )
    else:
        return render_template("404.j2.html"), 404
