.PHONY: help docker-build docker-up docker-down docker-logs docker-clean docker-reset

help:
	@echo "ChangeGuard Docker Commands"
	@echo "============================"
	@echo "make docker-build    - Build Docker images"
	@echo "make docker-up       - Start all containers"
	@echo "make docker-down     - Stop all containers"
	@echo "make docker-logs     - View container logs"
	@echo "make docker-clean    - Remove stopped containers and unused images"
	@echo "make docker-reset    - Reset everything (volumes included)"
	@echo "make docker-shell    - Open shell in backend container"
	@echo "make db-migrate      - Run database migrations"

docker-build:
	@echo "Building Docker images..."
	docker-compose build

docker-up:
	@echo "Starting containers..."
	docker-compose up -d
	@echo "Services starting:"
	@echo "  Frontend:  http://localhost:3000"
	@echo "  Backend:   http://localhost:8080"
	@echo "  Database:  localhost:5432"
	@echo "  Redis:     localhost:6379"

docker-down:
	@echo "Stopping containers..."
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-logs-backend:
	docker-compose logs -f backend

docker-logs-frontend:
	docker-compose logs -f frontend

docker-logs-db:
	docker-compose logs -f postgres

docker-clean:
	@echo "Cleaning up stopped containers and unused images..."
	docker-compose down
	docker system prune -f

docker-reset:
	@echo "Resetting everything (removing volumes)..."
	docker-compose down -v
	@echo "Reset complete. Run 'make docker-up' to start fresh."

docker-shell:
	docker-compose exec backend sh

docker-shell-db:
	docker-compose exec postgres psql -U changeguard -d changeguard

docker-ps:
	docker-compose ps

# Development shortcuts
dev-setup:
	@echo "Setting up development environment..."
	cp .env.example .env
	@echo "Environment file created. Update .env if needed."
	@echo "Run 'make docker-up' to start the application."

dev-logs:
	docker-compose logs -f backend frontend postgres redis
