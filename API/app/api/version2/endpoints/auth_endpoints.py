"""
This module collects the endpoints for the authentication resource

"""
import json
import re

# third party imports
from flask_restplus import Resource
from flask import request, jsonify
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized, Forbidden
from werkzeug.security import generate_password_hash, check_password_hash

#local imports
from ..utils.serializers import UserDTO
from ..models.user_model import UserModel

api = UserDTO().api
_user = UserDTO().user
_n_user = UserDTO().n_user
_n_user_resp = UserDTO().n_user_resp
_user_resp = UserDTO().user_resp

@api.route("/signup/")
class AuthSignup(Resource):
    """This class collects the methods for the auth/signup method"""

    docu_string = "This endpoint allows an unregistered user to sign up."
    @api.doc(docu_string)
    @api.expect(_n_user)
    @api.marshal_with(_n_user_resp, code=201)
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
            if not re.match(r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                    email):
                raise BadRequest("The email provided is invalid")
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
            "user_id":"{}".format(user_id)
        }
        user_model.close_db()
        return resp, 201

@api.route("/login/")
class AuthLogin(Resource):
    """This class collects the methods for the auth/login endpoint"""

    docu_string = "This endpoint allows a registered user to log in."
    @api.doc(docu_string)
    @api.expect(_user)
    @api.marshal_with(_user_resp, code=200)
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

        return resp, 200
