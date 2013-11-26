test: lint test-python

lint:
	@echo "Linting Python files"
	flake8 --ignore=E121,W404,F403,E501 --exclude=./docs/*,./env/*,./venv/*,migrations,.git . || exit 1
	@echo ""

test-python:
	@echo "Running Python tests"
	python manage.py test -v 2 || exit 1
	@echo ""

initdb:
	python manage.py syncdb 
	python manage.py migrate

install:
	pip install --upgrade setuptools
	pip install --upgrade "flake8>=2.0"
	pip install --upgrade -r requirements.txt

server:
	python manage.py runserver 0.0.0.0:7000
