CODE = shed
TESTS = tests
# Allow setting target coverage level from cli
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
	black --line-length=100 --skip-string-normalization --check $(CODE) $(TESTS)
	pylint --jobs 4 --rcfile=setup.cfg $(CODE) $(TESTS)
	mypy $(CODE)

format:
	isort --apply --recursive $(CODE) $(TESTS)
	black --line-length=100 --skip-string-normalization $(CODE) $(TESTS)
	unify --in-place --recursive $(CODE) $(TESTS)

validate: lint test
