"""
This module collects the views for the questions resource

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
            username = question.get_username_by_id(int(user_id))
            question.close_db() 
            resp = dict(message="success",
                        text=text, 
                        asked_by=username,
                        question_id=str(question_id))

            return jsonify(resp), 201
        else:
            # token is either invalid or expired, right now, we don't care
            raise Unauthorized

    def get(self):
        """This function handles get requests"""
        # get questions from db
        questions = QuestionModel().get_all()
        resp = {
            "message":"success",
            "questions":questions
        }
        return jsonify(resp), 200

class GetQuestion(MethodView):
    """This class collects the views for a particular question"""
    def get(self, question_id):
        """Returns a question and all it's answers"""
        # no auth required
        question = QuestionModel().get_question_by_id(int(question_id))
        if not question:
            # question was not found
            raise NotFound
        else:
            # find it's answers
            answers = AnswerModel().get_answers_by_question_id(int(question_id))
            question_id, user_id, text, description, date_created = question
            user = UserModel().get_username_by_id(int(user_id)) # returns the username
            resp = dict(username=user,
                        text=text,
                        description=description,
                        date_created=date_created,
                        answers=answers)
            return jsonify(resp), 200

    def put(self, question_id):
        """This function edits a question, given the id"""
        auth_header = request.headers.get('Authorization')
        if not auth_header or len(auth_header) < 8 or " " not in auth_header:
            raise BadRequest
        auth_token = auth_header.split(" ")[1]
        request_id = UserModel().decode_auth_token(auth_token)
        if isinstance(request_id, str):
            raise Unauthorized
        else:
            # confirm user request
            questions = QuestionModel()
            question = questions.get_item_by_id(int(question_id))
            if question == "Not found":
                raise NotFound
            question_id = question[0]
            user_id = question[1] 
            try:
                text = request.get_json()['text']
            except Exception:
                raise BadRequest
            if int(user_id) == int(request_id):
                # update question
                questions.update_item(field='text', data=text,
                                      item_id=int(question_id))
            else:
                raise Forbidden("You are not allowed to edit the question")
            resp = {"message":"success", "text":text}
            return jsonify(resp), 200

    def delete(self, question_id):
        """This function deletes a question, given the id"""
        auth_header = request.headers.get('Authorization')
        if not auth_header or len(auth_header) < 8 or " " not in auth_header:
            raise BadRequest
        auth_token = auth_header.split(" ")[1]
        response = UserModel().decode_auth_token(auth_token)
        if isinstance(response, str):
            raise Unauthorized
        else:
            # user is authorized
            questions = QuestionModel()
            question = questions.get_item_by_id(int(question_id))
            if question == "Not found":
                raise NotFound
            question_id = question[0]
            user_id = question[1]           
            # check if user ids match
            if int(user_id) == int(response):
                # delete question
                questions.delete_item(int(question_id))
            else:
                raise Forbidden("You are not allowed to delete the question")
            resp = {"message":"success", 
                    "description":"question deleted succesfully"}
            return jsonify(resp), 202

class GetUserQuestion(MethodView):
    """question views associated with users"""
    def get(self, username):
        """returns all the questions associated with a particular user"""
        """This function deletes a question, given the id"""
        users = UserModel()
        user_id  = users.get_user_by_username(username)[0]
        if not user_id:
            # user does not exist
            raise NotFound("The username provided does not exist")
        quest = QuestionModel()
        questions = quest.get_items_by_id(item='user',
                                          item_id=int(user_id))
        list_of_questions = []

        if not questions:
            # no question was not found
            raise NotFound
    
        if not isinstance(questions, list):
            list_of_questions.append(questions)
        else:
            list_of_questions = questions[:]
         
        resp = {
            "message":"success",
            "username":username,
            "questions":questions
        }
        return jsonify(resp), 200
