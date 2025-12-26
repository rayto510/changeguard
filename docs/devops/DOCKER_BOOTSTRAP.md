# Docker Bootstrap Guide for ChangeGuard

## Overview

This guide will help you set up ChangeGuard using Docker and Docker Compose. The setup includes:

- **PostgreSQL**: Primary database
- **Redis**: Caching layer
- **FastAPI Backend**: REST API server on port 8080
- **React Frontend**: Web UI served via Nginx on port 3000

## Prerequisites

- Docker Desktop (includes Docker and Docker Compose)
- Docker version 20.10+ or higher
- Docker Compose version 2.0+ or higher
- At least 4GB of available RAM
- 10GB of disk space (additional space for Python dependencies)

### Installing Docker

**macOS:**
```bash
# Using Homebrew
brew install --cask docker

# Or download from: https://www.docker.com/products/docker-desktop
```

**Linux:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

**Windows:**
Download Docker Desktop from https://www.docker.com/products/docker-desktop

## Quick Start

### 1. Initial Setup

```bash
# Clone the repository (if not already done)
git clone https://github.com/rayto510/changeguard.git
cd changeguard

# Copy environment variables
cp .env.example .env

# (Optional) Edit .env for custom configuration
# nano .env
```

### 2. Build and Start Containers

```bash
# Build images
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### 3. Verify Services

```bash
# Check container status
docker-compose ps

# Access the application
# Frontend:  http://localhost:3000
# Backend:   http://localhost:8080
# Database:  localhost:5432
# Redis:     localhost:6379
```

### 4. Stop Services

```bash
# Stop all containers
docker-compose down

# Remove containers and volumes (full reset)
docker-compose down -v
```

## Using Make Commands

If you have `make` installed, use these shortcuts:

```bash
# Setup development environment
make dev-setup

# Build images
make docker-build

# Start containers
make docker-up

# View logs
make docker-logs

# Stop containers
make docker-down

# Reset everything
make docker-reset

# Open shell in backend
make docker-shell

# Connect to database
make docker-shell-db
```

## File Structure

```
changeguard/
├── Dockerfile.backend       # Go backend image
├── Dockerfile.frontend      # React frontend image
├── docker-compose.yml       # Service orchestration
├── .env.example             # Environment template
├── .dockerignore            # Docker build exclusions
├── Makefile                 # Convenient commands
├── scripts/
│   └── init.sql             # Database initialization
└── frontend/
    └── nginx.conf           # Nginx configuration
```

## Configuration

### Environment Variables

Edit `.env` to customize:

```env
# Database
DB_USER=changeguard
DB_PASSWORD=changeguard
DB_NAME=changeguard

# Backend
JWT_SECRET=your-secret-key-change-in-production
PORT=8080
ENVIRONMENT=development

# Frontend
VITE_API_URL=http://localhost:8080/api
```

### Ports

| Service | Port | URL |
|---------|------|-----|
| Frontend | 3000 | http://localhost:3000 |
| Backend API | 8080 | http://localhost:8080 |
| PostgreSQL | 5432 | localhost |
| Redis | 6379 | localhost |

## Common Tasks

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### Access Database

```bash
# Using psql
docker-compose exec postgres psql -U changeguard -d changeguard

# Or with make
make docker-shell-db

# Common SQL commands
\dt                    # List tables
\d users               # Describe table
SELECT * FROM users;   # Query data
\q                     # Quit
```

### Access Backend Shell

```bash
# Open shell in backend container
docker-compose exec backend sh

# Or with make
make docker-shell
```

### Rebuild After Changes

```bash
# Rebuild images after code changes
docker-compose build

# Rebuild specific service
docker-compose build backend

# Restart service
docker-compose up -d --no-deps backend
```

### Clear Everything

```bash
# Remove containers, volumes, and images
docker-compose down -v
docker system prune -a

# Then rebuild and restart
docker-compose build
docker-compose up -d
```

## Troubleshooting

### Containers Won't Start

```bash
# Check logs for errors
docker-compose logs

# Ensure ports aren't in use
lsof -i :3000
lsof -i :8080
lsof -i :5432

# Kill processes using ports
kill -9 <PID>
```

### Database Connection Failed

```bash
# Verify database is running
docker-compose exec postgres pg_isready

# Check connection
docker-compose exec postgres psql -U changeguard -d changeguard -c "SELECT 1;"

# Reset database
docker-compose down -v
docker-compose up -d postgres
```

### Frontend Not Updating

```bash
# Rebuild frontend image
docker-compose build frontend

# Restart frontend
docker-compose up -d frontend

# Check volume mounts
docker inspect changeguard-frontend | grep -A 10 Mounts
```

### Memory Issues

```bash
# Check Docker resource usage
docker stats

# Increase Docker memory in settings or:
# Edit docker-compose.yml to add limits:
# services:
#   backend:
#     mem_limit: 1g
```

## Development Workflow

### Local Development with Hot Reload

```bash
# docker-compose.yml already mounts source directories
# Changes to code are automatically reflected:
# - backend: Go changes require service restart
# - frontend: Hot reload via Vite

# For backend changes
docker-compose exec backend go run ./cmd/server

# Frontend automatically reloads when files change
```

### Running Tests

```bash
# Backend tests
docker-compose exec backend go test ./...

# Frontend tests (if configured)
docker-compose exec frontend npm test
```

### Database Migrations

Add migration files to `scripts/` and they'll run on startup:

```bash
# Create migration
cat > scripts/02-add-columns.sql << 'EOF'
ALTER TABLE schema_changes ADD COLUMN priority INT DEFAULT 1;
EOF

# Restart database
docker-compose restart postgres
```

## Production Considerations

### Security

1. **Change default credentials** in `.env`:
   ```env
   DB_PASSWORD=<strong-random-password>
   JWT_SECRET=<strong-random-secret>
   ```

2. **Use environment-specific configs**:
   ```bash
   # Create production override
   cp docker-compose.yml docker-compose.prod.yml
   # Edit docker-compose.prod.yml with production settings
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Enable SSL/TLS** for HTTPS

4. **Restrict CORS** in `CORS_ALLOWED_ORIGINS`

### Scaling

Use Docker Compose profiles or Kubernetes for production scaling.

### Monitoring

```bash
# Resource usage
docker stats

# Container health
docker-compose ps

# Logs with timestamps
docker-compose logs --timestamps
```

## Next Steps

1. **Customize** `.env` with your settings
2. **Add features** to your backend/frontend
3. **Create database migrations** in `scripts/`
4. **Set up CI/CD** (see `docs/devops/CI_CD.md`)
5. **Deploy** to AWS/Cloud (see `docs/devops/DEPLOYMENT.md`)

## Support

For more information, see:
- Architecture: `docs/architecture/ARCHITECTURE.md`
- Setup: `docs/devops/SETUP.md`
- CI/CD: `docs/devops/CI_CD.md`
- Deployment: `docs/devops/DEPLOYMENT.md`

