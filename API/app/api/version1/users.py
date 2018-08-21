"""
This module defines the routes of the users resource and the accompanying view functions

Authored by: Ricky Nyairo
"""

# standard imports
import json
import re

# third party imports
from datetime import datetime
from flask import request, jsonify, make_response
from werkzeug.exceptions import NotFound, BadRequest, Unauthorized

# local imports
from app.data import data
from app import _locate
from . import version1

@version1.route('/users/', methods=['GET'], strict_slashes=False)
def get_users():
    """This function handles request to the users resource"""
    # return response with all the users in the data store
    response = make_response(jsonify(data['users']), 200)

    return response

@version1.route('/users/<int:user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """This function responds with a particular user, given the id"""
    # locate the user
    user = _locate(int(user_id), "users")[0]
    if not user:
        # the user with the given id was not found
        # raise error 404
        raise NotFound
    else:
        # return a response with the user id, email and username
        response = make_response(jsonify({
            "user_id":str(user['user_id']),
            "username":user['username'],
            "email":user['email']
            }), 201)
        return response

@version1.route('/users/signup/', methods=['POST'], strict_slashes=False)
def signup_users():
    """This functions hangle user signup requests"""
    try:
        user_id = int(data["users"][-1]['user_id']) + 1
    except IndexError:
        # there are no existing users, create first user.
        user_id = "1"
    req_data = json.loads(request.data.decode('utf-8').replace("'", '"'))
    # validation
    try:
        username = req_data['username']
        email = req_data['email']
        password = req_data['password']
    except (IndexError, KeyError):
        raise BadRequest
    if not username or not email:
        raise BadRequest
    # validate the email structure
    if not re.match(r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                    email):
        raise BadRequest

    date_created = '{:%B %d, %Y}'.format(datetime.now())
    new_user = {
        "user_id":str(user_id),
        "username":username,
        "email":email,
        "date_created":date_created,
        "no_of_answers":"0",
        "password":password
    }
    data['users'].append(new_user)
    # remove password from response
    del new_user["password"]
    new_user["message"] = "User signed up successfully"
    response = make_response(jsonify(new_user), 201)

    return response

@version1.route('/users/signin', methods=['POST'], strict_slashes=False)
def signin_users():
    """This functions hangle user signin requests"""
    req_data = json.loads(
        request.data.decode('utf-8').replace("'", '"'))
    # import pdb
    # validation
    try:
        username = req_data['username']
        password = req_data['password']
    except (IndexError, KeyError):
        raise BadRequest
    user = {}
    user = [user for item in data['users'] if item['username'] is username]
    if not user:
        # user was not found, raise error
        raise Unauthorized
    elif user['password'] is not password:
        # user is not authorized
        raise Unauthorized 
    resp = {
        "user_id":user['user_id'],
        "username":user['username'],
        "no_of_answers":user['no_of_answers'],
        "message":"User signed in successfully"
    }
    response = make_response(jsonify(resp), 200)
    return response
