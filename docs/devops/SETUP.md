# Development Setup

## Prerequisites
- Python 3.11+
- Node.js 20+
- npm or pnpm
- Docker & Docker Compose
- PostgreSQL locally or via Docker

## Steps
1. Clone the repo: `git clone https://github.com/yourusername/changeguard.git`
2. Copy environment variables: `cp .env.example .env`
3. Install frontend dependencies: `cd frontend && npm install`
4. Install backend dependencies: `pip install -r backend/requirements.txt`
5. Start backend: `uvicorn backend.main:app --reload --host 0.0.0.0 --port 8080`
6. Start frontend: `npm run dev`
7. Access app at: `http://localhost:3000`

## Notes
- Use `pip` to manage Python dependencies
- Create and activate virtual environment: `python -m venv venv && source venv/bin/activate`
- Use Docker Compose for local database setup
