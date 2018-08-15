import pdb
import json
from datetime import datetime

#local imports
from flask import Flask
from flask import request, jsonify, abort


def create_app():
    app = Flask(__name__)

    @app.route('/api/v1/questions/', methods=['POST', 'GET'])
    def questions():
        """this route handles request to the questions resource"""
        if request.method == 'GET':
            # return all questions in the db
            response = jsonify(data['questions'])
            response.status_code = 200
        else: 
            # handles a POST request
            # return the new question with the question id
            question_id = int(data["questions"][-1]['id']) + 1
            req_data = json.loads(
                request.data.decode('utf-8').replace("'", '"'))
            question_text = req_data['text']
            asked_by = req_data['asked_by']
            date = '{:%B %d, %Y}'.format(datetime.now())
            new_question = {
                "id":question_id,
                "text":question_text,
                "asked_by":asked_by,
                "date":date,
                "answers":[]
            }
            data['questions'].append(new_question)
            response = jsonify(new_question)
            response.status_code = 201

        return response
        
    @app.route('/api/v1/questions/<int:id>', methods=['GET'])
    def question(id, **kwargs):
        """This function retrieves a question, given a particular id"""
        questions = data['questions']
        question = {}
        for q in questions:
            if int(q['id']) == int(id):
                question = q 
        
        if len(question) == 0:
            # question not found
            # return error 404
            abort(404)
        else:
            # return the question
            response = jsonify(question)
            response.status_code = 200

            return response

    @app.route('/api/v1/questions/<int:id>/answers', methods=['POST'])
    def answer(id, **kwargs):
        """ This function allows the user to post an answer 
        to a particular question, given the question id """
        questions = data['questions']
        question = {} 
        answer = json.loads(request.data.decode('utf-8').replace("'", '"'))
        # initialize up votes to 0
        answer['up_votes'] = "0"
        found = False
        for q in questions:
            if int(q['id']) == int(id):
                # append the received answer to the answers list
                found = True
                question = q
                question['answers'].append(answer)
        if found:
            # return a response with the question id and the answer
            response = jsonify({
                "question_id":str(question['id']),
                "text":answer['text'],                
            })
            response.status_code = 201
            return response         
        else:
            # the question with the given id was not found
            # return error 404
            abort(404)
            

    return app

data = {
    "users":[
        {
            "email":"john_doe@gmail.com",
            "username":"johndoe",
            "password":"¥«,Â\u008aÝ"
        },
        {
            "email":"rickynyairo@gmail.com",
            "username":"ricky",
            "password":"¥«,Â\u008aÝ"
        },

    ],
    "questions":[
        {
            "id":"1000",
            "text":"What is the distance from the earth to the moon?",
            "askedBy":"Jimmy",
            "answers":[
                {
                    "text":"384000 km",
                    "up_votes":"10000",
                    "answered_by":"Nancy"
                },
                {
                    "text":"100000km",
                    "up_votes":"20",
                    "answered_by":"Brian"
                }
            ],
            "date":"December 20, 2016"
        },
        {
            "id":"1001",
            "text":"Who was the first Kenyan president?",
            "askedBy":"Nancy",
            "answers":[
                {
                    "text":"Jomo Kenyatta",
                    "up_votes":"100",
                    "answered_by":"Ricky"
                },
                {
                    "text":"Uhuru Kenyatta",
                    "up_votes":"20",
                    "answered_by":"Jimmy"
                },
                {
                    "text":"Mwai Kibaki",
                    "up_votes":"0",
                    "answered_by":"John Doe"
                }
            ],
            "date":"August 17, 2017"
        }, 
        {
            "id":"1002",
            "text":"What are the most popular programming languages?",
            "askedBy":"Ricky",
            "answers":[
                {
                    "text":"JavaScript",
                    "up_votes":"100",
                    "answered_by":"Ecma"
                },
                {
                    "text":"Python",
                    "up_votes":"7000",
                    "answered_by":"Guido Van Rossum"
                },
                {
                    "text":"Java",
                    "up_votes":"0",
                    "answered_by":"Crazy Guy"
                }
            ],
            "date":"July 10, 2018"
        }
    ]
}