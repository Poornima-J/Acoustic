web: flask db upgrade; flask translate compile; gunicorn microblog:app --preload
heroku ps:scale web=1
