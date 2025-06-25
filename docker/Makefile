# NOTE: make help uses a special comment format to group targets.
# If you'd like your target to show up use the following:
# my_target: ##@category_name sample description for my_target
default: help

.PHONY : build serve
build: ##@documentation Build the Documentation Site (Material UI React)
	$(info ********** Build the Documentation Site (Material UI React) **********)
	@../.python/bin/python ../scripts/build-docs-src.py
	@../.python/bin/python ../docs/scripts/release-notes.py

PHONY: docs-package docs-publish
docs-package: ##@documentation Image Build and Package the Documentation Site (Material UI React) to Docker Image
	$(info ********** Package the Documentation Site with Docker (Material UI React) **********)
	@docker build -t docs:latest -f docs/Dockerfile ../

docs-serve: ##@documentation Serve the Docker implementation of the Documentation Site (Material UI React)
	$(info ********** Serve the Docker Containerized Documentation Site (Material UI React) **********)
	@docker run --rm -p 8100:8100 -it docs:latest bash

docs-publish: ##@documentation Image Build and Publish the Documentation Site Docker Image to GCR
	@make docs-package
	$(info ********** Publish the Documentation Docker Image **********)
	@echo "This function is not yet implemented -- Coming soon!"

############# Development Section #############
help: ##@misc Show this help.
	@echo $(MAKEFILE_LIST)
	@perl -e '$(HELP_FUNC)' $(MAKEFILE_LIST)

# helper function for printing target annotations
# ripped from https://gist.github.com/prwhite/8168133
HELP_FUNC = \
	%help; \
	while(<>) { \
		if(/^([a-z0-9_-]+):.*\#\#(?:@(\w+))?\s(.*)$$/) { \
			push(@{$$help{$$2}}, [$$1, $$3]); \
		} \
	}; \
	print "usage: make [target]\n\n"; \
	for ( sort keys %help ) { \
		print "$$_:\n"; \
		printf("  %-20s %s\n", $$_->[0], $$_->[1]) for @{$$help{$$_}}; \
		print "\n"; \
	}
