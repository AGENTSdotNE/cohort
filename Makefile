.PHONY: install db backend frontend test format migrate superuser

install:
	cd backend && uv sync
	cd frontend && npm install

db:
	docker compose up -d

migrate:
	cd backend && uv run python manage.py migrate

superuser:
	cd backend && uv run python manage.py createsuperuser

backend:
	cd backend && uv run python manage.py runserver

frontend:
	cd frontend && npm run dev

test:
	cd backend && uv run ruff check . && uv run ruff format --check . && uv run python manage.py test
	cd frontend && npm run lint && npm run format:check && npm run typecheck

format:
	cd backend && uv run ruff check --fix . && uv run ruff format .
	cd frontend && npm run format && npx eslint --fix .
