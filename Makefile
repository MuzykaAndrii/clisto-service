up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker logs --follow backend

migrations:
	docker exec backend alembic revision --autogenerate

migrate:
	docker exec backend alembic upgrade head

shell:
	docker exec -it backend sh