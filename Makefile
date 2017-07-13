.PHONY: build test psql clean docs help

###################################
### Docker shortcuts

run:  ## Runs the dev containers
	docker-compose -f dev.yml up

down:  ## Shut down dev containers
	docker-compose -f dev.yml down

build:  ## Builds all available containers
	docker-compose -f dev.yml build

lint:  ## Run linting and static analysis
	docker-compose -f dev.yml run django flake8 network_search

test: clean  ## Runs tests in the Django container
	docker-compose -f dev.yml run django pytest network_search
	docker-compose -f dev.yml run django flake8 network_search

format:
	docker-compose -f dev.yml run django ./format.sh

psql:  ## Runs a psql shell against the network_search database
	docker-compose -f dev.yml run postgres psql -h postgres -U postgres -d network_search

clean:  ## Removes extraneous files and build artifacts
	-@find . -name '*.pyc' -follow -print0 | xargs -0 rm -f &> /dev/null
	-@find . -name '*.pyo' -follow -print0 | xargs -0 rm -f &> /dev/null
	-@find . -name '__pycache__' -type d -follow -print0 | xargs -0 rm -rf &> /dev/null

docs:
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

help:
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


###################################
### UI shortcuts
ui = ./front-end/

ui-deps:  ## Install UI scaffolding dependneices
	cd $(ui) && yarn install

ui-update: ## Update UI build process dependencies
	cd $(ui) && yarn upgrade-interactive

ui-dev:  ## Use for quick front-end development, only processes css, js, html
	clear
	cd $(ui) && yarn run django-dev

assets:  ## Compress any front-end related assets. (Slow as files may be large)
	clear
	cd $(ui) && yarn run assets

vue:  ## Build vue components
	clear
	cd $(ui) && yarn run vue-dev

html: ## Build only HTML templates (with data)
	clear
	cd $(ui) && yarn run template-build

build-ui:  ## Build front-end for pre-deployment, minimizes JS, minimizes and razors CSS
	clear
	cd $(ui) && yarn run django-build

