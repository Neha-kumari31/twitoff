# twitoff
# pipenv install flask flask-sqlalchemy flask-migrate python-dotenv requests tweepy basilica scikit-learn jinja2 gunicorn python-dotenv python-decouple

WEB APPLICATION 

# inclass-web-app-2

## Setup

Setup virtual environment:

```sh
pipenv install --python 3.7

pipenv install Flask Flask-SQLAlchemy Flask-Migrate

pipenv shell
```

Setup database:

```sh

 #> generates app/migrations dir

# run both when changing the schema:
FLASK_APP=web_app flask db migrate #> creates the db (with "alembic_version" table)
FLASK_APP=web_app flask db upgrade #> creates the "users" table
```


## Run

Run the app:

```sh
FLASK_APP=web_app flask run
```