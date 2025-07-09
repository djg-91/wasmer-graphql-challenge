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
	@$(DJANGO) collectstatic

migrate: ## Apply database migrations
	@$(DJANGO) migrate

makemigrations: ## Create new migrations based on model changes
	@$(DJANGO) makemigrations

shell: ## Open Django interactive shell
	@$(DJANGO) shell

dump-fixtures: ## Export current database data into fixtures.json
	@$(DJANGO) dumpdata --indent 2 > fixtures.json

load-fixtures: ## Load fixtures from fixtures.json
	@$(DJANGO) loaddata fixtures.json

graphql-schema: ## Export GraphQL schema to schema.graphql
	@$(DJANGO) graphql_schema --schema=api.schema.schema --out=schema.graphql

format: ## Format code with Ruff
	@$(UV) ruff format src

lint: ## Run linter using Ruff
	@$(UV) ruff check src

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}'
