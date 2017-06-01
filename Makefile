.PHONY: build test psql clean help

###################################
### Docker shortcuts

run:  ## Runs the dev containers
	docker-compose -f dev.yml up

build:  ## Builds all available containers
	docker-compose -f dev.yml build

test:  ## Runs tests in the Django container
	docker-compose -f dev.yml run django pytest

psql:  ## Runs a psql shell against the network_search database
	docker-compose -f dev.yml run postgres psql -h postgres -U postgres -d network_search

clean:  ## Removes extraneous files and build artifacts
	find . -name "*.pyc" -delete

help:
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
