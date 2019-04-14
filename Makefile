# You can set these variables from the command line.
PYTHON      = python
MANAGE_PY   = python manage.py
HOST        = 127.0.0.1
PORT        = 8000

# Put it first so that "make" without argument is like "make help".
help:
	@echo "Available commands for project"
	@echo "clean-pyc        - Remove python compiled files."
	@echo "run              - Spin up django server"
	@echo "test             - Run Test"
	@echo "tox_test         - Run tox"
	@echo "collectstatic    - Collect static files in project"
	@echo "superuser        - Creates a super user."
	@echo "clean-build      - Perform a clean build."
	@echo "lint             - Run flake8 /for project files."
	@echo "view_docs        - Update the docs and spin up sphinx server."
	@echo "install          - Install project in editable mode."


.PHONY: help Makefile

run:
	@echo "Starting server on ${HOST}:${PORT}"
	${MANAGE_PY} add_site
	${MANAGE_PY} runserver ${HOST}:${PORT}

app:
	@echo "Creating app $2..."
	${MANAGE_PY} startapp $2

test:
	@echo "Running test..."
	${MANAGE_PY} test --settings=eval_project.settings

view_docs:
	@echo "Building sphinx docs"
	pip install -q -e .[docs]
	cd docs && make html && echo "Serving documentation" && sphinx-serve -b build -p 8899

install:
	@echo "Installing package dependencies..."
	pip install -e . -r requirements.txt

install-test:
	@echo "Installing test dependencies..."
	pip install -e .[test]

lint:
	@echo "Running flak8..."
	pip install -e .[lint]
	flake8 . --exclude=docs,dist --ignore=F401
