import json

from datetime import datetime
from flask import request, jsonify, make_response
from . import questions
from app import _locate
from app.data import data
from werkzeug.exceptions import NotFound, BadRequest


@questions.route('/api/v1/questions/', methods=['POST', 'GET'])
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
            question_id = int(data["questions"][-1]['id']) + 1
        
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
            
        if len(req_data["text"]) == 0 or len(req_data["asked_by"]) == 0:
            raise BadRequest

        date = '{:%B %d, %Y}'.format(datetime.now())
        new_question = {
            "id":str(question_id),
            "text":question_text,
            "asked_by":asked_by,
            "date":date,
            "answers":[]
        }
        data['questions'].append(new_question)
        response = make_response(jsonify(new_question), 201)

    return response
    
@questions.route('/api/v1/questions/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def question(id, **kwargs):
    """This function, given a particular question id,
        retrieves the question or edits the question"""
    response = {}
    # locate the question
    q , index = _locate(int(id), "questions")
    
    if q is None:
        # question not found
        # return error 404
        raise NotFound

    if request.method == 'GET':
        # return the question
        response = make_response(jsonify(q), 200)

    elif request.method == 'PUT':
        # obtain the required edit
        edited_question = json.loads(request.data.decode('utf-8').replace("'", '"'))['text']
        # edit the question in the data store
        q['text'] = edited_question
        response = make_response(jsonify({
                    "id":id,
                    "text":edited_question
                }), 200)
    else:
        # delete the question
        del data["questions"][index]
        response = make_response(jsonify({
                    "question_id":id,
                    "action":"deleted"
                }), 200)

    return response

@questions.route('/api/v1/questions/<int:id>/answers', methods=['POST'])
def answer(id, **kwargs):
    """ This function allows the user to post an answer 
    to a particular question, given the question id """
    questions = data['questions']
    question = {} 
    answer = json.loads(request.data.decode('utf-8').replace("'", '"'))
    # initialize up votes to 0
    answer['up_votes'] = "0"
    # locate the question
    question = _locate(int(id), "questions")[0]
    if question:
        # question is located, append answer
        question['answers'].append(answer)
        # return a response with the question id and the answer
        response = make_response(jsonify({
            "question_id":question['id'],
            "text":answer['text'],                
            }), 201)
        return response         
    else:
        # the question with the given id was not found
        # raise error 404
        raise NotFound

