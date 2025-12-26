# ChangeGuard

Schema and API change tracking platform for microservices. Track breaking changes, coordinate across teams, and prevent integration failures.

## Problem

In microservice architectures, breaking schema and API changes cause integration failures that disrupt teams and slow deployments. ChangeGuard provides visibility, collaboration, and coordination for these critical changes.

## Features

- **Change Tracking**: Record and categorize schema/API changes (breaking, non-breaking, deprecation)
- **Team Collaboration**: Comments, discussions, and team notifications on every change
- **Impact Analysis**: See which services and teams are affected by each change
- **Status Workflows**: Track changes from draft → open → in-progress → resolved → archived
- **Real-time Notifications**: Affected teams notified immediately of breaking changes
- **Deployment Coordination**: Link changes to deployment dates and track progress
- **Audit Trail**: Complete history of all changes and team discussions

## Tech Stack

### Backend
- **Language**: Python 3.11
- **Framework**: FastAPI (HTTP) with async/await patterns
- **Database**: PostgreSQL 16 (primary datastore)
- **Cache**: Redis 7 (distributed caching with AOF persistence)
- **Auth**: JWT with role-based access control
- **ASGI Server**: Uvicorn for production deployments
- **Future**: WebSockets for real-time updates, gRPC for internal services

### Frontend
- **Framework**: React 18 with TypeScript 5.3
- **Build**: Vite 5.0 (fast dev server, optimized builds)
- **Styling**: Tailwind CSS 3.3 + PostCSS
- **State**: React Query (TanStack) for server state, React Context for UI state
- **HTTP**: Axios with interceptors for error handling
- **Date**: date-fns for formatting

### Infrastructure
- **Containerization**: Docker (multi-stage builds for optimization)
- **Orchestration**: Docker Compose (dev), ECS/EKS (prod)
- **Reverse Proxy**: Nginx for static assets and SPA routing
- **CI/CD**: GitHub Actions with multi-stage pipeline
- **Deployment**: AWS (EC2, RDS, ElastiCache, ALB)
- **SSL/TLS**: Let's Encrypt via AWS Certificate Manager

## Project Structure

```
changeguard/
├── backend/              # Backend source code
│   ├── main.py           # Application entry point
│   ├── api/              # API routes and endpoints
│   ├── models/           # Data models and schemas
│   ├── db/               # Database layer and migrations
│   ├── auth/             # Authentication and JWT
│   ├── middleware/       # Middleware (CORS, logging)
│   ├── services/         # Business logic services
│   └── requirements.txt   # Python dependencies
├── tests/                # Unit and integration tests
├── frontend/             # React application
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   └── api/          # API client
│   ├── index.html        # HTML template (Vite)
│   └── vite.config.ts    # Vite configuration
├── scripts/              # Database migrations and init
├── docs/                 # Project documentation
│   ├── architecture/     # API, data flow, state management
│   ├── devops/          # Docker, CI/CD, deployment
│   ├── product/         # Features, UI guidelines, user flows
│   ├── operations/      # Monitoring, security, backup
│   └── notes/           # Decision logs, resources
├── docker-compose.yml    # Multi-service orchestration
├── Dockerfile.backend    # Python application container
├── Dockerfile.frontend   # React application container
├── requirements.txt      # Python dependencies
└── Makefile             # Convenience commands
```

## Quick Start

### Prerequisites
- Docker & Docker Compose (recommended)
- Or: Python 3.11+, Node 20+, PostgreSQL 16, Redis 7

### Docker Setup (Recommended)
```bash
# Clone repository
git clone https://github.com/rayto510/changeguard.git
cd changeguard

# Copy environment template
cp .env.example .env

# Start all services (PostgreSQL, Redis, Backend, Frontend)
docker-compose up --build

# Services running:
# - Frontend: http://localhost:3000
# - Backend: http://localhost:8080
# - PostgreSQL: localhost:5432
# - Redis: localhost:6379
```

### Local Development Setup
```bash
# Backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8080
# Runs on http://localhost:8080

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
# Runs on http://localhost:5173
```

## Configuration

See `.env.example` for all available options:

