# StackOverflow-lite

## Introduction

StackOverflow-Lite is a platform for sharing questions and answers. 

[![Coverage Status](https://coveralls.io/repos/github/rickynyairo/StackOverflow-lite/badge.svg?branch=development)](https://coveralls.io/github/rickynyairo/StackOverflow-lite?branch=development)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![Website naereen.github.io](https://img.shields.io/website-up-down-green-red/https/naereen.github.io.svg)](https://rickynyairo.github.io/StackOverflow-lite/)
[![PyPI version](https://badge.fury.io/py/Flask.svg)](https://badge.fury.io/py/Flask)
[![Build Status](https://travis-ci.org/rickynyairo/StackOverflow-lite.svg?branch=development)](https://travis-ci.org/rickynyairo/StackOverflow-lite)

### Code Climate

[![Maintainability](https://api.codeclimate.com/v1/badges/13a7eb6d1036b235a820/maintainability)](https://codeclimate.com/github/rickynyairo/StackOverflow-lite/maintainability)

### Features

1. Users can create an account and log in.
2. Users can post questions.
3. Users can delete the questions they post.
4. Users can post answers.
5. Users can view the answers to questions.
6. Users can accept an answer out of all the answers to his/her question as the preferred answer. 

### Installing

Clone the repository [```here```](https://github.com/rickynyairo/StackOverflow-lite/)

### Testing

*To test the UI:*
Navigate to the UI directory
On your preferred browser, open index.html
Alternatively, the site is [```hosted here```](https://rickynyairo.github.io/StackOverflow-lite/)

*To test the API:*
Navigate to the API/ directory
In a virtual environment, perform the following:

>git checkout development

>pip install -r requirements.txt

>nosetests app/tests

>python run.py

### API-Endpoints

#### Heroku Hosting link

```https://stackoverflow-lite99.herokuapp.com/api/v2```

#### Version 1 

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/479da9f494c39acebfd6)

#### Users Endpoints : /api/v1/

Method | Endpoint | Functionality
--- | --- | ---
POST | /api/v1/users/signup | Creates a user account
POST | /api/v1/users/signin | Sign in a user
GET | /api/v1/users | Get a list of all users


#### Questions Endpoints

Method | Endpoint | Functionality
--- | --- | ---
POST | /api/v1/questions | Post a question
POST | /api/v1/questions/int:ques_id/answers | post an answer to a question
GET | /api/v1/questions | Get a List of all questions
GET | /api/v1/questions/int:ques_id | Get a question using its id
PUT | /api/v1/questions/int:ques_id | Edit a question


#### Version 2

#### Users Endpoints : /api/v2/

Method | Endpoint | Functionality
--- | --- | ---
POST | /auth/signup | Creates a user account
POST | /users/login | Sign in a user

#### Questions Endpoints : /api/v2/

Method | Endpoint | Functionality
--- | --- | ---
POST | questions | Post a question
POST | /questions/int:ques_id/answers | post an answer to a question
GET | /questions | Get a List of all questions
GET | /questions/int:ques_id | Get a question using its id
PUT | /questions/int:ques_id | Edit a question
DELETE | /questions/int:ques_id | Delete a question using its id
POST | /questions/int:ques_id/answers | Post an answer to a question
PUT | /questions/int:ques_id/answers/int:ans_id | Edit an answer

### Questions
[![Ask Me Anything !](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)](https://GitHub.com/Naereen/ama)




