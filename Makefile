# NOTE: make help uses a special comment format to group targets.
# If you'd like your target to show up use the following:
# my_target: ##@category_name sample description for my_target
default: help
.PHONY: install

install: ##@repo Installs needed prerequisites and software to develop in the SRE space
	$(info ********** Installing Repo Prerequisites **********)
	@brew bundle
	@pipx ensurepath
	@bash -l scripts/install.sh -a
	@bash -l scripts/install.sh -p
	@asdf reshim

# SRE Documentation Development
.PHONY : build serve
build: ##@documentation Build the Documentation Site (Material UI React)
	$(info ********** Build the Documentation Site (Material UI React) **********)
	#@bash scripts/docs.sh
	#@./.python/bin/python -m mkdocs build
	@./.python/bin/python scripts/build-docs-src.py
	@./.python/bin/python docs/scripts/release-notes.py

serve: ##@documentation Build and Publish the Documentation Site (Material UI React)
	$(info ********** Serve the Documentation Site (Material UI React) **********)
	@./.python/bin/python -m mkdocs serve

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
