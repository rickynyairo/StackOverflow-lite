"""
This module tests the answers model

"""
import unittest
import json
import string
from random import choice, randint

# local imports
from ... import create_app, init_db
from ...api.version2.models.user_model import UserModel
from ...api.version2.models.question_model import QuestionModel
from ...api.version2.models.answer_model import AnswerModel

class TestAnswerModel(unittest.TestCase):
    """
    This class encapsulates the tests for the answer model
    """
    def create_user(self):
        """create a fictitious user"""
        username = "".join(choice(
                                string.ascii_letters) for x in range (randint(7,10)))
        params = {
                "username":username,
                "first_name":"ugali",
                "last_name":"mayai",
                "email":"ugalimayai@gmail.com",
                "password":"password"
            }       
        user = UserModel(**params)
        user_id = user.save_user()
        return user_id

    def create_question(self):
        """This function sets up a test question in the db
        """
        user_id = self.create_user()

        params = {
            "user_id":user_id,
            "text":"What is the fastest programming language and why?",
            "description":"I am looking for the fastest programming language in terms\
                            of memory management for a very high performance project."
        }
        question = QuestionModel(**params)
        question_id = question.save_question()
        return question_id
    
    def create_answer(self):
        """Set up an answer in the db"""
        user_id = self.create_user()
        question_id = self.create_question()
        random_ans = "".join(choice(
                             string.ascii_letters) for x in range (randint(20,50)))
        params = {
            "user_id":user_id,
            "question_id":question_id,
            "text":random_ans
        }
        answer = AnswerModel(**params)
        answer_id = answer.save_answer()
        return answer_id

    def setUp(self):
        """Define the data to be used for the test
        """
        self.user_id = self.create_user()
        self.question_id = int(self.create_question())
        self.answer = {
            "question_id":self.create_question(),
            "user_id":self.user_id,
            "text":"Julia. It has everything awesome about every great programming language, and more."
        }
        self.question = {
            "user_id":self.user_id,
            "text":"What is the fastest programming language and why?",
            "description":"I am looking for the fastest programming language in terms\
                            of memory management for a very high performance project."
        }
        self.app = create_app()

        with self.app.app_context():
            self.db = init_db()
    
    def test_that_answer_can_be_created(self):
        """Test that the answer model can create an answer"""
        answer_id = self.create_answer()
        curr = self.db.cursor()
        curr.execute("SELECT user_id FROM answers\
                     WHERE answer_id = %d;" % (answer_id))
        posted_id = curr.fetchone()[0]

        self.assertTrue(posted_id)

    def test_that_answer_can_be_deleted(self):
        """Test that the answer model can delete a answer"""
        params = self.answer
        answer = AnswerModel(**params)       
        answer_id = answer.save_answer()
        answer.delete_item(answer_id)
        curr = self.db.cursor()
        query = "SELECT answer_id FROM answers\
                 WHERE answer_id = %d;" % (answer_id)
        curr.execute(query)
        data = curr.fetchone()
        self.assertEqual(None, data)

    def test_get_answers_by_question_id(self):
        """Test that the model can return all answers with a given question id"""
        user_id = self.user_id
        question_id = self.question_id
        random_ans_1 = "".join(choice(
                             string.ascii_letters) for x in range (randint(20,50)))
        answer1 = {
            "user_id":user_id,
            "question_id":question_id,
            "text":random_ans_1
        }
        random_ans_2 = "".join(choice(
                             string.ascii_letters) for x in range (randint(20,50)))
        answer2 = {
            "user_id":user_id,
            "question_id":question_id,
            "text":random_ans_2
        }
        answer_id_1 = AnswerModel(**answer1).save_answer()
        ans2 = AnswerModel(**answer2)
        answer_id_2 = ans2.save_answer()
        answers_to_question = ans2.get_answers_by_question_id(question_id)

        for answer in answers_to_question:
            self.assertEqual(int(answer['question_id']), question_id)

    def test_toggle_user_preferred(self):
        """Test that the user model can toggle the ```user_preferred``` field"""
        answer_id = self.create_answer()
        ans_model = AnswerModel()
        toggled = ans_model.toggle_user_preferred(int(answer_id))
        new_value = ans_model.get_item_by_id(int(answer_id))[6]
        self.assertTrue(new_value)

        
    def tearDown(self):
        """This function destroys objests created during the test run"""
        curr = self.db.cursor()
        exit_query = "DELETE FROM answers WHERE user_id = %d;" % (self.user_id)
        curr.execute(exit_query)
        curr.close()
        self.db.commit()
        del self.question
        with self.app.app_context():
            self.db.close()

if __name__ == "__main__":
    unittest.main()
