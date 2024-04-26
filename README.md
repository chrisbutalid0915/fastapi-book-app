# fastapi-book-app
Python Test


## Setup Local Deployment
1. Open cmd and install poetry `pip install poetry`
2. Run `poetry config virtualenvs.in-project true` to create virtual environments within the project directory.
3. Run `poetry install` to install dependencies.
4. Run `poetry shell` to activate the environment 
5. Run `uvicorn main:app --reload` to run the fastapi application.
6. Browse to http://127.0.0.1:8000/ to see the app running.

### API DOCS
Browse to http://127.0.0.1:8000/docs to see the API docs.