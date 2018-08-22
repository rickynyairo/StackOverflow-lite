"""
This module defines the user model and associated functions
"""
from datetime import datetime, timedelta

import jwt
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from .... import init_db, create_app

class UserModel(object):

    def __init__(self, username="u", first_name="i", last_name="o", password="p", email="1"):
        """initialize the user model"""
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = generate_password_hash(password)
        self.email = email
        self.date_created = datetime.now()
        self.db = init_db()
    
    def get_user_by_username(self, username):
        """return user from the db given a username"""
        database = self.db
        curr = database.cursor()
        curr.execute(
            """SELECT user_id, first_name, last_name, password, date_created \
            FROM users WHERE username = '%s'""" % (username))
        data = curr.fetchone()
        curr.close()
        return data

    def save_user(self):
        """Add user details to the database"""
        user = {
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password
        }
        # "date_created": self.date_created,

        database = self.db
        curr = database.cursor()
        query = """INSERT INTO users \
            VALUES (nextval('increment_pkey'), %(first_name)s, %(last_name)s,\
            %(username)s, %(email)s, ('now'), %(password)s);
            """
        user_id = curr.execute(query, user)
        database.commit()
        curr.close()
        pass

    def get_id(self):
        """Queries the database for the user id
        with the passed username
        """
        database = self.db
        curr = database.cursor()
        query = "SELECT user_id FROM users WHERE username = '%s';" % (self.username)
        curr.execute(query)
        user_id = curr.fetchone()
        curr.close()
        return user_id
    
    def get_user_by_id(self, user_id):
        """This function returns user details when an id is passed"""
        pass

    def delete_user(self, user_id):
        """This function takes in a user id and removes it from the database"""
        try:
            dbconn = self.db
            curr = dbconn.cursor()
            query = "DELETE FROM users WHERE user_id = %d;" % (int(user_id))
            curr.execute(query)
            curr.close()
            dbconn.commit()
        except Exception as e:
            return "Not Found"
        pass

    def close_db(self):
        """This function closes the database"""
        self.db.close()
        pass
    
    def encode_auth_token(self, user_id):
        """Function to generate Auth token
        """
        APP = create_app()
        # import pdb;pdb.set_trace()
        try:
            payload = {
                "exp": datetime.utcnow() + timedelta(days=1),
                "iat": datetime.utcnow(),
                "sub": user_id
            }
            token = jwt.encode(
                payload,
                APP.config.get('SECRET_KEY'),
                algorithm="HS256"
            )
            resp = token
        except Exception as e:
            resp = e

        return resp

    @staticmethod
    def decode_auth_token(auth_token):
        """This function takes in an auth 
        token and decodes it
        """
        APP = create_app()
        secret = APP.config.get("SECRET_KEY")
        try:
            payload = jwt.decode(auth_token, secret)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Expired"
        except jwt.InvalidTokenError:
            return "Invalid"