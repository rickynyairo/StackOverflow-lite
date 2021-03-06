"""
This module tests the questions resource thoroughly to ensure correct API functionality

Authored by: Ricky Nyairo
"""
import unittest
import json

# local imports
from ... import create_app
from ... import data as test_data


class QuestionsTests(unittest.TestCase):
    """This class collects all the test cases for the questions"""
    def setUp(self):
        """Performs variable definition and app initialization"""
        self.app = create_app()
        self.client = self.app.test_client()
        self.question = {
            "text":"How do you declare an integer variable in Java?",
            "asked_by":"Jimmy"
        }
        self.answer = {
            "text":"You do so by using the int keyword like so: int x;",
            "answered_by":"Jimmy"
        }
        self.error_msg = "The path accessed / resource requested cannot be found, please check"
        with self.app.app_context():
            self.data = test_data

    def post_data(self, path='/api/v1/questions/', data={}):
        """This function performs a POST request using the testing client"""
        if not data:
            data = {
            "text":"How do you declare an integer variable in Java?",
            "asked_by":"Jimmy"
            }
        result = self.client.post(path, data=json.dumps(data),
                                  content_type='applicaton/json')
        return result

    def get_data(self, path):
        """This function performs a GET request to a given path using the testing client
        """
        result = self.client.get(path)
        return result

    def put_data(self, path, data):
        """This function performs a PUT request to a given path using the testing client"""
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
        self.assertEqual(self.question['text'], result.json['text'])

    def test_get_questions(self):
        """Test that a user can obtain all the questions from the API"""
        new_question = self.post_data()
        self.assertEqual(new_question.status_code, 201)
        result = self.get_data('/api/v1/questions/')
        # assert that the server responds with the correct status code
        self.assertEqual(result.status_code, 200)
        self.assertIn(self.question['text'], str(result.data))

    def test_get_specific_question(self):
        """Test that the API can respond with a particular question, given the id"""
        # post a new question to get a question id in the response
        new_question = self.post_data()
        self.assertEqual(new_question.status_code, 201)
        # get json response
        response = new_question.json
        result = self.get_data('/api/v1/questions/{}'.format(response['question_id']))
        # check that the server responds with the correct status code
        self.assertEqual(result.status_code, 200)
        # test that the response contains the correct question
        self.assertIn(self.question['text'], str(result.data))

    def test_post_an_answer_to_a_question(self):
        """Test that the user can post an answer to a given question"""
        # create a question
        new_question = self.post_data()
        self.assertEqual(new_question.status_code, 201)
        # this is the response of the newly posted question
        response = new_question.json
        # post an answer to a question
        url = '/api/v1/questions/{}/answers'.format(response['question_id'])
        result = self.post_data(url, data=self.answer)
        self.assertEqual(result.status_code, 201)
        # the response should contain the question id and the answer text
        self.assertEqual("{}".format(response['question_id']), "{}".format(result.json['question_id']))
        self.assertEqual("{}".format(self.answer['text']), result.json['text'])

    def test_edit_question(self):
        """Test that the user can edit a question"""
        # create a question
        new_question = self.post_data()
        self.assertEqual(new_question.status_code, 201)
        question = new_question.json
        question_id = question['question_id']
        # edit the question by splitting it into 2
        size = len(question['text'])//2
        edited_question_text = question['text'][:size]
        # make PUT request to the endpoint
        result = self.put_data('/api/v1/questions/{}'.format(question_id),
                               data={"text":edited_question_text})
        # test that the request returns the right response
        self.assertEqual(result.status_code, 200)
        # test that the request returns the edited question
        self.assertEqual(edited_question_text, result.json['text'])
        # test that the function edits the data
        response = self.get_data('/api/v1/questions/{}'.format(question_id)).json
        self.assertEqual(edited_question_text, response['text'])


    def test_delete_question(self):
        """Test that the user can delete a question"""
        # create a question
        new_question = self.post_data('/api/v1/questions/', data=self.question)
        self.assertEqual(new_question.status_code, 201)
        question_id = new_question.json['question_id']
        response = self.delete_data('/api/v1/questions/{}'.format(question_id))
        # test that the right response code is returned
        self.assertEqual(response.status_code, 200)
        # test that the data store does not have the question
        response = self.get_data('/api/v1/questions/{}'.format(question_id))
        self.assertEqual(response.status_code, 404)

    def test_error_handling_for_not_found(self):
        """Test that the API sends back an error message when 404 errors are encountered"""
        # test that a non existent question cannot be accessed
        # post a question and obtain an id
        # create a question
        new_question = self.post_data('/api/v1/questions/', data=self.question)
        self.assertEqual(new_question.status_code, 201)
        question_id = new_question.json['question_id']
        # obtain an errorneous id
        erroneous_id = int(question_id) * int(question_id)
        result = self.get_data('/api/v1/questions/{}'.format(erroneous_id))
        self.assertEqual(result.status_code, 404)

        # attempting to post an answer to a non existent question
        # should raise an error
        result = self.post_data('/api/v1/questions/{}/answers'.format(erroneous_id),
                                data=self.answer)
        self.assertNotEqual(result.status_code, 200)
        # check that the right message is sent
        self.assertEqual(result.json['message'], self.error_msg)

    def test_error_handling_for_bad_requests(self):
        """Test that the API sends an appropriate error message when a bad request is made"""
        list_of_bad_requests = [
            {"text":"", "asked_by":"Jimmy"},
            {"text":"Question", "asked_by":""},
            {"asked_by":"Jimmy"},
            {"text":"Question"}
        ]
        for bad_req in list_of_bad_requests:
            result = self.post_data('/api/v1/questions/', data=bad_req)
            # assert correct status code
            self.assertEqual(result.status_code, 400)
            # assert correct error message
            self.assertEqual(result.json["message"],
                             "The request made had errors, please check the headers or parameters")

    def tearDown(self):
        """This function destroys all the variables
        that have been created during the test
        """
        del self.question
        del self.answer
        del self.data
        del self.error_msg


if __name__ == "__main__":
    unittest.main()
