# Development Setup

## Prerequisites
- Go 1.21+
- Node.js 20+
- npm or pnpm
- Docker & Docker Compose
- PostgreSQL locally or via Docker

## Steps
1. Clone the repo: `git clone https://github.com/yourusername/changeguard.git`
2. Copy environment variables: `cp .env.example .env`
3. Install frontend dependencies: `cd frontend && npm install`
4. Start backend: `go run ./cmd/server`
5. Start frontend: `npm run dev`
6. Access app at: `http://localhost:3000`

## Notes
- Use Go Modules (`go mod tidy`) to install dependencies
- Use Docker Compose for local database setup
