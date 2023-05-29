start:
	poetry run flask --app scripts/example --debug run
run:
	poetry run gunicorn --workers=4 --bind=127.0.0.1:5000 scripts.example:app