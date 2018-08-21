"""
This module collects the views for the authentication resource

"""
import json

# third party imports
from flask.views import MethodView
from flask import request, jsonify
from werkzeug.exceptions import BadRequest

class AuthLogin(MethodView):
    """This class collects the methods for the auth/login endpoint"""
    def post(self):
        pass

class AuthSignup(MethodView):
    """This class collects the methods for the auth/signup method"""
    def post(self):
        """This function handles a post request"""
        req_data = request.data.decode().replace("'", '"')
        if not req_data:
            raise BadRequest
        user_details = json.loads(req_data)
        try:
            username = user_details['username']
            first_name = user_details['first_name']
            last_name = user_details['last_name']
            email = user_details['email']
            password = user_details['password']
        except (KeyError, IndexError):
            raise BadRequest
        user = {
            "username":username,
            "first_name":first_name,
            "second_name":last_name,
            "email":email,
            "password":password
        }

        return jsonify(user), 201
