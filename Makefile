CODE = shed
# Allow setting coverage level from cli
COV_LEVEL=95
# Add source dir to pythonpath
PYTHONPATH = PYTHONPATH=./:$(CODE)
# Executables
PYTHON = $(PYTHONPATH) python3
PYTEST = $(PYTHONPATH) pytest
TEST =  $(PYTEST) --verbosity=2 --showlocals --strict

.PHONY: lint format test test-failed test-cov validate

# Actions

test:
	$(TEST) --cov --cov-fail-under=$(COV_LEVEL)

test-failed:
	$(TEST) --last-failed

test-cov:
	$(TEST) --cov-report html

lint:
	black --line-length=100 --skip-string-normalization --check $(CODE)
	pylint --jobs 4 --rcfile=setup.cfg $(CODE)
	mypy $(CODE)

format:
	isort --apply --recursive $(CODE)
	black --line-length=100 --skip-string-normalization $(CODE)
	unify --in-place --recursive $(CODE)

validate: lint test
