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
            "password":"¥«,Â\u008aÝ"
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
        new_user = self.post_data("/api/v1/users/", data=self.user)
        # test that the server responds with the correct status code
        self.assertEqual(new_user.status_code, 201)
        # test that the correct user is created
        self.assertEqual(self.user['username'], new_user.json['username'])

    def test_get_all_users(self):
        """Test that the API responds with a list of all the users"""
        # create a new user
        new_user = self.post_data("/api/v1/users/", data=self.user)
        self.assertEqual(new_user.status_code, 201)

        user_id = new_user.json['id']
        username = new_user.json['username']

        result = self.get_data("/api/v1/users/")
        self.assertEqual(result.status_code, 200)
        self.assertNotEqual(result.status_code, 404)
        result = json.loads(result.data.decode().replace("'", '"'))

        self.assertIn(username, str(result))
        self.assertIn(user_id, str(result))        

    def test_error_handling_for_not_found(self):
        """Test that the user resource sends an error message when a resource is not found
        """
        # test that a non existent user cannot be accessed
        new_user = self.post_data('/api/v1/users/', data=self.user)
        self.assertEqual(new_user.status_code, 201)
        user_id = new_user.json['id']
        # obtain an errorneous id
        erroneous_id = int(user_id) * int(user_id)

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
            result = self.post_data('/api/v1/users/', data=bad_req)
            # assert correct status code
            self.assertEqual(result.status_code, 400)
            # assert correct error message
            self.assertEqual(result.json["message"], "The request made had errors, please check the headers or params")

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