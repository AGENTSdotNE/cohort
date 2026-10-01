FROM node:24-slim AS frontend
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
WORKDIR /app
COPY backend/pyproject.toml backend/uv.lock ./
RUN uv sync --frozen --no-dev
COPY backend/ ./
COPY --from=frontend /frontend/dist ./frontend_dist
RUN uv run python manage.py collectstatic --noinput

CMD uv run python manage.py migrate && uv run gunicorn config.wsgi --bind 0.0.0.0:${PORT:-8000}
