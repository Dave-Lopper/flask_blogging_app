# /app/blueprints/main.py
import re

from flask import Blueprint, flash, redirect, request, url_for
from flask_login import login_required, current_user

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
            flash("Please provide a valid email adress.")
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
