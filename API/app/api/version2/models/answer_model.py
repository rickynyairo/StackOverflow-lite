"""
This module defines the answers model and associated functions
"""
from datetime import datetime, timedelta
import json

from .... import create_app
from ....database import init_db
from .base_model import BaseModel

class AnswerModel(BaseModel):
    """This class encapsulates the functions of the answer model"""

    __tablename__ = "answers"

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
        dbconn.commit()
        return data

    def up_vote_answer(self, answer_id, user_id):
        """This function increments or decrements the up_vote field"""
        dbconn = self.db
        curr = dbconn.cursor()
        curr.execute("SELECT voters FROM answers \
                              WHERE answer_id = %s;", (answer_id,))
        voters  = curr.fetchone()[0]
        data = {}
        votes = 1
        if not voters:
            data = json.dumps({ "up_voters":[user_id], "down_voters":[] })
        else:
            data = voters
            up_voters = data["up_voters"]
            if user_id not in up_voters:
                # the user has not upvoted the answer
                up_voters.append(user_id)
            else:
                up_voters.remove(user_id)
                votes = -1
            data = json.dumps({ "up_voters":up_voters, "down_voters":data["down_voters"] })
        query = "UPDATE answers SET voters = %s WHERE answer_id = %s RETURNING voters;"
        # import pdb;pdb.set_trace()
        curr.execute(query, (data, answer_id))
        # new_voters = curr.fetchone()[0]
        curr.execute("""UPDATE answers SET up_votes = \
                     up_votes + %s WHERE answer_id = %s \
                     RETURNING up_votes;""", (votes, int(answer_id)))
        data = curr.fetchone()[0]
        dbconn.commit()
        return int(data)

    def down_vote_answer(self, answer_id, user_id):
        """This function increments or decrements the down_vote field"""
        dbconn = self.db
        curr = dbconn.cursor()
        curr.execute("SELECT down_votes, voters FROM answers \
                              WHERE answer_id = %s;", (answer_id,))
        res  = curr.fetchone()
        voters = res[1]
        down_votes = res[0]
        if not down_votes:
            curr.execute("""UPDATE answers SET down_votes = 0 \
                         WHERE answer_id = %s;""", (int(answer_id),))
            dbconn.commit()
        data = {}
        votes = 1
        if not voters:
            data = json.dumps({ "up_voters":[], "down_voters":[user_id] })
        else:
            data = voters
            down_voters = data["down_voters"]
            if user_id not in down_voters:
                # the user has not downvoted the answer
                down_voters.append(user_id)
            else:
                down_voters.remove(user_id)
                votes = -1
            data = json.dumps({ "up_voters":data["up_voters"], "down_voters":down_voters })
        query = "UPDATE answers SET voters = %s WHERE answer_id = %s RETURNING voters;"
        # import pdb;pdb.set_trace()
        curr.execute(query, (data, answer_id))
        # new_voters = curr.fetchone()[0]
        curr.execute("""UPDATE answers SET down_votes = \
                     down_votes + %s WHERE answer_id = %s \
                     RETURNING down_votes;""", (votes, int(answer_id)))
        data = curr.fetchone()[0]
        dbconn.commit()
        return int(data)

    def get_answers_by_item_id(self, item, item_id):
        """return a list of all the answers with the given item_id"""
        dbconn = self.db
        curr = dbconn.cursor()
        curr.execute("""SELECT * FROM answers WHERE \
                     %s_id = %d ORDER BY \
                     up_votes DESC, date_created DESC;""" % (item, item_id))
        data = curr.fetchall()
        data_items = []
        if not isinstance(data, list):
            data_items.append(data)
        else:
            data_items = data[:]
        resp = []
        for i, items in enumerate(data_items):
            answer_id, question_id, user_id, text, up_votes, date, user_preferred, down_votes, voters = items
            if not down_votes:
                down_votes = 0
            username = self.get_username_by_id(int(user_id))
            answer = {
               "answer_id":int(answer_id),
               "question_id":int(question_id),
               "username":username,
               "text":text,
               "date_created":date.strftime("%B %d, %Y"),
               "up_votes":int(up_votes),
               "down_votes":int(down_votes),
               "user_preferred":user_preferred
            }
            resp.append(answer)
        return resp
