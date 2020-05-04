# /app/blueprints/main.py
from flask import Blueprint, render_template

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.j2.html")


@main.route("/signin")
def signin():
    return render_template("signin.j2.html")


@main.route("/logged-in")
def loggedin():
    return render_template("logged-in.j2.html")
