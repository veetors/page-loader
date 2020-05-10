install:
	@poetry install

lint:
	@poetry run flake8 page_loader

ptw:
	@poetry run ptw

test:
	@poetry run pytest --cov=page_loader --cov-report xml tests/

selfcheck:
	poetry check

check: selfcheck lint test

build: check
	@poetry build

publish: build
	@poetry publish -r test_pypi

.PHONY: install test lint selfcheck check build