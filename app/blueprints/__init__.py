# /app/blueprints/__init__.py
from .auth import auth
from .main import main
from .profile import profile

__all__ = ['auth', 'main', 'profile']
