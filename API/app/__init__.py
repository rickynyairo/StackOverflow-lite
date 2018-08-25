"""
This module sets up configuration and creates the application.
It defines functions to be accessed by all modules.

The module sets up the blueprints to seperate the api versions

Authored by: Ricky Nyairo
"""

import json
import os
from contextlib import closing

# third party imports
from flask import Flask, jsonify, request, make_response
from instance.config import app_config
import psycopg2

# local imports
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

def init_db():
    """Set up the database to stode the user data
    """
    db_url = os.getenv("DATABASE_URL")  
    db = psycopg2.connect(db_url)
    return db

def error_handler(error, message):
    """This function creates a custom dictonary for the error functions"""
    request_data = ""
    if not request.data.decode():
        request_data = "Request body is empty"
    else:
        request_data = json.loads(request.data.decode().replace("'", '"'))
    
    error_dict = {
        "path_accessed":str(request.path),
        "message":message,
        "request_data":request_data,
        "error":str(error)
    }
    
    return error_dict

def not_found(error):
    """This function returns a custom JSON response when a resource is not found"""
    message = "The path accessed / resource requested cannot be found, please check"
    error_dict = error_handler(error, message)
    response = make_response(jsonify(error_dict), 404)
    return response

def bad_request(error):
    """This function creates a custom JSON response when a bad request is made"""
    message = "The request made had errors, please check the headers or parameters"   
    response = make_response(jsonify(error_handler(error, message)), 400)
    return response

def method_not_allowed(error):
    """This function creates a custom JSON response if the request method is not allowed."""
    message = "The request method used is not allowed"
    return jsonify(error_handler(error, message)), 400

def forbidden(error):
    """Return an error message if the request is forbidden"""
    message = "Sorry, You are not allowed to do that"
    return jsonify(error_handler(error, message)), 403

def unauthorized(error):
    """This function creates a custom JSON response when an unauthorized request is made"""
    message = "You are not authorized to access this resource, please confirm credentials"
    response = make_response(jsonify(error_handler(error, message)), 400)
    return response

def create_app(config_name='development'):
    """This function sets up and returns the application"""
    app = Flask(__name__, instance_relative_config=True)
    app.url_map.strict_slashes = False
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    from .api.version1 import version1 as version1_blueprint
    app.register_blueprint(version1_blueprint, url_prefix="/api/v1")

    from .api.version2 import version2 as version2_blueprint
    app.register_blueprint(version2_blueprint, url_prefix="/api/v2")

    app.register_error_handler(400, bad_request)
    app.register_error_handler(401, unauthorized)
    app.register_error_handler(404, not_found)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(403, forbidden)

    return app

db = init_db()
APP = create_app()
