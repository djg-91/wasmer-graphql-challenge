# Base image
FROM python:3.13-slim

# Install uv official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_HTTP_TIMEOUT=60

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy uv files and install dependencies
COPY pyproject.toml uv.lock /app/
RUN uv sync --frozen --no-cache

# Copy project files
COPY . .

# Expose port
EXPOSE 8000

# Set entrypoint script
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"] 
