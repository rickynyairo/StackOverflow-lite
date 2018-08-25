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
            # token is either invalid or expired, right now, we don't care
            raise Unauthorized

class GetAnswer(MethodView):
    """This class collects the views gor a particular answer"""
    def delete(self, question_id, answer_id):
        """This function deletes a answer, given the id"""
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise BadRequest
        auth_token = auth_header.split(" ")[1]
        response = UserModel().decode_auth_token(auth_token)

        if isinstance(response, str):
            # the user is not authorized to view this endpoint
            raise Unauthorized
        else:
            # user is authorized
            questions = QuestionModel()
            question = questions.get_question_by_id(int(question_id))
            answers = AnswerModel()
            answer = answers.get_answer_by_id(int(answer_id))
            if not answer or not question:
                # the answer or question was not found
                raise NotFound("The details of the question or the answer could not be located.")
            answer_id, user_id, text, description, date_created = answer           
            # check if user ids match
            if int(user_id) == int(response):
                # delete answer
                answers.delete_answer(int(answer_id))
            else:
                # it is not the same user who asked the answer
                raise Forbidden
            resp = {
                "message":"success",
                "description":"answer deleted succesfully"
            }
            return jsonify(resp), 200

    def put(self, question_id, answer_id):
        """This function edits an answer, given the id"""
        auth_header = request.headers.get('Authorization')
        if not auth_header or not request.data:
            raise BadRequest
        auth_token = auth_header.split(" ")[1]
        response = UserModel().decode_auth_token(auth_token)
        if isinstance(response, str):
            # the user is not authorized to view this endpoint
            raise Unauthorized
        else:
            questions = QuestionModel()
            question = questions.get_question_by_id(int(question_id))
            answers = AnswerModel()
            answer = answers.get_answer_by_id(int(answer_id))
            if not answer or not question:
                # the answer or question was not found
                raise NotFound("Details of the question answer not found.")
            text = ""          
            # check if user ids match
            if int(user_id) == int(response):
                new_text = json.loads(request.data.decode().replace("'", '"'))['text']
                text = answers.update_answer(new_text, answer_id)
            else:
                raise Forbidden
            resp = {
                "message":"success",
                "description":"answer updated succesfully",
                "text":text
            }
            return jsonify(resp), 200