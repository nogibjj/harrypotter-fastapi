install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt
format:	
	black *.py 

lint:
	pylint --disable=R,C --extension-pkg-whitelist='pydantic' --ignore-patterns=test_.*?py *.py 

test: 
	python -m pytest -vv test_*.py

refactor: format lint

all: install format