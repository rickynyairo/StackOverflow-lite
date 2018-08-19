"""
This module tests the users resource thoroughly to ensure correct API functionality

Authored by: Ricky Nyairo
"""
import unittest
import json

# local imports
from app import create_app
from app import data as test_data

class UserTests(unittest.TestCase):
    """This class collects all the test cases for the users"""
    def setUp(self):
        """Performs variable definition and app initialization"""
        self.app = create_app()
        self.client = self.app.test_client()
        self.user = {
            "email":"ugalimayai@gmail.com",
            "username":"ugalimayai",
            "password":"password"
        }
        self.error_msg = "The path accessed / resource requested cannot be found, please check"
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

    def test_create_user(self):
        """Test that a new user is created using a POST request
        """
        new_user = self.post_data("/api/v1/users/signup", data=self.user)
        # test that the server responds with the correct status code
        self.assertEqual(new_user.status_code, 201)
        # test that the correct user is created
        self.assertEqual(self.user['username'], new_user.json['username'])

    def test_get_all_users(self):
        """Test that the API responds with a list of all the users"""
        # create a new user
        new_user = self.post_data("/api/v1/users/signup", data=self.user)
        self.assertEqual(new_user.status_code, 201)

        user_id = new_user.json['user_id']
        username = new_user.json['username']

        result = self.get_data("/api/v1/users/")
        self.assertEqual(result.status_code, 200)
        self.assertNotEqual(result.status_code, 404)
        result = json.loads(result.data.decode().replace("'", '"'))

        self.assertIn(username, str(result))
        self.assertIn(user_id, str(result))

    def test_get_user_by_id(self):
        """Test that the API can respond with user details, given the id
        """
        # create user
        new_user = self.post_data("/api/v1/users/signup", data=self.user)
        self.assertEqual(new_user.status_code, 201)
        user_id = new_user.json['user_id']
        # obtain user details
        result = self.get_data('/api/v1/users/{}'.format(user_id))

        self.assertEqual(result.json['user_id'], user_id)
        self.assertNotEqual(result.status_code, 404)

    def test_error_handling_for_not_found(self):
        """Test that the user resource sends an error message when a resource is not found
        """
        # test that a non existent user cannot be accessed
        new_user = self.post_data('/api/v1/users/signup', data=self.user)
        self.assertEqual(new_user.status_code, 201)
        user_id = new_user.json['user_id']
        # obtain an errorneous id
        erroneous_id = int(user_id) + int(user_id)

        # an attempt to get a non-existing user should raise an error
        result = self.get_data('/api/v1/users/{}'.format(erroneous_id))
        self.assertEqual(result.status_code, 404)
        self.assertNotEqual(result.status_code, 200)

        # check that the right message is sent
        self.assertEqual(result.json['message'], self.error_msg)

    def test_error_handling_for_bad_requests(self):
        """Test that the users resource sends an error message when a bad request is made
        """
        list_of_bad_requests = [
            {"username":"jamie", "email":"", "password":"password"},
            {"username":"jamie", "email":"Jimmy@mail.com", "password":""},
            {"username":"jamie", "email":"Jimmy@mailcom", "password":"password"},
            {"username":"jamie", "email":"Jimmymail.com", "password":""}
        ]
        for bad_req in list_of_bad_requests:
            result = self.post_data('/api/v1/users/signup', data=bad_req)
            # assert correct status code
            self.assertEqual(result.status_code, 400)
            # assert correct error message
            self.assertEqual(result.json["message"],
                             "The request made had errors, please check the headers or params")


    def test_user_sign_up_and_sign_in(self):
        """Test that a new user can sign up for an account and sign in
        """
        new_user = self.post_data('/api/v1/users/signup/', data=self.user)

        # API should respond with a success message and the allocated user id
        self.assertEqual(new_user.status_code, 201)
        # user_id = new_user.json['user_id']
        message = new_user.json['message']

        # test that message was a success
        self.assertEqual(message, "User signed up successfully")

        # attempt unauthorized sign in
        user = {
            "username":self.user['username'],
            "password":self.user['password']
        }
        unauthorized_user = user
        unauthorized_user['password'] = user['password'][::-1]

        unauthorized_user_signin = self.post_data('/api/v1/users/signin', data=unauthorized_user)
        self.assertEqual(unauthorized_user_signin.status_code, 400)
        self.assertEqual(unauthorized_user_signin.json['message'],
                         "You are not authorized to access this resource, please confirm credentials")

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
