.PHONY: all build-run-app build-run-test launch-drive docker-% clean

# Default to testing
all: docker-test clean

# Build and run a standalone containerized app
build-run-app: docker-app

# Build and run containerized tests
build-run-test: docker-test

# Launch a drive test build-run-test must be running
launch-drive:
	python app_driver.py

# Define the base image name
BASE_IMAGE_NAME := user-service

# Pattern rule for docker targets restricted to "test" or "app"
docker-%:
	@if [ "$*" = "test" ] || [ "$*" = "app" ]; then \
		echo "Building and running target: $*"; \
		docker build --target $* -t $(BASE_IMAGE_NAME)-$* .; \
		docker run --rm $(BASE_IMAGE_NAME)-$*; \
	else \
		echo "Invalid target: $*. Only 'test' and 'app' are allowed."; \
		exit 1; \
	fi

# Clean target to remove created Docker images
clean:
	@docker image inspect $(BASE_IMAGE_NAME)-test > /dev/null 2>&1 && \
	docker rmi user-service-test || true

	@docker image inspect $(BASE_IMAGE_NAME)-test-app > /dev/null 2>&1 && \
	docker rmi user-service-app || true
