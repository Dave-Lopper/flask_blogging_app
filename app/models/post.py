# /app/models/post.py
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app.boot import DB


class Post(DB.Model):
    __tablename__ = "posts"
    id = DB.Column(DB.Integer, primary_key=True, nullable=False)
    content = DB.Column(DB.String(3000))
    posted_at = DB.Column(DateTime)
    user_id = DB.Column(DB.Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="posts")

    likes = relationship("Like")

    @hybrid_property
    def excerpt(self):
        """Shortens post content to 180 chars.

        :return: The shorten post exceprt
        :rtype: [string]
        """
        words = self.content[:177].split(' ')
        words.pop(len(words) - 1)
        excerpt = " ".join(words)
        return f"{excerpt}..."
