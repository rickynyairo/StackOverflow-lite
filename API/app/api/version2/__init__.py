"""
This module sets up the users resource

Authored by: Ricky Nyairo
"""

from flask import Blueprint

version2 = Blueprint('version2', __name__)

from .auth.auth_views import AuthSignup, AuthLogin
from .questions.question_views import Questions, GetQuestion

version2.add_url_rule('/auth/signup', view_func=AuthSignup.as_view('signup'))
version2.add_url_rule('/auth/login', view_func=AuthLogin.as_view('login'))
version2.add_url_rule('/questions', view_func=Questions.as_view('questions'))
version2.add_url_rule('/questions/<int:question_id>', view_func=GetQuestion.as_view('get_questions'))