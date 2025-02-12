.PHONY: build up down logs ps shell migrate test clean

# Default environment variables
COMPOSE=docker-compose
BACKEND_SERVICE=backend
DB_SERVICE=db
REDIS_SERVICE=redis

# Build all services
build:
	$(COMPOSE) build

# Start all services
up:
	$(COMPOSE) up -d

# Stop all services
down:
	$(COMPOSE) down

# View logs
logs:
	$(COMPOSE) logs -f

# Show running containers
ps:
	$(COMPOSE) ps

# Backend shell
shell:
	$(COMPOSE) exec $(BACKEND_SERVICE) /bin/bash

# Database shell
db-shell:
	$(COMPOSE) exec $(DB_SERVICE) psql -U postgres truckdb

# Redis shell
redis-shell:
	$(COMPOSE) exec $(REDIS_SERVICE) redis-cli

# Run database migrations
migrate:
	$(COMPOSE) exec $(BACKEND_SERVICE) poetry run alembic upgrade head

# Generate new migration
migration-new:
	$(COMPOSE) exec $(BACKEND_SERVICE) poetry run alembic revision -m "$(name)"

# Run tests
test:
	$(COMPOSE) exec $(BACKEND_SERVICE) poetry run pytest

# Clean up
clean:
	$(COMPOSE) down -v
	rm -rf backend/__pycache__
	rm -rf backend/.pytest_cache
	rm -rf backend/app/__pycache__
	rm -rf backend/app/**/__pycache__

# Start development environment
dev: build up
	$(COMPOSE) logs -f

# Initialize database (first time setup)
init-db: up
	@echo "Waiting for database to be ready..."
	@sleep 5
	$(MAKE) migrate

# Rebuild and restart a specific service
# Usage: make restart service=backend
restart:
	$(COMPOSE) up -d --build $(service)

# Show help
help:
	@echo "Available commands:"
	@echo "  make build          - Build all services"
	@echo "  make up            - Start all services"
	@echo "  make down          - Stop all services"
	@echo "  make logs          - View logs"
	@echo "  make ps            - Show running containers"
	@echo "  make shell         - Backend shell"
	@echo "  make db-shell      - Database shell"
	@echo "  make redis-shell   - Redis shell"
	@echo "  make migrate       - Run database migrations"
	@echo "  make migration-new - Generate new migration (use with name=migration_name)"
	@echo "  make test          - Run tests"
	@echo "  make clean         - Clean up"
	@echo "  make dev           - Start development environment"
	@echo "  make init-db       - Initialize database (first time setup)"
	@echo "  make restart       - Rebuild and restart a service (use with service=name)"
