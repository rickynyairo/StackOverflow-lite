"""
This module collects the views for the answers resource

"""
import json

# third party imports
from flask_restplus import Resource
from flask import request, jsonify
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized, Forbidden

from ..models.user_model import UserModel
from ..models.question_model import QuestionModel
from ..models.answer_model import AnswerModel

from ..utils.serializers import AnswerDTO

api = AnswerDTO().api
_n_answer = AnswerDTO().n_answer
_n_answer_resp = AnswerDTO().n_answer_resp
_edit_answer_resp = AnswerDTO().edit_answer_resp
_vote_ans = AnswerDTO().up_votes

@api.route('/')
class Answers(Resource):
    """This class collects the methods for the answers endpoint"""

    docu_string = "This endpoint handles POST requests to the answers resource"
    @api.doc(docu_string)
    @api.expect(_n_answer, validate=True)
    @api.marshal_with(_n_answer_resp, code=201)
    def post(self, question_id):
        """This endpoint handles POST requests to the answers resource"""
        auth_header = request.headers.get('Authorization')
        if not auth_header or not request.data:
            raise BadRequest("The request is malformed. Attach missing fields")
        auth_token = auth_header.split(" ")[1]
        response = UserModel().decode_auth_token(auth_token)
        if not isinstance(response, str):
            # the token decoded succesfully
            user_id = response
            req_data = json.loads(request.data.decode().replace("'", '"'))
            text = req_data['text']
            # save answer in db
            answer = AnswerModel(int(question_id), int(user_id), text)
            check = answer.check_text_exists(text)
            if isinstance(check, int):
                # asnwer exists in the db
                raise Forbidden("The answer exists in the database with id: %d"%(check))
            answer_id = int(answer.save_answer())
            answer.close_db() 
            resp = {
                "message":"success",
                "text":text,
                "answer_id":answer_id
            }
            return resp, 201
        else:
            # token is either invalid or expired
            raise Unauthorized

@api.route("/<int:answer_id>")
class GetAnswer(Resource):
    """This class encapsulates the method functions for a particular answer"""

    docu_string = "This endpoint handles PUT requests to the answers resource"
    @api.doc(docu_string)
    @api.expect(_n_answer, validate=False)
    @api.marshal_with(_edit_answer_resp)
    def put(self, question_id, answer_id):
        """
        This function is restricted to the author of the answer and the author of the question to edit or mark an answer as preferred. 
        The ```answer_author_id``` is allowed to edit the answer. 
        The ```question_author_id``` is allowed to mark the answer as preferred
        """
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise BadRequest("This endpoint requires authorization")
        auth_token = auth_header.split(" ")[1]
        response = UserModel().decode_auth_token(auth_token)
        if isinstance(response, str):
            # the user is not authorized to view this endpoint
            raise Unauthorized("You are not allowed to access this resource")
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
                raise Forbidden("You are not athorized to edit this answer")
            resp = {
                "message":"success",
                "description":"answer updated succesfully",
                "value":value
            }
            return resp, 200

@api.route("/<int:answer_id>/vote")
class GetAnswer(Resource):
    """This class encapsulates the vote function for a particular answer"""
    docu_string = "This endpoint handles PUT requests to the answers resource"
    @api.doc(docu_string)
    @api.expect(_vote_ans, validate=True)
    @api.marshal_with(_edit_answer_resp, 200)
    def put(self, question_id, answer_id):
        """
        This endpoint allows an authorized user to upvote or downvote an answer
        """
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise BadRequest("This endpoint requires authorization")
        auth_token = auth_header.split(" ")[1]
        response = UserModel().decode_auth_token(auth_token)
        if isinstance(response, str):
            # the user is not authorized to access this endpoint
            raise Unauthorized("You are not allowed to access this resource")
        else:
            # vote for the answer
            # find the question and answer 
            answers = AnswerModel()
            find_qstn = QuestionModel().get_item_by_id(question_id)
            find_ans = answers.get_item_by_id(answer_id)
            if find_qstn == "Not Found" or find_ans == "Not Found":
                # the question or answer was not found
                raise NotFound("the question or answer was not found")
            vote = int(request.get_json()["vote"])
            if vote not in [-1, 1]:
                raise BadRequest("Upvote value not allowed")
            votes_for_answer = answers.vote_answer(answer_id, vote)
            resp = {
                "message":"success",
                "description":"answer updated succesfully",
                "value":str(votes_for_answer)
            }
            return resp, 200
