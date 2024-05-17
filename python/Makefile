.PHONY: clean

clean:
	docker rmi user-service-test || true
	docker rmi user-service-app || true

docker-test:
	docker build --target testing -t user-service-test .
	docker run --rm user-service-test

docker-app:
	docker build --target standalone -t user-service-app .
	docker run --rm -p 8000:8000 user-service-app

user-service-drive:
	python app_driver.py
