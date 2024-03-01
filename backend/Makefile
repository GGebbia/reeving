clean:
	# Delete migrations and compiled files. Deletes db
	find . -type d -name venv -prune -o -path "*/migrations/*.py" ! -name "__init__.py" -exec rm -f {} +
	find . -type d -name venv -prune -o -path "*/migrations/*.pyc" -exec rm -f {} +
	rm -f db.sqlite3

create_db: clean
	. venv/bin/activate && python manage.py makemigrations
	. venv/bin/activate && python manage.py migrate

run: install
	python3 manage.py runserver 0.0.0.0:8000

test: install create_db
	. venv/bin/activate && python3 manage.py test

coverage: install create_db
	. venv/bin/activate && coverage run manage.py test
	. venv/bin/activate && coverage report -m

venv:
	test -d venv || python3 -m venv venv

install: venv
	. venv/bin/activate && pip install -r requirements.txt