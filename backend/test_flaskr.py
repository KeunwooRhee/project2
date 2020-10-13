import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('rhee','projectpassword','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['categories'])

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])
        self.assertEqual(data['total_questions'],19)
        self.assertTrue(data['categories'])
        self.assertEqual(data['current_category'],None)

    def test_404_get_questions_beyond_valid_page(self):
        res = self.client().get('/questions?page=0', json={'rating':1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],"resource not found")
    
    def test_delete_questions(self):
        res = self.client().delete('/questions/4')
        data = json.loads(res.data)

        question = Question.query.filter_by(id=4).all()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertEqual(len(question), 0)
    
    def test_422_delete_questions(self):
        res = self.client().delete('/questions/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],"unprocessible")
    
    def test_add_questions(self):
        new_question = {
            "question":"new question4",
            "answer":"OK",
            "difficulty":2,
            "category":"6"
        }

        res = self.client().post('/add', json=new_question)
        data = json.loads(res.data)

        question = Question.query.filter_by(question="new question4", answer="OK", difficulty=2, category=6).all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(question)
    
    def test_search_questions(self):
        search_term1 = {
            "searchTerm":"title"
        }

        search_term2 = {
            "searchTerm":"abcdefghijklmnopqrstuvwxyz"
        }

        res1 = self.client().post('/questions', json=search_term1)
        data1 = json.loads(res1.data)

        res2 = self.client().post('/questions', json=search_term2)
        data2 = json.loads(res2.data)

        self.assertEqual(res1.status_code, 200)
        self.assertEqual(len(data1['questions']), 2)
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(len(data2['questions']), 0)

    def test_get_questions_based_on_category(self):
        res = self.client().get('/categories/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'],3)
        self.assertEqual(data['current_category'],1)

    def test_404_get_questions_based_on_category(self):
        res = self.client().get('/categories/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],"resource not found")
    
    def test_play_quiz(self):
        quiz_category = {
            "previous_questions":[],
            "quiz_category":{"type":"Sports","id":"6"}
        }

        res = self.client().post('/play', json=quiz_category)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        

    def test_end_play_quiz(self):
        quiz_category = {
            "previous_questions":[20,21,22],
            "quiz_category":{"type":"Science","id":"1"}
        }

        res = self.client().post('/play', json=quiz_category)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], False)

    def test_422_play_quiz(self):
        quiz_category = {
            "previous_questions":[],
            "quiz_category":{"type":"Science","id":"100"}
        }

        res = self.client().post('/play', json=quiz_category)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],"unprocessible")        

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()