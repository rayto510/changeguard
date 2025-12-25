# Docker Setup

## Backend
- Dockerfile builds Go backend
- Ports: 8080 (API)

## Frontend
- Dockerfile builds React app
- Ports: 3000

## Docker Compose
- Runs PostgreSQL, Redis, backend, frontend
- Example command: `docker-compose up --build`

## Volumes
- `db_data` for PostgreSQL persistence
- `redis_data` for Redis persistence
