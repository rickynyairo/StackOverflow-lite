"""
This module defines the questions model and associated functions
"""
from datetime import datetime, timedelta

from flask import current_app

# local imports
from .... import create_app
from ....database import init_db
from .base_model import BaseModel

class QuestionModel(BaseModel):
    """This class encapsulates the functions of the question model"""

    __tablename__ = "questions"

    def __init__(self, user_id=0, text="text", description="desc"):
        """initialize the question model"""
        self.user_id = user_id
        self.text = text
        self.description = description
        self.date_created = datetime.now()
        self.db = init_db()

    def save_question(self):
        """Add question details to the database"""
        question = {
            "user_id": self.user_id,
            "text": self.text,
            "description": self.description
        }
        database = self.db
        curr = database.cursor()
        query = """INSERT INTO questions VALUES (nextval('increment_pkey'), %(user_id)s, %(text)s,\
                %(description)s, ('now')) RETURNING question_id;"""
        curr.execute(query, question)
        question_id = curr.fetchone()[0]
        database.commit()
        curr.close()
        return int(question_id)

    def most_answered(self):
        """Obtains the question with the most answers"""
        dbconn = self.db
        curr = dbconn.cursor()
        curr.execute("""SELECT question_id, COUNT(answer_id) FROM answers GROUP BY question_id ORDER BY COUNT(answer_id) DESC;""")
        data = curr.fetchone()
        curr.close()
        return data

    def get_questions_by_user(self, user_id):
        """Return a list of questions associated with a particular user"""
        database = self.db
        curr = database.cursor()
        curr.execute("""SELECT question_id, text, description, date_created\
                     FROM questions WHERE user_id = %d ORDER BY date_created DESC;""" % (user_id)
                    )
        data = curr.fetchall()
        curr.close()
        # return a list of dictionaries
        resp = []
        for i, items in enumerate(data):
            question_id, text, description, date_created = items
            username = self.get_username_by_id(int(user_id))
            item_dict = {
                "question_id":int(question_id),
                "username":username,
                "text":text,
                "description":description,
                "date_created":date_created.strftime("%B %d, %Y")
            }
            resp.append(item_dict)
        return resp

    def get_all(self):
        """This function returns a list of all the questions"""
        dbconn = self.db
        curr = dbconn.cursor()
        curr.execute("""SELECT * FROM questions ORDER BY date_created DESC;""")
        data = curr.fetchall()
        resp = []
        curr.close()
        for i, items in enumerate(data):
            question_id, user_id, text, description, date = items
            question = dict(
               question_id=int(question_id),
               username=self.get_username_by_id(int(user_id)),
               text=text,
               description=description,
               date_created=date.strftime("%B %d, %Y")
            )
            resp.append(question)
        return resp
    