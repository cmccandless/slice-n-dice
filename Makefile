init:
	pip install -r requirements.txt
	
lint:
	flake8

test:
	coverage run -m pytest -v
