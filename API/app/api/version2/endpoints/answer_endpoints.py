"""
This module collects the views for the answers resource

"""
import json

# third party imports
from flask.views import MethodView
from flask import request, jsonify
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized, Forbidden
from .... import init_db

from ..models.user_model import UserModel
from ..models.question_model import QuestionModel
from ..models.answer_model import AnswerModel

class Answers(MethodView):
    """This class collects the methods for the answers endpoint"""
    def post(self, question_id):
        """This function handles post requests"""
        auth_header = request.headers.get('Authorization')
        if not auth_header or not request.data:
            raise BadRequest
        auth_token = auth_header.split(" ")[1]
        response = UserModel().decode_auth_token(auth_token)
        if not isinstance(response, str):
            # the token decoded succesfully
            user_id = response           
            req_data = json.loads(request.data.decode().replace("'", '"'))
            try:
                text = req_data['text']
            except (KeyError, IndexError):
                raise BadRequest
            # save answer in db
            answer = AnswerModel(int(question_id), int(user_id), text)
            answer_id = int(answer.save_answer())
            answer.close_db() 
            resp = dict(message="success", text=text, answer_id=str(answer_id))
            return jsonify(resp), 201
        else:
            # token is either invalid or expired
            raise Unauthorized

class GetAnswer(MethodView):
    """This class encapsulates the method functions for a particular answer"""

    def put(self, question_id, answer_id):
        """
        This function is restricted to the author of the answer and the
        author of the question. 
        The ```answer_author_id``` is allowed to edit the answer. 
        The ```question_author_id``` is allowed to mark the answer as preferred
        """
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise BadRequest
        auth_token = auth_header.split(" ")[1]
        response = UserModel().decode_auth_token(auth_token)
        if isinstance(response, str):
            # the user is not authorized to view this endpoint
            raise Unauthorized
        else:
            questions = QuestionModel()
            question_author_id = questions.get_item_by_id(int(question_id))[1]
            answers = AnswerModel()
            answer_author_id = answers.get_item_by_id(int(answer_id))[2]
            if not question_author_id or not answer_author_id:
                # the answer or question was not found
                raise NotFound("Details of the question or answer not found.")
            value = ""          
            # check if user ids match
            user_id = int(response)
            if user_id == int(answer_author_id) and user_id != int(question_author_id):
                new_text = json.loads(request.data.decode().replace("'", '"'))['text']
                value = answers.update_item(field="text", 
                                            data=new_text,
                                            item_id=answer_id)[0]
            elif user_id == int(question_author_id) and user_id != int(answer_author_id):
                value = "{}".format(answers.toggle_user_preferred(answer_id))
            else:
                raise Forbidden
            resp = {
                "message":"success",
                "description":"answer updated succesfully",
                "value":value
            }
            return jsonify(resp), 200
