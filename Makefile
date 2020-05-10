install:
	@poetry install

selfcheck:
	poetry check

check: selfcheck

build: check
	@poetry build

publish: build
	@poetry publish -r test_pypi