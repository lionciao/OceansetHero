start:
	docker-compose up

p-start:
	docker-compose up -d

p-stop:
	docker-compose down

start_with_build:
	docker-compose up --build

be-logs:
	docker-compose logs -f backend

fe-logs:
	docker-compose logs -f frontend