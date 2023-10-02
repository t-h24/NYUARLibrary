tests:
	docker compose up --build

migrate:
	docker compose exec python manage.py migrate

makemigrations:
	docker compose exec python manage.py makemigrations