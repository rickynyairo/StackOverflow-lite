"""
This module collects the views for the questions resource

"""
import json

# third party imports
from flask.views import MethodView
from flask import request, jsonify
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized
from .... import init_db

from ..users.user_models import UserModel
from ..questions.question_models import QuestionModel

class Questions(MethodView):
    """This class collects the methods for the questions endpoint"""
    def post(self):
        """This function handles post requests"""
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise BadRequest
        auth_token = auth_header.split(" ")[1]
        response = UserModel().decode_auth_token(auth_token)
        if not isinstance(response, str):
            # the token decoded succesfully
            user_id = response       
            if not request.data:
                raise BadRequest
            req_data = json.loads(request.data.decode().replace("'", '"'))
            try:
                text = req_data['text']
                description = req_data['description']
            except (KeyError, IndexError):
                raise BadRequest
            # save question in db
            question = QuestionModel(int(user_id), text, description)
            question_id = question.save_question() 
            resp = dict(message="success", text=text, question_id=str(question_id))

            return jsonify(resp), 201
        else:
            # token is either invalid or expired, right now, we don't care
            raise Unauthorized
