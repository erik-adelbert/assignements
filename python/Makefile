.PHONY: all build-run-app build-run-test launch-drive docker-% clean

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
launch-drive:
	python app_driver.py $(API_PORT)

# Pattern rule for docker targets restricted to "test" or "app"
docker-%:
	@if [ "$*" = "test" ] || [ "$*" = "app" ]; then \
		echo "Building target: $*"; \
		$(DOCKER) build --target $* -t $(BASE_IMAGE_NAME)-$* .; \
	else \
		echo "Invalid target: $*. Only 'test' and 'app' are allowed."; \
		exit 1; \
	fi

	@echo "Running target: $*";
	@if [ "$*" = "test" ]; then \
		$(DOCKER) run --rm $(BASE_IMAGE_NAME)-$*; \
	else \
		$(DOCKER) run --rm -p $(API_PORT):8000 $(BASE_IMAGE_NAME)-$*; \
	fi

# Clean target to remove created Docker images
clean:
	@echo
	@echo "Identifying and removing Docker image(s):"

	@docker image inspect $(BASE_IMAGE_NAME)-test > /dev/null 2>&1 && \
	$(DOCKER) rmi $(BASE_IMAGE_NAME)-test || true

	@docker image inspect $(BASE_IMAGE_NAME)-app > /dev/null 2>&1 && \
	$(DOCKER) rmi $(BASE_IMAGE_NAME)-app || true
