"""
This module collects the views for the answers resource

"""
import json

# third party imports
from flask.views import MethodView
from flask import request, jsonify
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized, Forbidden
from .... import init_db

from ..users.user_models import UserModel
from ..questions.question_models import QuestionModel
from ..answers.answers_models import AnswerModel

class Answers(MethodView):
    """This class collects the methods for the answers endpoint"""
    def post(self, question_id):
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
            # save answer in db
            answer = AnswerModel(int(question_id), int(user_id), text)
            answer_id = answer.save_answer()
            answer.close_db() 
            resp = dict(message="success", text=text, answer_id=str(answer_id))
            return jsonify(resp), 201
        else:
            # token is either invalid or expired, right now, we don't care
            raise Unauthorized

    def get(self, question_id):
        """This function handles get requests"""
        # get answers from db
        answers = AnswerModel().get_answers_by_question_id(int(question_id))
        resp = {
            "message":"success",
            "answers":answers
        }
        return jsonify(resp), 200

class GetAnswer(MethodView):
    """This class collects the views gor a particular answer"""

    def get(self, answer_id):
        """Returns a answer and all it's answers"""
        # no auth required
        answer = AnswerModel().get_answer_by_id(int(answer_id))
        if not answer:
            # answer was not found
            raise NotFound
        else:
            # find it's answers
            answers = AnswerModel().get_answers_by_answer_id(int(answer_id))
            answer_id, user_id, text, description, date_created = answer
            user = UserModel().get_user_by_id(int(user_id))
            resp = dict(user=user,
                        text=text,
                        description=description,
                        date_created=date_created,
                        answers=answers)
            return jsonify(resp), 200

    def delete(self, answer_id):
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
            answers = AnswerModel()
            answer = answers.get_answer_by_id(int(answer_id))
            if not answer:
                # the answer was not found
                raise NotFound
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