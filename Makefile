init:
	pip install -r requirements.txt
	
lint: lint-dice lint-parser

lint-dice:
	flake8 dice*.py

lint-parser:
	flake8 query_parser*.py

test:
	coverage run -m pytest -v

test-dice:
	coverage run -m pytest -v dice_test.py

test-parser:
	coverage run -m pytest -v query_parser_test.py
