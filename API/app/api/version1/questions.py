"""
This module defines the routes of the questions resource and the accompanying view functions

Authored by: Ricky Nyairo
"""

# standard imports
import json
from datetime import datetime

# third party imports
from werkzeug.exceptions import NotFound, BadRequest
from flask import request, jsonify, make_response

# local imports
from app import _locate
from app.data import data
from . import version1

@version1.route('/questions/',
                 methods=['POST', 'GET'], strict_slashes=False)
def get_questions():
    """This function handles request to the questions resource"""
    if request.method == 'GET':
        # return all questions in the db
        response = make_response(jsonify(data['questions']), 200)

    elif request.method == 'POST':
        # return the new question with the assigned question id
        # try to access the local data store to locate the last
        # and allocate the new question an id
        try:
            question_id = int(data["questions"][-1]['question_id']) + 1
        # if that fails, there is no data in the data store
        # assign id = 1
        except IndexError:
            question_id = "1"

        req_data = json.loads(request.data.decode('utf-8').replace("'", '"'))
        # validation
        try:
            question_text = req_data['text']
            asked_by = req_data['asked_by']

        except (IndexError, KeyError):
            raise BadRequest

        if not req_data["text"] or not req_data["asked_by"]:
            raise BadRequest

        date = '{:%B %d, %Y}'.format(datetime.now())
        new_question = {
            "question_id":str(question_id),
            "text":question_text,
            "asked_by":asked_by,
            "date":date,
            "answers":[]
        }
        data['questions'].append(new_question)
        response = make_response(jsonify(new_question), 201)

    return response

@version1.route('/questions/<int:ques_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def get_question(ques_id):
    """This function, given a particular question id,
        retrieves the question or edits the question"""
    response = {}
    # locate the question
    question, index = _locate(int(ques_id), "questions")

    if question is None:
        # question not found
        # raise error 404
        raise NotFound

    if request.method == 'GET':
        # return the question
        response = make_response(jsonify(question), 200)

    elif request.method == 'PUT':
        # obtain the required edit
        edited_question = json.loads(request.data.decode('utf-8').replace("'", '"'))['text']
        # edit the question in the data store
        question['text'] = edited_question
        response = make_response(jsonify({
            "question_id":ques_id,
            "text":edited_question
            }), 200)
    else:
        # delete the question
        del data["questions"][index]
        response = make_response(jsonify({
            "question_id":ques_id,
            "action":"deleted"
            }), 200)

    return response

@version1.route('/questions/<int:ques_id>/answers',
                 methods=['POST'], strict_slashes=False)
def post_answer(ques_id):
    """ This function allows the user to post an answer
    to a particular question, given the question id """

    answer = json.loads(request.data.decode('utf-8').replace("'", '"'))
    # initialize up votes to 0
    answer['up_votes'] = "0"
    # locate the question
    question = _locate(int(ques_id), "questions")[0]
    if not question:
        # the question with the given id was not found
        # raise error 404
        raise NotFound
    else:
        # question is located, append answer
        question['answers'].append(answer)
        # return a response with the question id and the answer
        response = make_response(jsonify({
            "question_id":question['question_id'],
            "text":answer['text'],
            }), 201)
        return response
