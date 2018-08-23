"""
This module tests the answers end point
"""
import unittest
import json
import string
from random import choice, randint

# local imports
from ... import create_app, init_db
from ...api.version2.users.user_models import UserModel
from ...api.version2.questions.question_models import QuestionModel
from ...api.version2.answers.answers_models import AnswerModel

class TestAnswers(unittest.TestCase):
    """This class collects all the test cases for the questions"""
    def create_user(self):
        """create a fictitious user"""
        username = "".join(choice(
                           string.ascii_letters) for x in range (randint(7,10)))
        params = {
                "username":username,
                "first_name":"ugali",
                "last_name":"mayai",
                "email":"ugalimayai@gmail.com",
                "password":"password"
            }       
        user = UserModel(**params)
        user_id = user.save_user()
        return user_id, user

    def create_question(self, user_id):
        """This function sets up a test question in the db
        """
        params = {
            "user_id":user_id,
            "text":"What is the fastest programming language and why?",
            "description":"I am looking for the fastest programming language in terms\
                            of memory management for a very high performance project."
        }
        question = QuestionModel(**params)
        question_id = question.save_question()
        return question_id, question

    def setUp(self):
        """Performs variable definition and app initialization"""
        self.app = create_app()
        self.client = self.app.test_client()
        self.user_id, user = self.create_user()
        self.auth_token = user.encode_auth_token(self.user_id).decode('utf-8')
        self.question = {
            "user_id":self.user_id,
            "text":"What is the fastest programming language and why?",
            "description":"I am looking for the fastest programming language in terms\
                            of memory management for a very high performance project."
        }
        self.question_id, ques = self.create_question(self.user_id)
        self.answer = {
            "question_id":self.question_id,
            "user_id":self.user_id,
            "text":"Julia. It has everything awesome about every great programming language, and more."
        }
        self.app = create_app()
        with self.app.app_context():
            self.db = init_db()

    def post_data(self, question_id=0, auth_token=2, data={}, headers=0):
        """This function performs a POST request using the testing client"""
        if not data:
            data = self.answer
        if auth_token is 2:
            auth_token = self.auth_token
        if not headers:
            headers = {"Authorization":"Bearer {}".format(auth_token)}
        if not question_id:
            question_id = self.answer['question_id']
        path = "/api/v2/questions/{}/answers".format(question_id)
        result = self.client.post(path, data=json.dumps(data),
                                  headers=headers,
                                  content_type='applicaton/json')
        return result

    def test_post_answer(self):
        """Test that a user can post a answer
        """
        new_answer = self.post_data()
        # test that the server responds with the correct status code
        self.assertEqual(new_answer.status_code, 201)
        self.assertTrue(new_answer.json['message'])
        
    def test_error_messages(self):
        """Test that the endpoint responds with the correct error message"""
        question_id = self.answer['question_id']
        path = "/api/v2/questions/{}/answers".format(question_id)
        empty_req = self.client.post(path,
                                     headers=dict(Authorization="Bearer {}".format(self.auth_token)),
                                     data={})
        self.assertEqual(empty_req.status_code, 400)
        bad_data = self.answer
        del bad_data['text']
        empty_params = self.post_data(data=bad_data)
        self.assertEqual(empty_params.status_code, 400)
        empty_req = self.post_data(data={"":""})
        self.assertEqual(empty_req.status_code, 400)
    
    def test_unauthorized_request(self):
        """Test that the endpoint rejects unauthorized requests"""
        # test false token
        false_token = self.post_data(headers=dict(Authorization="Bearer wrongtoken"))
        self.assertEqual(false_token.status_code, 400)
   
    def tearDown(self):
        """This function destroys objests created during the test run"""
        curr = self.db.cursor()
        exit_query = "DELETE FROM answers WHERE user_id = %d;" % (self.user_id)
        curr.execute(exit_query)
        curr.close
        self.db.commit()
        del self.answer
        with self.app.app_context():
            self.db.close()

if __name__ == "__main__":
    unittest.main()
