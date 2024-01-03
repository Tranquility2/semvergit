.PHONY: run clean

SHELL=/bin/bash

setup-dev:
	python3 -m pip install --editable '.[dev]'

pip-clean:
	python3 -m pip uninstall -y -r <(pip freeze)

clean:
	rm -rf **/__pycache__ **/**/__pycache__ .pytest_cache/ dist/ .mypy_cache/ .coverage **/*.egg-info build

check-black:
	python3 -m black --diff --check .

check-isort:
	python3 -m isort --diff --check .

check-format: | check-black check-isort

fix-format:
	python3 -m black .
	python3 -m isort .

lint:
	python3 -m pylint --reports=True semvergit

pytest:
	python3 -m pytest -v

coverage:
	python3 -m coverage run --source=semvergit --module pytest \
	--verbose tests && coverage report --show-missing

tests: | pytest coverage

mypy:
	python3 -m mypy	.
