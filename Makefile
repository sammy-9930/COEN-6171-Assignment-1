.PHONY: test unit-tests clean coverage help

test unit-tests:  ## Run unit tests
	python -m pytest -v tests/test_course_schedule_II.py

coverage:  ## Run tests with coverage report
	python -m pytest --cov=src/course_schedule tests/

clean:  ## Remove Python cache files
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name ".pytest_cache" -exec rm -r {} +

help:  ## Show this help message
	

# Default target
.DEFAULT_GOAL := help