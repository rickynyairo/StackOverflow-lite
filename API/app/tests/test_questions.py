import os
import sys
import unittest
import json
from app import create_app

class QuestionsTests(unittest.TestCase):
    """This class collects all the test cases for the questions"""
    def setUp(self):
        """Performs variable definition and app initialization"""
        self.app=create_app()
        self.client = self.app.test_client()
        self.question =  {
            "text":"How do you declare an integer variable in Java?",
            "asked_by":"Jimmy"
        }
        self.answer =  {
            "text":"You do so by using the 'int' keyword like so:\nint x;",
            "answered_by":"Jimmy"
        }
    def post_data(self, path, data):
        """This function performs a post request using the testing client"""
        result = self.client.post(path, data=json.dumps(data),
                             content_type='applicaton/json')
        return result

    def get_data(self, path):
        """This function performs a get request using the testing client"""
        result = self.client.get(path, content_type='applicaton/json')
        return result

    def test_post_question(self):
        """Test that a user can post a new question"""
        result = self.post_data('/api/v1/questions/', data=self.question)
        self.assertEqual(result.status_code, 201)
        self.assertIn(self.question['text'], str(result.data))

    def test_get_questions(self):
        """Test that a user can obtain all the questions from the API"""
        new_question = self.post_data('/api/v1/questions/', data=self.question)
        self.assertEqual(new_question.status_code, 201)
        result = self.get_data('/api/v1/questions/')
        # assert that the server responds with the correct status code
        self.assertEqual(result.status_code, 200)
        self.assertIn(self.question['text'], str(result.data))

    def test_get_specific_question(self):
        """Test that the API can respond with a particular question, given the id"""
        # post a new question to get a question id in the response
        new_question = self.post_data('/api/v1/questions/', data=self.question)
        self.assertEqual(new_question.status_code, 201)
        # convert response to JSON
        response = json.loads(new_question.data.decode('utf-8').replace("'", '"'))
        result = self.get_data('/api/questions/{}'.format(response['id']))
        # check that the server responds with the correct status code 
        self.assertEqual(result.status_code, 200)
        # test that the response contains the correct question
        self.assertIn(self.question['text'], str(result.data))

    def test_post_an_answer_to_a_question(self):
        """This tests that the user can post an answer to a given question"""
        # create a question 
        new_question = self.post_data('/api/v1/questions/', data=self.question)
        self.assertEqual(new_question.status_code, 201)
        # convert response to JSON
        response = json.loads(new_question.data.decode('utf-8').replace("'", '"'))
        #post an answer to a question
        url='/api/v1/questions/{}/answers'.format(response['id'])
        result = self.post_data(url, data=self.answer)
        self.assertEqual(result.status_code, 201)
        #the response should contain the question id and the answer
        response = json.loads(result.data.decode('utf-8').replace("'", '"'))
        self.assertIn("{}".format(response['id']), str(response.data))
        self.assertIn("{}".format(self.answer['text']), str(response.data))

if __name__ == "__main__":
    unittest.main()