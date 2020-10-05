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
  #CORS(app)

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
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
  @app.route('/', methods=['GET'])
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
  @app.route('/questions', methods=['GET'])
  def get_questions():
    '''
    try:
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
    
    except:
      abort(422)
    '''
    page = request.args.get('page', 1, type=int)
    start = (page -1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
  
    current_categories = None
    #current_categories = 0

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
  @app.route('/categories/<int:category_id>', methods=['GET'])
  def get_categories(category_id):
    categories = Category.query.filter_by(id=category_id).all()
    result = Category.query.filter_by(id=category_id).one_or_none()
  
    if result is None:
      abort(404)
    else: 
      formatted_categories = [category.format() for category in categories]
  
    questions = Question.query.filter_by(category=category_id).all()
    #print(questions)
    formatted_questions = [question.format() for question in questions]
   # formatted_categories = [category.format() for category in categories]

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
  @app.route('/play', methods=['POST'])
  def play_quizzes():
    '''
    category =  request.get_json()['quiz_category']['id']
    previous_questions = request.get_json()['previous_questions']
    possible_questions = []
    
    if category is 0:
      all_questions = Question.query.all()
    else:
      all_questions = Question.query.filter_by(category=category).all()
    
    for question in all_questions:
      if question.id in previous_questions:
        pass
      else:
        possible_questions.append(question)

    if len(possible_questions) <= 0:
      return jsonify({'success': False})
      #abort(404)
    else:
      current_question = possible_questions[random.randint(0, len(possible_questions)-1)].format()

    return jsonify({
      'success': True,
      'question': current_question
    })
    '''
    
    try:
      category =  request.get_json()['quiz_category']['id']
      previous_questions = request.get_json()['previous_questions']
      possible_questions = []
    
      if category is 0:
        all_questions = Question.query.all()
      else:
        all_questions = Question.query.filter_by(category=category).all()
      
      if len(all_questions) <= 0:
        abort(422)

      for question in all_questions:
        if question.id in previous_questions:
          pass
        else:
          possible_questions.append(question)

      if len(possible_questions) <= 0:
        return jsonify({'success': False})
        #abort(404)
      else:
        current_question = possible_questions[random.randint(0, len(possible_questions)-1)].format()

      return jsonify({
        'success': True,
        'question': current_question
      })

    except:
      abort(422)
    
    
    '''
    category =  request.get_json()['quiz_category']['id']
    previous_questions = request.get_json()['previous_questions']
    possible_questions = []
  
    if category is 0:
      all_questions = Question.query.all()
    else:
      all_questions = Question.query.filter_by(category=category).all()
    
  
    if all_questions is None:
      abort(422)
    
    for question in all_questions:
      if question.id in previous_questions:
        pass
      else:
        possible_questions.append(question)

    if len(possible_questions) <= 0:
      return jsonify({'success': False})
      #abort(404)
    else:
      current_question = possible_questions[random.randint(0, len(possible_questions)-1)].format()

    return jsonify({
      'success': True,
      'question': current_question
    })
    '''
    


  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "resource not found"
    }), 404

  @app.errorhandler(422)
  def unprocessible(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "unprocessible"
    }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "bad request"
    }), 400

  @app.errorhandler(405)
  def mehotd_not_allowed(error):
    return jsonify({
      "success": False,
      "error": 405,
      "message": "method not allowed"
    }), 405

  return app

    