install:
	@poetry install

lint:
	@poetry run flake8 page_loader

selfcheck:
	poetry check

check: selfcheck lint

build: check
	@poetry build

publish: build
	@poetry publish -r test_pypi

.PHONY: install test lint selfcheck check build