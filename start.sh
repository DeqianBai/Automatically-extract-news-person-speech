export FLASK_APP=flaskr
export FLASK_ENV=development
flask init-db
flask run -p 8082 -h 0.0.0.0 > /dev/null &