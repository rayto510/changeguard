# State Management

## Frontend State
- Local state: React `useState` for simple UI state
- Global state: Zustand or React Query for server state
- Caching: use React Query caching + Redis on backend

## Backend State
- Database as source of truth
- Redis for caching frequently accessed data
