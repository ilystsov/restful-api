lint:
	poetry run flake8 src tests
	poetry run mypy src
	poetry run mypy tests

test:
	poetry run pytest --cov=src --cov-report html


run:
	uvicorn src.homework.main:app --reload

docker-build:
	docker build -f docker/Dockerfile -t api .

docker-run:
	docker run -p 8000:8000 api

docker-test:
	docker run -t api pytest
