"""
This module sets up the user interface

"""
from flask import Blueprint

from ..api.version2.models.user_model import UserModel

ui = Blueprint('ui', __name__)

from .user_views import *

ui.add_url_rule('/', view_func=LandingPage.as_view('index'))
ui.add_url_rule('/signup', view_func=SignupPage.as_view('signup'))
ui.add_url_rule('/questions', view_func=QuestionsPage.as_view('questions'))
ui.add_url_rule('/profile/<username>', view_func=ProfilePage.as_view('profile'))
ui.add_url_rule('/questions/<int:question_id>', view_func=QuestionPage.as_view('question'))
ui.add_url_rule('/home', view_func=HomePage.as_view('home'))
ui.add_url_rule('/login', view_func=LoginPage.as_view('login'))
