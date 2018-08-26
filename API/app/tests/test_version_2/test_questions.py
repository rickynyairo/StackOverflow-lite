"""
This module tests the questions end point
"""
import unittest
import json
import string
from random import choice, randint

# local imports
from ... import create_app, init_db
from ...api.version2.models.user_model import UserModel



class TestQuestions(unittest.TestCase):
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

    def setUp(self):
        """Performs variable definition and app initialization"""
        self.app = create_app()
        self.client = self.app.test_client()
        self.user_id, self.user = self.create_user()
        self.auth_token = self.user.encode_auth_token(self.user_id).decode('utf-8')
        self.question = {
            "text":"What is the fastest programming language and why?",
            "description":"I am looking for the fastest programming language in terms\
                            of memory management for a very high performance project."
        }
        self.app = create_app()
        with self.app.app_context():
            self.db = init_db()

    def post_data(self, path='/api/v2/questions', auth_token=2, data={}, headers=0):
        """This function performs a POST request using the testing client"""
        if not data:
            data = self.question
        if auth_token is 2:
            auth_token = self.auth_token
        if not headers:
            headers = {"Authorization":"Bearer {}".format(auth_token)}
        result = self.client.post(path, data=json.dumps(data),
                                  headers=headers,
                                  content_type='applicaton/json')
        return result

    def get_data(self, path='/api/v2/questions'):
        """This function performs a GET request to a given path
            using the testing client
        """
        result = self.client.get(path)
        return result

    def test_post_question(self):
        """Test that a user can post a question
        """
        new_question = self.post_data()
        # test that the server responds with the correct status code
        self.assertEqual(new_question.status_code, 201)
        self.assertTrue(new_question.json['message'])
        question_id =  new_question.json['question_id']
        # test that the correct question is created
        dbconn = self.db
        curr = dbconn.cursor()
        curr.execute("SELECT text FROM questions\
                     WHERE question_id = %d" % (int(question_id)))
        question_text = curr.fetchone()[0]
        self.assertEqual(self.question['text'], question_text)
        
    def test_error_messages(self):
        """Test that the endpoint responds with the correct error message"""
        empty_req = self.client.post("/api/v2/questions",
                                     headers=dict(Authorization="Bearer {}".format(self.auth_token)),
                                     data={})
        self.assertEqual(empty_req.status_code, 400)
        bad_data = self.question
        del bad_data['text']
        empty_params = self.post_data(data=bad_data)
        self.assertEqual(empty_params.status_code, 400)
        empty_req = self.post_data(data={"":""})
        self.assertEqual(empty_req.status_code, 400)
        bad_data = {
            "user_id":"",
            "textsss":"What is the fastest programming language and why?",
            "description":"Description"
        }
        bad_req = self.post_data(data=bad_data)
        self.assertEqual(bad_req.status_code, 400)
    
    def test_unauthorized_request(self):
        """Test that the endpoint rejects unauthorized requests"""
        # test false token
        false_token = self.post_data(headers=dict(Authorization="Bearer wrongtoken"))
        self.assertEqual(false_token.status_code, 400)
        # test correct token
        correct_token = self.post_data()
        self.assertEqual(correct_token.status_code, 201)

    def test_get_questions(self):
        """Test that the api can respond with a list of questions"""
        new_question = self.post_data()
        questions = self.get_data().json
        self.assertEqual(questions['message'], 'success')
        self.assertIn(new_question.json['text'], str(questions['questions']))

    def test_get_questions_associated_to_user(self):
        """Test that the API responds with all the questions of a particular user"""
        user_id, user = self.create_user()
        question = self.post_data(headers={"Authorization":"Bearer {}".format(self.auth_token)})
        username = self.user.get_username_by_id(self.user_id)
        path = "/api/v2/questions/{}".format(username)
        req = self.get_data(path=path)
        self.assertEqual(req.status_code, 200)
        self.assertEqual(username, req.json["username"])
    
    def test_edit_question(self):
        """Test that a user can edit the text of a question that they've posted"""
        question_id = int(self.post_data().json['question_id'])
        headers = {"Authorization":"Bearer {}".format(self.auth_token)}
        path  = "/api/v2/questions/{}".format(question_id)
        data = {"text":"edited question"}
        result = self.client.put(path,
                                 headers=headers,
                                 data=json.dumps(data),
                                 content_type='application/json')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json['text'], data['text'])

    def test_delete_question(self):
        """Test that a user can delete a question that they have posted"""
        question_id = int(self.post_data().json['question_id'])
        headers = {"Authorization":"Bearer {}".format(self.auth_token)}
        path  = "/api/v2/questions/{}".format(question_id)
        result = self.client.delete(path,
                                    headers=headers,
                                    content_type='application/json')
        self.assertEqual(result.status_code, 202)
        self.assertEqual(result.json['message'], 'success')

    def tearDown(self):
        """This function destroys objests created during the test run"""
        curr = self.db.cursor()
        exit_query = "DELETE FROM questions WHERE user_id = %d;" % (self.user_id)
        curr.execute(exit_query)
        exit_query = "DELETE FROM users WHERE user_id = %d;" % (self.user_id)
        curr.execute(exit_query)
        curr.close
        self.db.commit()
        del self.question
        with self.app.app_context():
            self.db.close()

if __name__ == "__main__":
    unittest.main()
