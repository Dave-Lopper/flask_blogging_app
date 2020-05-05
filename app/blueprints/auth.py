# /app/blueprints/auth.py
from datetime import date
import re

from flask import Blueprint, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash

from app.models import User
from app.boot import DB

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["POST"])
def register():
    email = request.form.get("signin_email")
    if DB.session.query(User.id).filter_by(email=email).scalar() is not None:
        flash("Email already exists", "email")
        return redirect(url_for("main.signin"))

    # Bonus exercise
    email_regex = r'^\w+([.-]?\w+)*@\w+([.-]?\w+)*\.(\w{2,3})$'
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
    return redirect(url_for("main.index"))
