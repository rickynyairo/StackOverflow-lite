"""
This module sets up the questions resource

Authored by: Ricky Nyairo
"""
from flask import Blueprint

questions = Blueprint('questions', __name__)

from . import views
