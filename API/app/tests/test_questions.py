import os
import sys
import unittest
import json

# local imports
from app import create_app
from app import data as test_data


class QuestionsTests(unittest.TestCase):
    """This class collects all the test cases for the questions"""
    def setUp(self):
        """Performs variable definition and app initialization"""
        self.app = create_app()
        self.client = self.app.test_client()
        self.question =  {
            "text":"How do you declare an integer variable in Java?",
            "asked_by":"Jimmy"
        }
        self.answer =  {
            "text":"You do so by using the int keyword like so: int x;",
            "answered_by":"Jimmy"
        }
        with self.app.app_context():
            self.data = test_data

    def post_data(self, path, data):
        """This function performs a POST request using the testing client"""
        result = self.client.post(path, data=json.dumps(data),
                             content_type='applicaton/json')
        return result

    def get_data(self, path):
        """This function performs a GET request to a given path 
            using the testing client
        """
        result = self.client.get(path)
        return result

    def put_data(self, path, data):
        """This function performs a PUT request to a given path 
            using the testing client
        """
        result = self.client.put(path, data=json.dumps(data),
                             content_type='applicaton/json')
        return result

    def delete_data(self, path):
        """This function performs a DELETE request to a given path 
            using the testing client
        """
        result = self.client.delete(path)
        return result

    def test_post_question(self):
        """Test that a user can post a new question"""
        # post a question
        result = self.post_data('/api/v1/questions/', data=self.question)
        self.assertEqual(result.status_code, 201)
        # assert that the question is in the response
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
        result = self.get_data('/api/v1/questions/{}'.format(response['id']))
        # check that the server responds with the correct status code 
        self.assertEqual(result.status_code, 200)
        # test that the response contains the correct question
        self.assertIn(self.question['text'], str(result.data))

    def test_post_an_answer_to_a_question(self):
        """Test that the user can post an answer to a given question"""
        # create a question 
        new_question = self.post_data('/api/v1/questions/', data=self.question)
        self.assertEqual(new_question.status_code, 201)
        # convert response to JSON
        response = json.loads(new_question.data.decode('utf-8').replace("'", '"'))
        # post an answer to a question
        url='/api/v1/questions/{}/answers'.format(response['id'])
        result = self.post_data(url, data=self.answer)
        self.assertEqual(result.status_code, 201)
        # the response should contain the question id and the answer
        response2 = json.loads(result.data.decode('utf-8').replace("'", '"'))
        self.assertEqual("{}".format(response['id']), response2['question_id'])
        self.assertEqual("{}".format(self.answer['text']), response2['text'])
    
    def test_edit_question(self):
        """Test whether the user can edit a question"""
        # create a question 
        new_question = self.post_data('/api/v1/questions/', data=self.question)
        self.assertEqual(new_question.status_code, 201)
        question = json.loads(new_question.data.decode('utf-8').replace("'", '"'))
        question_id = question['id']
        # edit the question by splitting it into 2
        size = len(question['text'])//2
        edited_question_text = question['text'][:size]
        # make PUT request to the endpoint
        result = self.put_data('/api/v1/questions/{}'.format(question_id), 
                                data = {"text":edited_question_text})
        # test that the request returns the right response
        self.assertEqual(result.status_code, 200)
        result = json.loads(result.data.decode('utf-8').replace("'", '"'))
        # test that the request returns the edited question
        self.assertEqual(edited_question_text, result['text'])
        # test that the function edits the data
        response = self.get_data('/api/v1/questions/{}'.format(question_id))
        response = json.loads(response.data.decode('utf-8').replace("'", '"'))
        self.assertEqual(edited_question_text, response['text'])


    def test_delete_question(self):
        """Test that the user can delete a question"""
        # create a question 
        new_question = self.post_data('/api/v1/questions/', data=self.question)
        self.assertEqual(new_question.status_code, 201)
        question_id = json.loads(
            new_question.data.decode('utf-8').replace("'", '"'))['id']
        response = self.delete_data('/api/v1/questions/{}'.format(question_id))
        # test that the right response code is returned
        self.assertEqual(response.status_code, 200)
        # test that the data store does not have the question
        response = self.get_data('/api/v1/questions/{}'.format(question_id))
        self.assertEqual(response.status_code, 404)
        
    def tearDown(self):
        """This function destroys all the variables 
        that have been created during the test
        """
        del self.question
        del self.answer
        del self.data


if __name__ == "__main__":
    unittest.main()