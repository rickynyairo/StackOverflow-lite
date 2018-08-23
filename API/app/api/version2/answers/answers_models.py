"""
This module defines the answers model and associated functions
"""
from datetime import datetime, timedelta

from .... import init_db, create_app

class AnswerModel(object):
    """This class encapsulates the functions of the answer model"""
    def __init__(self, question_id=0, user_id=0, text="text"):
        """initialize the answer model"""
        self.user_id = user_id
        self.text = text
        self.question_id = question_id
        self.date_created = datetime.now()
        self.db = init_db()

    def get_answers_by_user_id(self, user_id=0):
        """return a list of all the answers with the user id given"""
        if not user_id:
            user_id = self.user_id
        database = self.db
        curr = database.cursor()
        curr.execute(
            """SELECT * FROM answers WHERE user_id = %d;""" % (user_id))
        data = curr.fetchall()
        curr.close()
        # return a list of tuples
        resp = []
        for i, items in enumerate(data):
            answer_id, question_id, user_id, text, date, up_votes, user_preferred = items
            answer = dict(
               question_id=int(question_id),
               user_id=int(user_id),
               text=text,
               answer_id=answer_id,
               date_created=date,
               up_votes=up_votes,
               user_preferred=user_preferred
            )
            resp.append(answer)
        return resp

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
  
    def delete_answer(self, answer_id):
        """This function takes in a answer id and removes it from the database"""
        try:
            dbconn = self.db
            curr = dbconn.cursor()
            query = "DELETE FROM answers WHERE answer_id = %d;" % (int(answer_id))
            curr.execute(query)
            curr.close()
            dbconn.commit()
        except Exception as e:
            return "Not Found"
        pass

    def update_answer(self, text, answer_id):
        """update an answer given the answer_id"""
        dbconn = self.db
        curr = dbconn.cursor()
        curr.execute("UPDATE answers \
                     SET text = '%s' WHERE answer_id = %d RETURNING text;" % (text, answer_id))
        text = curr.fetchone()
        return text

    def get_answers_by_question_id(self, question_id):
        """return a list of all the answers with the given question_id"""
        dbconn = self.db
        curr = dbconn.cursor()
        curr.execute("""SELECT * FROM answers WHERE \
                     question_id = %d;""" % (int(question_id))) 
        data = curr.fetchall()
        self.close_db()
        resp = []     
        for i, items in enumerate(data):
            answer_id, question_id, user_id, text, date, up_votes, user_preferred = items
            answer = dict(
               answer_id=int(answer_id),
               user_id=int(user_id),
               text=text,
               question_id=int(question_id),
               date_created=date,
               up_votes=up_votes,
               user_preferred=user_preferred
            )
            resp.append(answer)
        return resp
       
    def close_db(self):
        """This function closes the database"""
        self.db.close()
        pass