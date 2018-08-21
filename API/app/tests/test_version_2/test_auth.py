"""
This module tests the authentication endpoint

Authored by: Ricky Nyairo
"""
import unittest
import json

# local imports
from ... import create_app

class AuthTest(unittest.TestCase):
    """This class collects all the test cases for the users"""
    def setUp(self):
        """Performs variable definition and app initialization"""
        self.app = create_app()
        self.client = self.app.test_client()
        self.user = {
            "first_name":"ugali",
            "last_name":"mayai",
            "email":"ugalimayai@gmail.com",
            "username":"ugalimayai",
            "password":"password"
        }
        self.error_msg = "The path accessed / resource requested cannot be found, please check"
        self.data={}

    def post_data(self, path='/api/v2/auth/signup', data={}):
        """This function performs a POST request using the testing client"""
        if not data:
            data = {
            "username":"ugalimayai",
            "password":"password"
            }
        result = self.client.post(path, data=json.dumps(data),
                                  content_type='applicaton/json')
        return result

    def get_data(self, path):
        """This function performs a GET request to a given path
            using the testing client
        """
        result = self.client.get(path)
        return result

    def test_sign_up_user(self):
        """Test that a new user can sign up using a POST request
        """
        new_user = self.post_data("/api/v2/auth/signup", data=self.user)
        # test that the server responds with the correct status code
        self.assertEqual(new_user.status_code, 201)
        # test that the correct user is created
        # self.assertEqual(self.user['username'], new_user.json['username'])

    def test_error_messages(self):
        """Test that the endpoint responds with the correct error message"""
        empty_req = self.client.post("/api/v2/auth/signup", data={})
        self.assertEqual(empty_req.status_code, 400)

    def tearDown(self):
        """This function destroys all the variables
        that have been created during the test
        """
        del self.user
        del self.data
        del self.error_msg
        del self.client


if __name__ == "__main__":
    unittest.main()
