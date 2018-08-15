from flask import Flask
import json
from flask import request, jsonify, abort
from datetime import datetime

def create_app():
    app=Flask(__name__)

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
            req_data = json.loads(request.data.decode('utf-8').replace("'", '"'))
            # import pdb; pdb.set_trace()
            question_text = req_data['text']
            asked_by = req_data['asked_by']
            date = '{:%B %d, %Y}'.format(datetime.now())
            new_question = {
                "id":question_id,
                "text":question_text,
                "asked_by":asked_by,
                "date":date
            }
            data['questions'].append(new_question)
            response = jsonify(new_question)
            response.status_code = 201

        return response
        
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
            "answers":["100000km-000","384000km-020"],
            "date":"December 17, 2017"
        },
        {
            "id":"1001",
            "text":"Who was the first Kenyan president?",
            "askedBy":"Nancy",
            "answers":["Jomo Kenyatta-100","Uhuru Kenyatta-020","Mwai Kibaki-060", "Raila Odinga-000"],
            "date":"August 17, 2017"
        }, 
        {
            "id":"1002",
            "text":"What are the most popular programming languages?",
            "askedBy":"Ricky",
            "answers":["JavaScript-100","Python-020","Java-060", "Fortran-000"],
            "date":"August 17, 2017"
        }
    ]
}