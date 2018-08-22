"""
This module sets up the users resource

Authored by: Ricky Nyairo
"""

from flask import Blueprint

version2 = Blueprint('version2', __name__)

<<<<<<< HEAD
from .auth.auth_views import AuthSignup, AuthLogin

version2.add_url_rule('/auth/signup', view_func=AuthSignup.as_view('signup'))
version2.add_url_rule('/auth/login', view_func=AuthLogin.as_view('login'))
=======
>>>>>>> parent of 2426653... [Chore #Feature] Wrote tests for the user sign up endpoint and made the endpoint
