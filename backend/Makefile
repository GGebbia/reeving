clean:
	# Delete migrations and compiled files. Deletes db
	find . -type d -name venv -prune -o -path "*/migrations/*.py" ! -name "__init__.py" -exec rm -f {} +
	find . -type d -name venv -prune -o -path "*/migrations/*.pyc" -exec rm -f {} +
	rm -f db.sqlite3

create_db: clean
	python3 manage.py makemigrations
	python3 manage.py migrate
	# python3 manage.py createsuperuser

run: install
	python3 manage.py runserver

test:
	python3 manage.py test

coverage:
	coverage run manage.py test
	coverage report -m

venv:
	test -d venv || python3 -m venv venv

install: venv
	. venv/bin/activate && pip install -r requirements.txt