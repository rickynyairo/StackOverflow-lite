"""
This module collects the endpoints for the authentication resource

"""
import json

# third party imports
from flask.views import MethodView
from flask import request, jsonify
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized, Forbidden
from werkzeug.security import generate_password_hash, check_password_hash

from ..models.user_model import UserModel

class AuthLogin(MethodView):
    """This class collects the methods for the auth/login endpoint"""
    def post(self):
        """This function handles post requests"""       
        if not request.data:
            raise BadRequest
        req_data = json.loads(request.data.decode().replace("'", '"'))
        try:
            username = req_data['username']
            password = req_data['password']
        except (KeyError, IndexError):
            raise BadRequest
        # locate user in db
        user = UserModel(username=username, password=password)
        record = user.get_user_by_username(username)
        if not record:
            raise Unauthorized('Your details were not found, please sign up')

        user_id, fname, lname, pwordhash, date_created = record
        name = "{}, {}".format(lname, fname)
        if not check_password_hash(pwordhash, password):
            raise Unauthorized
    
        token = user.encode_auth_token(int(user_id))
        
        resp = dict(
            message="success",
            AuthToken=token.decode('utf-8'),
            name=name,
            date_created=date_created
        )      

        return jsonify(resp), 200

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
            "last_name":last_name,
            "email":email,
            "password":password
        }
        user_model = UserModel(**user)
        try:
            saved = user_model.save_user()
            if not saved:
                raise ValueError
        except ValueError:
            raise Forbidden("The username already exists")

        user_id = saved
        token = user_model.encode_auth_token(user_id)
        resp = {
            "message":"User signed up successfully",
            "AuthToken":"{}".format(token.decode('utf-8')),
            "username":username,
            "user_id":"{}".format(user_id),
            "status":"success"
        }
        user_model.close_db()
        return jsonify(resp), 201
