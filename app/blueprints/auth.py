# /app/blueprints/auth.py
from datetime import date
import re

from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from app.models import User
from app.boot import DB
from app.utils import email_regex

auth = Blueprint("auth", __name__)


@login_required
@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route("/login", methods=["POST"])
def login():
    """Login endoint

    Logs user in and redirects to profile page,
    to the index in case of failure

    :return: redirect Flask method to main.profile
    :rtype: werkzeug.wrappers.response.Response
    """
    email = request.form.get("login_email")
    password = request.form.get("login_password")
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Please check your login details and try again.")
        return redirect(url_for("main.index"))

    remember = True if request.form.get("login_rememberme") else False
    login_user(user, remember=remember)

    return redirect(url_for("main.profile"))


@auth.route("/register", methods=["POST"])
def register():
    """Register endpoint

    Checks users input, adds it to the database,
    logs him in and redirects him to his profile if success.
    Redirects on index on failure.

    :return: redirect Flask method to main.profile
    :rtype: werkzeug.wrappers.response.Response
    """
    email = request.form.get("signin_email")
    if DB.session.query(User.id).filter_by(email=email).scalar() is not None:
        flash("Email already exists", "email")
        return redirect(url_for("main.signin"))

    if re.match(email_regex, email) is None:
        flash("Please provide a valid email adress", "email")
        return redirect(url_for("main.signin"))

    password = request.form.get("signin_password")
    password_confirm = request.form.get("signin_password_confirm")
    if password != password_confirm:
        flash("Password and its confirmation are different !", "password")
        return redirect(url_for("main.signin"))

    first_name = request.form.get("signin_first_name")
    last_name = request.form.get("signin_last_name")
    birth_date = request.form.get("signin_birth_date")

    user = User(email=email, first_name=first_name,
                last_name=last_name, birth_date=birth_date,
                password=generate_password_hash(password),
                registered_at=date.today())
    DB.session.add(user)
    DB.session.commit()

    login_user(user)
    return redirect(url_for("main.profile"))
