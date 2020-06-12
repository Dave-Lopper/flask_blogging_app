# app/models/like.py
from sqlalchemy.orm import relationship

from app.boot import DB


class Like(DB.Model):
    __tablename__ = "likes"
    id = DB.Column(DB.Integer, primary_key=True)
    user_id = DB.Column(DB.Integer, DB.ForeignKey("users.id"))
    user = relationship("User")
    post_id = DB.Column(DB.Integer, DB.ForeignKey("posts.id"))
    post = relationship("Post", back_populates="likes")
