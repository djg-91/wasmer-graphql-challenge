.PHONY: \
	run \
	collectstatic \
	migrate \
	makemigrations \
	shell \
	dump-fixtures \
	load-fixtures \
	graphql-schema \
	format \
	lint \
	help

UV = uv run
DJANGO = @$(UV) python src/manage.py

run: ## Start the ASGI server with auto-reload
	@$(UV) uvicorn config.asgi:application --reload --app-dir src

collectstatic: ## Collect static files into STATIC_ROOT
	@$(DJANGO) collectstatic --no-input

migrate: ## Apply database migrations
	@$(DJANGO) migrate

makemigrations: ## Create new migrations based on model changes
	@$(DJANGO) makemigrations

load-fixtures: ## Load fixtures from fixtures.json
	@$(DJANGO) loaddata fixtures.json

graphql-schema: ## Export GraphQL schema to schema.graphql
	@$(DJANGO) graphql_schema --schema=api.schema.schema --out=schema.graphql

docker-build: ## Build Docker image
	@docker build -t wasmer-graphql .

docker-run: ## Stop, remove if exists, then run Docker container
	@docker stop wasmer-graphql-container 2>/dev/null
	@docker rm wasmer-graphql-container 2>/dev/null
	@docker run -d \
		-p 8000:8000 \
		--env-file .env \
		--name wasmer-graphql-container \
		wasmer-graphql

format: ## Format code with Ruff
	@$(UV) ruff format src

lint: ## Run linter using Ruff
	@$(UV) ruff check src

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}'
