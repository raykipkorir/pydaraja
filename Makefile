install:
	pip install .[dev]

lint:
	pre-commit run --all-files

tests:
	coverage run -m pytest
