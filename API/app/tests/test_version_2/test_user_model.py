"""
This module tests the user model

"""
import unittest
import json
import string
from random import choice, randint

# local imports
from ... import create_app, init_db
from ...api.version2.users.user_models import UserModel

class TestUserModel(unittest.TestCase):
    """This class encapsulates the tests for the user model
    """
    def setUp(self):
        """Define the data to be used for the test
        """
        self.user = {
                "username":"".join(choice(
                                string.ascii_letters) for x in range (randint(7,10))),
                "first_name":"ugali",
                "last_name":"mayai",
                "email":"ugalimayai@gmail.com",
                "password":"password"
            }
        self.app = create_app()

        with self.app.app_context():
            self.db = init_db()
 
    def test_that_user_can_be_created(self):
        """Test that the user model can create a user"""
        params = self.user
        user = UserModel(**params)
        # save the user to the db
        user.save_user()
        curr = self.db.cursor()
        curr.execute("SELECT email FROM users\
                     WHERE username = '%s';" % (self.user['username']))
        user_email = curr.fetchone()[0]
        self.assertEqual(self.user['email'], user_email)
    
    def test_that_user_can_be_deleted(self):
        """Test that the user model can delete a user"""
        params = self.user
        username = self.user['username']
        user = UserModel(**params)
        user.save_user()
        user_id = user.get_id()[0]
        user.delete_user(user_id)
        curr = self.db.cursor()
        query = "SELECT user_id FROM users WHERE user_id = %d;" % (int(user_id))
        curr.execute(query)
        data = curr.fetchone()
        self.assertEqual(None, data)
    
    def test_encode_user_token(self):
        """Test that the user model can encode a JWT token, given a user_id"""
        params = self.user
        user = UserModel(**params)
        user.save_user()
        user_id = int(user.get_id()[0])
        token = user.encode_auth_token(user_id)
        self.assertTrue(isinstance(token, bytes))

    def test_decode_user_token(self):
        """Test that the user model can decode an authentication token"""
        params = self.user
        user = UserModel(**params)
        user.save_user()
        user_id = int(user.get_id()[0])
        token = user.encode_auth_token(user_id)
        decoded_sub = user.decode_auth_token(token)
        self.assertTrue(decoded_sub)
        self.assertEqual(decoded_sub, user_id)

    def tearDown(self):
        """This function destroys objests created during the test run"""
        curr = self.db.cursor()
        exit_query = "DELETE FROM users WHERE email = '%s';" % (self.user['email'])
        curr.execute(exit_query)
        curr.close()
        self.db.commit()
        del self.user
        with self.app.app_context():
            self.db.close()

if __name__ == "__main__":
    unittest.main()

