"""
This module sets up the user interface

"""
from flask import Blueprint

ui = Blueprint('ui', __name__)

from .user_views import *

ui.add_url_rule('/', view_func=LandingPage.as_view('index'))
ui.add_url_rule('/home', view_func=QuestionsPage.as_view('questions'))
ui.add_url_rule('/login', view_func=LoginPage.as_view('login'))
