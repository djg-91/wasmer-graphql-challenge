#!/bin/bash
set -e

# Generate static
uv run python src/manage.py collectstatic --no-input

# Run migrations
uv run python src/manage.py migrate

# Final command to run the app
uv run uvicorn config.asgi:application --app-dir src --host 0.0.0.0 --port 8000

