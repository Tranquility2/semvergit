.PHONY: run clean build

SHELL=/bin/bash

setup:
	python3 -m pip install --editable '.[dev,test]'

setup-dev:
	python3 -m pip install '.[dev]'

setup-test:
	python3 -m pip install '.[test]'

pip-clean:
	python3 -m pip uninstall -y -r <(pip freeze)

clean:
	rm -rf **/__pycache__ **/**/__pycache__ .pytest_cache/ \
	dist/ .mypy_cache/ .coverage **/*.egg-info build

check-black:
	python3 -m black --diff --check .

check-isort:
	python3 -m isort --diff --check .

check-format: | check-black check-isort

check-lint:
	python3 -m pylint --reports=True --recursive=y .

pytest:
	python3 -m pytest -v

coverage:
	python3 -m coverage run --source=semvergit --module pytest \
	--verbose tests && coverage report --show-missing

tests: | pytest coverage

check-mypy:
	python3 -m mypy	.

check-bandit:
	python3 -m bandit -c pyproject.toml -r .

compile:
	python3 -m pip install --upgrade pip-tools
	python3 -m piptools compile -o requirements/requirements.txt pyproject.toml
	python3 -m piptools compile -o requirements/requirements-test.txt requirements/requirements-test.in
	python3 -m piptools compile -o requirements/requirements-dev.txt requirements/requirements-dev.in

build:
	python3 -m pip install --upgrade build
	python3 -m build

 publish:
	python3 -m pip install --upgrade twine
	python3 -m twine upload dist/*
