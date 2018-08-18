import json
from datetime import datetime
from flask import request, jsonify, abort
from . import users
from app.data import data
     
@users.route('/api/v1/users/', methods=['POST', 'GET'])
def get_users():
    """This function handles request to the users resource"""
    if request.method == 'GET':
        # return all questions in the db
        response = jsonify(data['users'])
        response.status_code = 200
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
        username = req_data['username']
        email = req_data['email']
        date_created = '{:%B %d, %Y}'.format(datetime.now())
        new_user = {
            "id":user_id,
            "username":username,
            "email":email,
            "date_created":date_created,
            "no_of_answers":"0"
        }
        data['users'].append(new_user)
        response = jsonify(new_user)
        response.status_code = 201

    return response
    