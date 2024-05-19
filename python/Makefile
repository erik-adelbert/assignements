# This Makefile provides a streamlined way to build, run, and clean up 
# Docker containers for the application and its tests. It also includes 
# a target for running a stress test, which depends aiohttp python module.
.PHONY: all build-run-app build-run-test stress-test docker-% clean

# Container CLI, could also be podeman or lima
DOCKER ?= docker

# Define the container image name prefix
BASE_IMAGE_NAME ?= user-service

# Local app port mapping
API_PORT ?= 8000

# Default to testing
all: docker-test clean

# Build and run a standalone containerized app
build-run-app: docker-app

# Build and run containerized tests
build-run-test: docker-test

# Launch a simple stress test build-run-test must be running 
# on localhost
#
# Depends on python module aiohttp being available to python:
# $ pip install aiohttp
stress-test:
	python stress.py $(API_PORT)

# Pattern rule for docker targets restricted to "test" or "app"
docker-%:
	@if [ "$*" = "test" ] || [ "$*" = "app" ]; then \
		echo "Building target: $*"; \
		$(DOCKER) build --target $* -t $(BASE_IMAGE_NAME)-$* . --build-arg API_PORT="$(API_PORT)"; \
	else \
		echo "Invalid target: $*. Only 'test' and 'app' are allowed."; \
		exit 1; \
	fi

	@echo "Running target: $*";
	@if [ "$*" = "test" ]; then \
		$(DOCKER) run --rm $(BASE_IMAGE_NAME)-$*; \
	else \
		$(DOCKER) run --rm -p $(API_PORT):$(API_PORT) $(BASE_IMAGE_NAME)-$*; \
	fi

# Clean target to remove created Docker images
clean:
	@echo
	@echo "Identifying and removing Docker image(s):"

	@for target in test app; do \
		$(DOCKER) image inspect $(BASE_IMAGE_NAME)-$$target > /dev/null 2>&1 && \
		$(DOCKER) rmi $(BASE_IMAGE_NAME)-$$target || true; \
	done

# Dummy count python lines
lines:
	@find . -name '*.py' \( -not -iname "__init__.py" \) | xargs wc -l | sort
