"""
This module sets up the users resource

Authored by: Ricky Nyairo
"""

from flask import Blueprint

users = Blueprint('users', __name__)

from . import views
