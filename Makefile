init:
	pip install -r requirements.txt
	
lint:
	flake8

test:
	python -m pytest
	coverage run -m pytest -v
