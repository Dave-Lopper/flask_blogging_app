# /app/blueprints/profile.py
import re

from flask import Blueprint, flash, redirect, request, url_for
from flask_login import login_required, logout_user, current_user
from werkzeug.security import check_password_hash

from app.boot import DB
from app.models import User


profile = Blueprint("profile", __name__)


@profile.route("/edit_profile", methods=["POST"])
@login_required
def edit_profile():
    email = request.form.get("edit_email")
    if email != current_user.email:
        email_regex = r'^\w+([.-]?\w+)*@\w+([.-]?\w+)*\.(\w{2,3})$'
        if re.match(email_regex, email) is None:
            flash("Please provide a valid email adress", "edit")
            return redirect(url_for("main.profile"))

    first_name = request.form.get("edit_first_name")
    last_name = request.form.get("edit_last_name")

    DB.session.query(User).filter_by(id=current_user.id) \
        .update({
            "email": email,
            "first_name": first_name,
            "last_name": last_name
        })
    DB.session.commit()

    return redirect(url_for("main.profile"))


@profile.route("/delete_profile", methods=["POST"])
@login_required
def delete_profile():
    password = request.form.get("delete_password")

    if check_password_hash(current_user.password, password):
        user_id = current_user.id
        logout_user()
        DB.session.query(User).filter_by(id=user_id).delete()
        return redirect(url_for("main.index"))

    flash("Please check your password and try again", "delete")
    return redirect(url_for("main.profile"))
