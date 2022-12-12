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

deploy:
	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 216514549505.dkr.ecr.us-east-1.amazonaws.com
	docker build -t harrypotter .
	docker tag harrypotter:latest 216514549505.dkr.ecr.us-east-1.amazonaws.com/harrypotter:latest
	docker push 216514549505.dkr.ecr.us-east-1.amazonaws.com/harrypotter:latest

run: 
	python3 -m uvicorn api:app --reload

all: install refactor test deploy
