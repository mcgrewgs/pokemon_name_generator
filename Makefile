new_hash = $(shell sha2 -256 -q Pipfile)
old_hash = $(shell cat pipfile_hash)
PIPENV_VENV_IN_PROJECT = 1
PROJECT_NAME = pokemon_name_generator
PYTHON_CMD = pipenv run python

.PHONY: setup
setup:
	if ! pipenv --venv; then PIPENV_VENV_IN_PROJECT=$(PIPENV_VENV_IN_PROJECT) pipenv install --dev; fi

.PHONY: update
update: setup
	if [[ "$(new_hash)" != "$(old_hash)" ]]; then PIPENV_VENV_IN_PROJECT=$(PIPENV_VENV_IN_PROJECT) pipenv update --dev; echo "$(new_hash)" > pipfile_hash; fi

.PHONY: words
words:
	$(PYTHON_CMD) -i -c 'import pokemon_name_generator.words as words'
