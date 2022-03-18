include .env

SHELL := /bin/bash
PYTHON := python


help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

sort:  ## User isort
	isort ./tele-pyro

black:  ## User black
	black ./tele-pyro

build:  ## Build package
	poetry build

publish:  ## Publish package
	poetry publish --username PYPI_USERNAME --password PYPI_PASS

git-push:  ## Git push
	git add .
	git commit -m "update"
	git push

push:  ## Prepare and push to git
	sort
	black
	git-push

deploy:  ## Publish package in PyPi
	poetry publish --username PYPI_USERNAME --password PYPI_PASS

check:  ## Check
	python convertor.py -d ... -p ... --hash ... --id ...