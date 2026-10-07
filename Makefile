.PHONY: install dev db backend frontend storybook test format migrate superuser

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
	cd backend && uv run python manage.py createsuperuser

backend:
	cd backend && uv run python manage.py runserver

frontend:
	cd frontend && npm run dev

storybook:
	cd frontend && npm run storybook

test:
	cd backend && uv run ruff check . && uv run ruff format --check . && uv run python manage.py test
	cd frontend && npm run lint && npm run format:check && npm run typecheck

format:
	cd backend && uv run ruff check --fix . && uv run ruff format .
	cd frontend && npm run format && npx eslint --fix .