```bash
# Database
DB_HOST=localhost
DB_PORT=5432
DB_USER=app_user
DB_PASSWORD=secure_password
DB_NAME=changeguard

# Redis
REDIS_URL=redis://localhost:6379/0

# Application
PORT=8080
ENV=development
JWT_SECRET=your-secret-key-32-chars-minimum

# Frontend
REACT_APP_API_URL=http://localhost:8080/api/v1
REACT_APP_ENV=development
```

## API Endpoints

See [API Documentation](docs/architecture/API.md) for complete reference.

### Core Endpoints
- `POST /auth/login` - User authentication
- `POST /auth/register` - Create account
- `GET /schema-changes` - List changes (with filtering)
- `POST /schema-changes` - Create change record
- `GET /schema-changes/:id` - Get change details
- `PUT /schema-changes/:id` - Update change
- `DELETE /schema-changes/:id` - Delete change
- `POST /schema-changes/:id/comments` - Add comment
- `GET /notifications` - Get user notifications

## Database Schema

See [DB Schema Documentation](docs/architecture/DB_SCHEMA.md) for ERD and table definitions.

**Core Tables**:
- `users` - User accounts and authentication
- `schema_changes` - Change records (breaking, non-breaking, deprecation)
- `comments` - Discussion threads on changes
- `notifications` - User notifications for changes
- `teams` - Team organization (future)
- `team_members` - Team membership (future)

## Documentation

- **[Vision & Roadmap](docs/VISION.md)** - Product direction and release timeline
- **[Architecture](docs/architecture/)** - System design, data flows, state management
- **[API Reference](docs/architecture/API.md)** - Complete endpoint documentation
- **[Deployment Guide](docs/devops/DEPLOYMENT.md)** - AWS infrastructure setup
- **[Docker Setup](docs/devops/DOCKER.md)** - Container orchestration
- **[CI/CD Pipeline](docs/devops/CI_CD.md)** - GitHub Actions workflow
- **[Operations](docs/operations/)** - Monitoring, security, backup/recovery

## Development

### Running Tests
```bash
# Backend tests
pytest -v

# Frontend tests
cd frontend
npm run test
```

### Running Linters
```bash
# Backend (Python)
flake8 .
mypy . --ignore-missing-imports

# Frontend
cd frontend
npm run lint
npm run type-check
```

### Building for Production
```bash
# Docker images
docker build -f Dockerfile.backend -t changeguard-backend:latest .
docker build -f Dockerfile.frontend -t changeguard-frontend:latest .

# Or via Docker Compose
docker-compose build
```

## Deployment

### To AWS
See [Deployment Guide](docs/devops/DEPLOYMENT.md) for complete instructions:
1. Set up VPC with public/private subnets
2. Create RDS PostgreSQL and ElastiCache Redis
3. Configure security groups
4. Deploy with GitHub Actions or manual deployment
5. Configure SSL/TLS certificates with Let's Encrypt

### Staging
```bash
git push origin develop
# Auto-deploys to staging via CI/CD
```

### Production
```bash
git push origin main
# Auto-deploys to production via CI/CD (after approval)
```

## Monitoring

- **Logs**: CloudWatch Logs (backend) + browser console (frontend)
- **Metrics**: CloudWatch (CPU, memory, latency, error rate)
- **Uptime**: Health checks on all services every 30 seconds
- **Alerts**: SNS notifications for critical issues

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature/your-feature`
5. Open a Pull Request

### Code Standards
- Follow language-specific style guides (Go fmt, Prettier for JS)
- Write tests for new features (target 80%+ coverage)
- Update docs for API changes
- Use clear commit messages and PR descriptions

## License

MIT License - see LICENSE file for details

## Support

- **Issues**: [GitHub Issues](https://github.com/rayto510/changeguard/issues)
- **Discussions**: [GitHub Discussions](https://github.com/rayto510/changeguard/discussions)
- **Email**: support@changeguard.io

## Roadmap

- **v0.1** (Current): MVP with core features
- **v0.2** (Q1 2026): Real-time updates, WebSockets
- **v1.0** (Q2 2026): RBAC, analytics dashboard, production-ready
- **v2.0** (Q4 2026): Multi-tenant, enterprise features

See [Roadmap](docs/ROADMAP.md) for detailed timeline and features.
