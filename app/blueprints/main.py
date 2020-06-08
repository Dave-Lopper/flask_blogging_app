# /app/blueprints/main.py
from flask import Blueprint, current_app, render_template, request
from flask_login import login_required, current_user

from app.models import Post

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
