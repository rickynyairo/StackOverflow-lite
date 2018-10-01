"""
This module renders the templates for the user interface
"""
from flask import render_template, url_for, redirect
from flask.views import MethodView
from werkzeug.exceptions import NotFound

from ..api.version2.models.question_model import QuestionModel
from ..api.version2.models.user_model import UserModel

class SignupPage(MethodView):
    """Encapsulates the views for the landing page"""
    def get(self):
        """returns the index page"""
        return render_template('index.html')

class HomePage(MethodView):
    """Encapsulates the views for the home page"""
    def get(self):
        """returns the home page"""
        return render_template('home.html')

class ProfilePage(MethodView):
    """Encapsulates the views for the user profile page"""
    def get(self, username):
        """render the profie page"""
        user = UserModel().check_exists(username)
        if user:
            context = {
                "userId":int(user[0]),
                "username":username,
                "dateCreated":user[1].strftime("%B %d, %Y")
            }
            return render_template("profile.html", **context)
        else:
            raise NotFound("The username provided was not found")

class QuestionPage(MethodView):
    """Encapsulates the views for the questions page"""
    def get(self, question_id):
        """return the questions page"""
        questions = QuestionModel()
        question = questions.get_item_by_id(question_id)
        if not question:
            raise NotFound("The specified resource cannot be located.")
        else:
            username = questions.get_username_by_id(question[1])
            date = question[4]
            context = {
                "questionId":int(question[0]),
                "questionText":question[2],
                "questionDesc":question[3],
                "username":username,
                "dateCreated":date.strftime("%B %d, %Y")

            }
        return render_template('question.html', **context)

class QuestionsPage(MethodView):
    """Encapsulates the views for the questions page"""
    def get(self):
        """redirects to the home page"""
        return redirect(url_for('ui.home'), 303)

class LandingPage(MethodView):
    """Encapsulates the views for the questions page"""
    def get(self):
        """redirects to the home page"""
        return redirect(url_for('ui.home'), 303)

class LoginPage(MethodView):
    """Encapsulates the views for the login page"""
    def get(self):
        """return the login page"""
        return render_template('login.html')