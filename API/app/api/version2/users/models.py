from flask_bcrypt import Bcrypt

from .... import db

class UserModel(object)

    def __init__(self, username, first_name, last_name, password, email):
        """initialize the user model"""
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = Bcrypt().generate_password_hash(password).decode()
        self.email = email
        self.db = db
    
    def get_user(self, user_id):
        """return user from the db given a username"""
        database = self.db
        database.cursor().execute(
            "SELECT user_id, first_name, last_name, date_created FROM users WHERE username={}".format(username))
        return database.fetch_all()

    def password_is_valid(self, password)
        """Returns true or false of the password used is valid"""
        return Bcrypt().check_password_hash(self.password, password)

    def save_user():
        """Add user details to the database"""