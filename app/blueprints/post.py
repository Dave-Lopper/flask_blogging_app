# app/blueprints/post.py
import datetime

from faker import Faker
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user

from app.models import Post, User
from app.boot import DB


post = Blueprint("post", __name__)


@post.route("/write_post", methods=["POST"])
@login_required
def write_post():
    """Post writing endpoint

    Inserts the given post in DB

    :return: redirect Flask method to main.index
    :rtype: werkzeug.wrappers.response.Response
    """
    content = request.form.get("write_post_content")
    post = Post(
        content=content,
        posted_at=datetime.datetime.now(),
        user=current_user,
        user_id=current_user.id
    )
    DB.session.add(post)
    DB.session.commit()
    return redirect(url_for('main.index'))


@post.route("/delete_post/<post_id>", methods=["GET"])
@login_required
def delete_post(post_id):
    """Post deletion endpoint

    Deletes the given post in DB

    :param post_id: ID of post to delete
    :type post_id: [string]
    :return: redirect Flask method to main.index
    :rtype: werkzeug.wrappers.response.Response
    """
    post = Post.query.get(int(post_id))
    if post is None:
        return render_template("404.j2.html"), 404
    else:
        DB.session.delete(post)
        DB.session.commit()
        flash("Post deleted succesfully")
        return redirect(f"/user/{current_user.id}")


@post.cli.command("seed")
def seed():
    """Seeds the database with users and posts.

    Takes the number of users, and the number of post for each user to be
    inserted as input.
    """
    nb_users = input("How many users would you like to insert ?\n")
    nb_post = input("How many posts by user would you like to insert ?\n")
    print("Working on it... \n")
    fake = Faker()
    users = []
    posts = []
    for i in range(int(nb_users)):
        user = User(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            password=fake.password(),
            birth_date=fake.date_time()
        )
        users.append(user)
    DB.session.add_all(users)

    for user in User.query.all():
        for i in range(int(nb_post)):
            post = Post(
                content=fake.text(),
                posted_at=fake.date_time(),
                user=user,
                user_id=user.id
            )
            posts.append(post)
    DB.session.add_all(posts)
    DB.session.commit()
    total_posts = int(nb_users) * int(nb_post)
    print(f"Inserted {nb_users} users and {total_posts} posts in database.")
