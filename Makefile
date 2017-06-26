.PHONY: build test psql clean docs help

###################################
### Docker shortcuts

run:  ## Runs the dev containers
	docker-compose -f dev.yml up

build:  ## Builds all available containers
	docker-compose -f dev.yml build

lint:  ## Run linting and static analysis
	docker-compose -f dev.yml run django flake8 network_search

test: clean  ## Runs tests in the Django container
	docker-compose -f dev.yml run django pytest
	docker-compose -f dev.yml run django flake8 network_search

format:
	docker-compose -f dev.yml run django ./format.sh

psql:  ## Runs a psql shell against the network_search database
	docker-compose -f dev.yml run postgres psql -h postgres -U postgres -d network_search

clean:  ## Removes extraneous files and build artifacts
	find . -name "*.pyc" -delete

docs:
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

help:
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


###################################
### UI shortcuts
ui = ./front-end/

ui-deps: 
	cd $(ui) && yarn install

ui-update: ## Update UI Build Process dependencies
	cd $(ui) && yarn upgrade-interactive

ui-dev:
	clear
	cd $(ui) && yarn run django-dev

ui-build:
	clear
	cd $(ui) && yarn run django-build

proto-dev:
	clear
	cd $(ui) && yarn run dev

proto-build:
	clear
	cd $(ui) && yarn run build

razor:
	clear
	cd $(ui) && yarn run razor
