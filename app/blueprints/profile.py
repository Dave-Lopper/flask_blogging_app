# /app/blueprints/profile.py
import re

from flask import Blueprint, flash, redirect, request, url_for
from flask_login import login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from app.boot import DB
from app.models import User
from app.utils import email_regex


profile = Blueprint("profile", __name__)


@profile.route("/edit_profile", methods=["POST"])
@login_required
def edit_profile():
    """Edit profile endpoint.

    Allows the user to change his attributes

    :return: redirect Flask method to main.profile
    :rtype: werkzeug.wrappers.response.Response"""
    email = request.form.get("edit_email")
    if email != current_user.email:
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
    """Delete profile endpoint.

    Allows the user to delete his account,
    Asks for the password, and checks it.

    :return: redirect Flask method to main.profile
    :rtype: werkzeug.wrappers.response.Response"""
    password = request.form.get("delete_password")

    if check_password_hash(current_user.password, password):
        user_id = current_user.id
        logout_user()
        DB.session.query(User).filter_by(id=user_id).delete()
        return redirect(url_for("main.index"))

    flash("Please check your password and try again", "delete")
    return redirect(url_for("main.profile"))


@profile.route("/edit_password", methods=["POST"])
@login_required
def edit_password():
    """Edit password endpoint

    Allows the user to change his password,
    Asks for the password, and checks it.

    :return: redirect Flask method to main.profile
    :rtype: werkzeug.wrappers.response.Response"""
    current_password = request.form.get("edit_current_password")

    if not check_password_hash(current_user.password, current_password):
        flash("Please check your password and try again", "current")
        return redirect(url_for("main.change_password"))

    new_password = request.form.get("edit_new_password")
    new_password_confirm = request.form.get("edit_new_password_confirm")

    if new_password != new_password_confirm:
        flash("The new password and its confirmation don't match", "new")
        return redirect(url_for("main.change_password"))

    current_user.password = generate_password_hash(new_password)
    DB.session.commit()
    flash(
        "Your password has been changed succesfully",
        "change_password_success"
    )
    return redirect(url_for("main.profile"))
