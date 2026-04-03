up:
	docker compose up --build

down:
	docker compose down

migrate:
	docker compose exec web python manage.py migrate

superuser:
	docker compose exec web python manage.py createsuperuser

demo:
	docker compose exec web python manage.py load_demo_data

rebuild:
	docker compose exec web python manage.py rebuild_leaderboard
