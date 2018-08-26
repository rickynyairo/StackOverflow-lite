"""
This module sets up the users resource

Authored by: Ricky Nyairo
"""

from flask import Blueprint

version2 = Blueprint('version2', __name__)

from .endpoints.answer_endpoints import Answers, GetAnswer 
from .endpoints.auth_endpoints import AuthLogin, AuthSignup
from .endpoints.question_endpoints import Questions, GetQuestion, GetUserQuestion

version2.add_url_rule('/auth/signup', view_func=AuthSignup.as_view('signup'))
version2.add_url_rule('/auth/login', view_func=AuthLogin.as_view('login'))
version2.add_url_rule('/questions', view_func=Questions.as_view('questions'))
version2.add_url_rule('/questions/<username>', view_func=GetUserQuestion.as_view('user_questions'))
version2.add_url_rule('/questions/<int:question_id>', view_func=GetQuestion.as_view('one_question'))
version2.add_url_rule('/questions/<int:question_id>/answers/<int:answer_id>', view_func=GetAnswer.as_view('get_answer'))
version2.add_url_rule('/questions/<int:question_id>/answers', view_func=Answers.as_view('answers'))