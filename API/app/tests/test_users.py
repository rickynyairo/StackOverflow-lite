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
            "id":"2",
            "email":"ugalimayai@gmail.com",
            "username":"ugalimayai",
            "password":"¥«,Â\u008aÝ"
        }
        with self.app.app_context():
            self.data = test_data

    def post_data(self, path, data):
        """This function performs a POST request using the testing client"""
        result = self.client.post(path, data=json.dumps(data),
                             content_type='applicaton/json')
        return result

    def test_create_user(self):
        """Test that a new user is created using a POST request
        """
        new_user = self.post_data("/api/v1/users/", data=self.user)
        # test that the server responds with the correct status code
        self.assertEqual(new_user.status_code, 201)
        # test that the correct user is created
        self.assertEqual(self.user['username'], new_user.json['username'])

    def tearDown(self):
        """This function destroys all the variables 
        that have been created during the test
        """
        del self.user
        del self.data


if __name__ == "__main__":
    unittest.main()