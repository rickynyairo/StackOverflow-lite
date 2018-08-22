"""
This module tests the question model

"""
import unittest
import json
import string
from random import choice, randint

# local imports
from ... import create_app, init_db
from ...api.version2.users.user_models import UserModel
from ...api.version2.questions.question_models import QuestionModel

class TestQuestionModel(unittest.TestCase):
    """This class encapsulates the tests for the user model
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

    def setUp(self):
        """Define the data to be used for the test
        """
        
        self.user_id = self.create_user()

        self.question = {
            "user_id":self.user_id,
            "text":"What is the fastest programming language and why?",
            "description":"I am looking for the fastest programming language in terms\
                            of memory management for a very high performance project."
        }
        self.app = create_app()

        with self.app.app_context():
            self.db = init_db()
    
    def test_that_question_can_be_created(self):
        """Test that the user model can create a user"""
        params = self.question
        question = QuestionModel(**params)
        
        # save the user to the db
        question_id = question.save_question()
        curr = self.db.cursor()
        curr.execute("SELECT text FROM questions\
                     WHERE question_id = %d;" % (question_id))
        question_text = curr.fetchone()[0]

        self.assertIn(self.question['text'], question_text)

    def test_that_question_can_be_deleted(self):
        """Test that the question model can delete a question"""
        params = self.question
        question = QuestionModel(**params)       
        question_id = question.save_question()
        question.delete_question(question_id)
        curr = self.db.cursor()
        query = "SELECT question_id FROM questions\
                 WHERE question_id = %d;" % (question_id)
        curr.execute(query)
        data = curr.fetchone()
        self.assertEqual(None, data)

    def test_get_question_by_user_id(self):
        """Test that the model can return all questions with a given id"""
        user_id = self.create_user()
        random_que_1 = "".join(choice(
                             string.ascii_letters) for x in range (randint(7,10)))
        random_desc_1 = "".join(choice(
                             string.ascii_letters) for x in range (randint(20,50)))
        question1 = {
            "user_id":user_id,
            "text":random_que_1,
            "description":random_desc_1
        }
        random_que_2 = "".join(choice(
                             string.ascii_letters) for x in range (randint(7,10)))
        random_desc_2 = "".join(choice(
                             string.ascii_letters) for x in range (randint(20,50)))
        question2 = {
            "user_id":self.user_id,
            "text":random_que_2,
            "description":random_desc_2
        }
        question_id_1 = QuestionModel(**question1).save_question()
        que2 = QuestionModel(**question2)
        question_id_2 = que2.save_question()
        questions_by_user = que2.get_questions_by_user_id(user_id)

        for question in questions_by_user:
            self.assertEqual(int(question[1]), user_id)


    def tearDown(self):
        """This function destroys objests created during the test run"""
        curr = self.db.cursor()
        exit_query = "DELETE FROM questions WHERE user_id = %d;" % (self.user_id)
        curr.execute(exit_query)
        curr.close()
        self.db.commit()
        del self.question
        with self.app.app_context():
            self.db.close()

if __name__ == "__main__":
    unittest.main()
