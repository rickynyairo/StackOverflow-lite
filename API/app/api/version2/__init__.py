"""
This module sets up the users resource

Authored by: Ricky Nyairo
"""

from flask import Blueprint

version2 = Blueprint('version2', __name__)

from .auth.views import AuthSignup

version2.add_url_rule('/auth/signup', view_func=AuthSignup.as_view('signup'))