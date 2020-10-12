# Trivia API
This is the project for the Udacity's Nanodegree Program. This program provides:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

All backend code follows PEP8 style guidelines.

## Getting Started 

### Pre-requisites and Installation: Backend

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Pre-requisites and Installation: Frontend

#### Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

>_tip_: **npm i** is shorthand for **npm install**

### Database Setup and Running the server: Backend

#### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

#### Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

Base URL: The backend app is hosted at the default, [http://localhost:5000](http://localhost:5000) 

### Running the Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```

### Tests

In order to run tests navigate to the backend folder and run the followind commands:

```bash
dropdb trivia_test
create db trivia_test
psql trivia_test < trivia.psql
python3 test_flaskr.py
```

### Error Handling

Errors are returned as JSON objects in the following format:
```    
{
  "success": False, 
  "error": 400,
  "message": "bad request"
}
```

The API will return four error types when requests fail:

* 400: Bad Request
* 404: Resource Not Found
* 405: Method Not Allowed
* 422: Not Processible

## API Reference

### GET /questions
        Returns a list of book objects, success value, and total number of books
        Results are paginated in groups of 8. Include a request argument to choose page number, starting from 1.
    Sample: curl http://127.0.0.1:5000/books

  "books": [
    {
      "author": "Stephen King",
      "id": 1,
      "rating": 5,
      "title": "The Outsider: A Novel"
    },
    {
      "author": "Lisa Halliday",


## Authors

K. Rhee. 

## Acknowledgements

This is not the real world application, but the project for the Udacity's Nanodegree Program. 

Do not copy and use this program as your own project if you are the student of the Udacity's Full Stack Web Develer Nanodegree Program.
