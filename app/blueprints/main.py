# /app/blueprints/main.py
from flask import Blueprint, render_template
from flask_login import login_required

from app.models import Post

main = Blueprint("main", __name__)


@main.route("/")
def index():
    posts = Post.query.order_by(Post.posted_at.desc()).all()
    return render_template("index.j2.html", posts=posts)


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
