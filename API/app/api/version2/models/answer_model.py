"""
This module defines the answers model and associated functions
"""
from datetime import datetime, timedelta

from flask import current_app

from .... import create_app
from ....database import init_db
from .base_model import BaseModel

class AnswerModel(BaseModel):
    """This class encapsulates the functions of the answer model"""
    def __init__(self, question_id=0, user_id=0, text="text"):
        """initialize the answer model"""
        self.user_id = user_id
        self.text = text
        self.question_id = question_id
        self.date_created = datetime.now()
        self.db = init_db()

    def save_answer(self):
        """Add answer details to the database"""
        answer = {
            "question_id":self.question_id,
            "user_id": self.user_id,
            "text": self.text,
            "up_votes":0
        }
        database = self.db
        curr = database.cursor()
        query = """INSERT INTO answers VALUES (nextval('increment_pkey'), %(question_id)s,\
                   %(user_id)s, %(text)s, %(up_votes)s,('now')) RETURNING answer_id;"""
        curr.execute(query, answer)
        answer_id = curr.fetchone()[0]
        database.commit()
        curr.close()
        return int(answer_id)

    def toggle_user_preferred(self, answer_id):
        """this function marks a given answer as the preferred"""
        dbconn = self.db
        curr = dbconn.cursor()
        curr.execute("""UPDATE answers SET user_preferred = \
                     NOT user_preferred WHERE answer_id = %d \
                     RETURNING user_preferred;""" % (int(answer_id))) 
        data = curr.fetchone()[0]
        return data

    def get_answers_by_question_id(self, question_id):
        """return a list of all the answers with the given question_id"""
        dbconn = self.db
        curr = dbconn.cursor()
        curr.execute("""SELECT * FROM answers WHERE \
                     question_id = %d;""" % (int(question_id))) 
        data = curr.fetchall()
        data_items = []
        if not isinstance(data, list):
            data_items.append(data)
        else:
            data_items = data[:]
        resp = []     
        for i, items in enumerate(data_items):
            answer_id, question_id, user_id, text, up_votes, date, user_preferred = items
            username = BaseModel().get_username_by_id(int(user_id))
            answer = {
               "answer_id":int(answer_id),
               "question_id":int(question_id),
               "username":username,
               "text":text,
               "date_created":date,
               "up_votes":int(up_votes),
               "user_preferred":user_preferred
            }
            resp.append(answer)
        return resp
