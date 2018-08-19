import json
import re

from datetime import datetime
from flask import request, jsonify, make_response
from werkzeug.exceptions import NotFound, BadRequest

from . import users
from app.data import data
from app import _locate

@users.route('/api/v1/users/', methods=['POST', 'GET'])
def get_users():
    """This function handles request to the users resource"""
    if request.method == 'GET':
        # return all questions in the db
        response = make_response(jsonify(data['users']), 200)
    else: 
        # handles a POST request
        # return the new user with the user id and username
        try:
            user_id = int(data["users"][-1]['id']) + 1
        except IndexError:
            # there are no existing users, create first user. 
            user_id = "1"
        req_data = json.loads(
            request.data.decode('utf-8').replace("'", '"'))

        # validation
        try:
            username = req_data['username']
            email = req_data['email']
            password = req_data['password']

        except (IndexError, KeyError):
            raise BadRequest

        if len(username) == 0 or len(email) == 0:
            raise BadRequest

        # validate the email structure
        if not re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email):
            raise BadRequest

        date_created = '{:%B %d, %Y}'.format(datetime.now())
        new_user = {
            "id":str(user_id),
            "username":username,
            "email":email,
            "date_created":date_created,
            "no_of_answers":"0"
        }
        data['users'].append(new_user)
        response = jsonify(new_user)
        response.status_code = 201

    return response
    
@users.route('/api/v1/users/<int:id>', methods=['GET'])
def get_user(id):
    """This function responds with a particular user, given the id"""
    response = {}
    # locate the user
    user, index = _locate(int(id), "users")
    if user:
        # return a response with the user id, email and username
        response = make_response(jsonify({
            "user_id":str(user['id']),
            "username":user['username'],
            "email":user['email']                
            }), 201)
        return response         
    else:
        # the user with the given id was not found
        # raise error 404
        raise NotFound