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
	aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/s6y1u4h5	
	docker build -t harrypotter .
	docker tag harrypotter:latest public.ecr.aws/s6y1u4h5/harrypotter:latest
	docker push public.ecr.aws/s6y1u4h5/harrypotter:latest

run: 
	python3 -m uvicorn api:app --reload

all: install refactor test