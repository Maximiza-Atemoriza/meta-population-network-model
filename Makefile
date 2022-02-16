POETRY := $(shell command -v poetry 2> /dev/null)

install:
ifndef POETRY
    $(error "poetry is not available, please install poetry ( https://python-poetry.org/ )")
endif
	poetry install

docker:
	docker-compose run -p 8051:8051 app python3 ./src/index.py

poetry: install
	poetry run python ./src/index.py
