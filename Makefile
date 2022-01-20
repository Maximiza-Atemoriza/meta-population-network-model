POETRY := $(shell command -v poetry 2> /dev/null)

install:
ifndef POETRY
    $(error "poetry is not available, please install poetry ( https://python-poetry.org/ )")
endif
	poetry update

run: install
	poetry run python ./src/dash_app/index.py
