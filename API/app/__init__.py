"""
This module sets up configuration and creates the application.
It defines functions to be accessed by all modules.

Authored by: Ricky Nyairo
"""

import json

# local imports
from flask import Flask, jsonify, request, make_response
from .data import data

def _locate(item_id, items):
    """This function takes 2 arguments (id : int and items : string)
        To locate the item = question or user, with the identifier = id,
        from the collection of items."""
    collection = data[items]
    required_item = {}
    found = False
    index = 0
    for i, item in enumerate(collection):
        if item['{}_id'.format(items[:-1])] == str(item_id):
            required_item = item
            found = True
            index = i
            break
    if found:
        responce = (required_item, index)
    else:
        responce = (None, None)

    return responce

def not_found(error):
    """This function returns a custom JSON response when a resource is not found"""
    error_dict = {
        "path_accessed":str(request.path),
        "message":"The path accessed / resource requested cannot be found, please check",
        "error":str(error)
    }
    response = make_response(jsonify(error_dict), 404)
    return response

def bad_request(error):
    """This function creates a custom JSON response when a bad request is made"""
    error_dict = {
        "path_accessed":str(request.path),
        "message":"The request made had errors, please check the headers or params",
        "request_data":json.loads(request.data.decode().replace("'", '"')),
        "error":str(error)
    }
    response = make_response(jsonify(error_dict), 400)
    return response

def create_app():
    """This function sets up and returns the application"""
    app = Flask(__name__)
    from .questions import questions as questions_blueprint
    app.register_blueprint(questions_blueprint)
    from .users import users as users_blueprints
    app.register_blueprint(users_blueprints)
    app.register_error_handler(400, bad_request)
    app.register_error_handler(404, not_found)
    return app

APP = create_app()
    