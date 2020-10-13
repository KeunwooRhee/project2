import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r"/api/*": {"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  '''
  This web page allows 'GET', 'POST', 'DELETE' methods.
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE')
    return response


  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  '''
  GET '/categories'
    - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
    - Request Arguments: None
    - Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs
      {'1' : "Science",
       '2' : "Art",
       '3' : "Geography",
       '4' : "History",
       '5' : "Entertainment",
       '6' : "Sports"}
  '''
  @app.route('/categories', methods=['GET'])
  def get_all_categories():
    try:
      categories = Category.query.all()
      formatted_categories = [category.format() for category in categories]
   
      return jsonify({
        'success': True,
        'categories': formatted_categories
      })
    
    except:
      abort(422)


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  '''
  GET '/questions'
    - Fetches a dictionary of categories, a list of questions, number of total questions, current category
    - Request Arguments: None or 'page'
      - 'page' is an integer number.  
      - None is equal to 'page=1'.
    - Returns: An object with four keys,
      - 'categories' that contains an object of id: category_string key:value pairs
      - 'current_category' that is an id of category. In this route, 'current_category' is 'None'. 'None' is a default category.
      - 'questions' that contains a list of question objects
        {
          "answer": "Maya Angelou", 
          "category": 4, 
          "difficulty": 2, 
          "id": 5, 
          "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        }
      - 'total_questions' that is the number of total questions
    - Error: 404, if the value of the 'page' is beyond the number of total pages. 
  '''
  @app.route('/questions', methods=['GET'])
  def get_questions():
    
    page = request.args.get('page', 1, type=int)
    start = (page -1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
  
    current_categories = None

    questions = Question.query.all()
    formatted_questions = [question.format() for question in questions]
  
    categories = Category.query.all()
  
    formatted_categories = {}
    
    for category in categories:
      formatted_categories[category.id] = category.type 

    if len(formatted_questions[start:end]) == 0:
      abort(404)
    else:  
      return jsonify({
        'success': True,
        'questions': formatted_questions[start:end],
        'total_questions': len(formatted_questions),
        'categories': formatted_categories,
        'current_category': current_categories
      })


  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  '''
  DELETE '/questions/<int:question_id>'
    - Deletes a question of id, 'id' is 'question_id'. 
    - Request Arguments: None
    - Returns: An object of the deleted question
      {
        "answer": "Maya Angelou", 
        "category": 4, 
        "difficulty": 2, 
        "id": 5, 
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
      }
    - Error: 422, if there is no question of 'question_id'. It cannot delete a question. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id): 
    
    deleted_question = Question.query.filter_by(id=question_id).one_or_none()
    
    if deleted_question is None:
      abort(422)
    else: 
      deleted_question.delete()
      return jsonify({
        'success': True,
        'question': deleted_question.format()
      }) 
     

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  '''
  POST '/add'
    - Adds a question 
    - Request Arguments: question, answer, category, difficulty
    - Returns: An object of the newly added question
      {
        "answer": "Maya Angelou", 
        "category": 4, 
        "difficulty": 2, 
        "id": 5, 
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
      }
    - Error: 400, if the key of the request argument is wrong. e.g., 'questio'
  '''
  @app.route('/add', methods=['POST'])
  def add_question():
    try:
      question = request.get_json()['question']
      answer = request.get_json()['answer']
      category = request.get_json()['category']
      difficulty = request.get_json()['difficulty']
      
      new_question = Question(question=question, answer=answer, category=category, difficulty=difficulty) 
      new_question.insert()

      return jsonify({
        'success': True,
        'question': new_question.format()
      })

    except:
      abort(400)
    

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  '''
  POST '/questions'
    - Searches questions that include a 'searchTerm' 
    - Request Arguments: searchTerm, a terminology to search.
    - Returns: A list of objects, questions. e.g., if 'searchTerm' is 'name',
      [
        {
          "answer": "Muhammad Ali",
          "category": 4,
          "difficulty": 1,
          "id": 9,
          "question": "What boxer's original name is Cassius Clay?"
        },
        {
          "answer": "Brazil",
          "category": 6,
          "difficulty": 3,
          "id": 10,
          "question": "Which is the only team to play in every soccer World Cup tournament?"
        }
      ]
    - Error: 400, if the key of the request argument is wrong. e.g., 'searchterm'
  '''
  @app.route('/questions', methods=['POST'])
  def search_questions():
    try:
      search_term = request.get_json()['searchTerm']
    
      search_results = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

      formatted_questions = [question.format() for question in search_results] 

      return jsonify({
        'success': True,
        'questions': formatted_questions
      })

    except:
      abort(400)


  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  '''
  GET '/categories/<int:category_id>'
    - Fetches a list of questions and the number of total questions in the current category
    - Request Arguments: None
    - Returns: An object with three keys,
      - 'current_category' that is an id of the current category
      - 'questions' that contains a list of question objects
        {
          "answer": "Maya Angelou", 
          "category": 4, 
          "difficulty": 2, 
          "id": 5, 
          "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        }
      - 'total_questions' that is the number of total questions in the current category
    - Error: 404, there is no category of 'category_id' 
  '''
  @app.route('/categories/<int:category_id>', methods=['GET'])
  def get_categories(category_id):
    result = Category.query.filter_by(id=category_id).one_or_none()
  
    if result is None:
      abort(404)
    else: 
      questions = Question.query.filter_by(category=category_id).all()
      formatted_questions = [question.format() for question in questions]
 
    return jsonify({
      'success': True,
      'questions': formatted_questions,
      'total_questions': len(formatted_questions),
      'current_category': category_id
    })
  

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  '''
  POST '/play'
    - Fetches a question to play the quiz
    - Request Arguments: quiz_category, previous_questions
      - 'quiz_category' is the category of the questions to play the quiz in this time. 
        If the value of 'quiz_category' is 0, it means 'All' categories.
      - 'previous_questions' are the questions already played.
    - Returns: An object with three keys,
      - 'previous_questions' are the quesitons already played.
      - 'category' is the category of the questions to play the quiz in this time.
      - 'question' is a random quesiton to play. It is not one of the previous questions.
        {
          "answer": "Maya Angelou", 
          "category": 4, 
          "difficulty": 2, 
          "id": 5, 
          "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        } 
    - Error: 422, there is no question to play
  '''
  @app.route('/play', methods=['POST'])
  def play_quizzes():
    try:
      category =  request.get_json()['quiz_category']['id']
      previous_questions = request.get_json()['previous_questions']
      possible_questions = []
    
      if category is 0:
        all_questions = Question.query.all()
      else:
        all_questions = Question.query.filter_by(category=category).all()
      
      # error, there is no question to play in a current category
      if len(all_questions) <= 0:
        abort(422)

      # make a pool of questions to play the quiz without already played questions
      for question in all_questions:
        if question.id in previous_questions:
          pass
        else:
          possible_questions.append(question)

      # return 'False' for scoring if there is no possible question to play or a random question
      if len(possible_questions) <= 0:
        return jsonify({
          'success': False,
          'previous_questions': previous_questions,
          'category': category,
          'question': None
        })
      else:
        current_question = possible_questions[random.randint(0, len(possible_questions)-1)].format()

      return jsonify({
        'success': True,
        'previous_questions': previous_questions,
        'category': category,
        'question': current_question
      })

    except:
      abort(422)

    
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "bad request"
    }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "resource not found"
    }), 404

  @app.errorhandler(405)
  def mehotd_not_allowed(error):
    return jsonify({
      "success": False,
      "error": 405,
      "message": "method not allowed"
    }), 405

  @app.errorhandler(422)
  def unprocessible(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "unprocessible"
    }), 422

  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "internal server error"
    }), 422
 
  return app  