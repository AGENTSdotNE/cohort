.PHONY: install dev db backend frontend storybook test format migrate superuser seed

install:
	cd backend && uv sync
	cd frontend && npm install

dev:
	docker compose up

db:
	docker compose up -d db

migrate:
	cd backend && uv run python manage.py migrate

superuser:
	docker compose exec backend uv run python manage.py createsuperuser

seed:
	docker compose exec backend uv run python manage.py seed

backend:
	cd backend && uv run python manage.py runserver

frontend:
	cd frontend && npm run dev

storybook:
	docker compose exec frontend npm run storybook -- --host 0.0.0.0 --no-open

test:
	cd backend && uv run ruff check . && uv run ruff format --check . && uv run python manage.py makemigrations --check --dry-run && uv run python manage.py test
	cd frontend && npm run lint && npm run format:check && npm run typecheck && npm run build

format:
	cd backend && uv run ruff check --fix . && uv run ruff format .
	cd frontend && npm run format && npx eslint --fix .
