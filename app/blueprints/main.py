# /app/blueprints/main.py
from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.j2.html")


@main.route("/signin")
def signin():
    return render_template("signin.j2.html")


@main.route("/logged-in")
@login_required
def loggedin():
    return render_template("logged-in.j2.html", name=current_user.first_name)
