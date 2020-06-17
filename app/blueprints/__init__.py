# /app/blueprints/__init__.py
from .auth import auth
from .main import main
from .like import like
from .post import post
from .profile import profile

__all__ = ['auth', 'like', 'main', 'post', 'profile']
