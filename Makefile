.PHONY: test format lint check install dev clean build publish

test:
	PYTHONPATH=. python3 -m pytest tests/ -vv

format:
	black solexplain/ tests/
	isort solexplain/ tests/

lint:
	flake8 solexplain/ tests/ --max-line-length 120 --ignore E203,W503
	black --check solexplain/ tests/
	isort --check solexplain/ tests/

check: lint test

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

clean:
	rm -rf build/ dist/ *.egg-info solexplain.egg-info .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

build: clean
	python3 -m build

publish: build
	python3 -m twine upload dist/*
