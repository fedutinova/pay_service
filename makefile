format:
	@echo "formatting..."
	poetry run ruff format app

types:
	@echo "checking types..."
	poetry run mypy app


migration:
	@echo "running migrations..."
	alembic revision --autogenerate -m "initial migration"


start:
	@echo "starting app..."
	poetry run python cli.py api


test_with_cov:
	@echo "running tests with coverage..."
	pytest --cov=app --cov-report=term-missing

test:
	@echo "running tests..."
	pytest -v
