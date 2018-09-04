"""
This module renders the templates for the user interface
"""
from flask import render_template, url_for
from flask.views import MethodView


class LandingPage(MethodView):
    """Encapsulates the views for the landing page"""
    def get(self):
        """returns the index page"""
        return render_template('index.html')

class HomePage(MethodView):
    """Encapsulates the views for the home page"""
    def get(self):
        """returns the home page"""
        return render_template('home.html')

class QuestionsPage(MethodView):
    """Encapsulates the views for the questions page"""
    def get(self):
        """return the questions page"""
        return render_template('questions.html')

class LoginPage(MethodView):
    """Encapsulates the views for the login page"""
    def get(self):
        """return the login page"""
        return render_template('login.html')