.DEFAULT_GOAL 	:= main
.PHONY: clean, info

ORG_NAME 		:= 2kodevs
PROJECT_NAME 	:= CoolCompiler
APP_VERSION		:= v0.1
APP_DESCRIPTION := $(ORG_NAME) - $(PROJECT_NAME)$(APP_VERSION)
DEVELOPERS		:= Lázaro Raúl Iglesias Vera, Miguel Tenorio Potrony, Mauricio Lázaro Perdomo Cortéz
COPYRIGHT	 	:= Copyright © 2020: $(DEVELOPERS)

main: ## Compiling the compiler :)
	# Compiling the compiler :)

clean: ## Remove temporary files
	rm -rf build/*

test: ## Run testsuit with name TAG
	pytest ../tests -v --tb=short -m=${TAG}

info: ## Display project description
	@echo "$(APP_DESCRIPTION)"
	@echo "$(COPYRIGHT)"

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

