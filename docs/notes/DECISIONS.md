# Architectural Decisions

This document tracks key technical decisions made during ChangeGuard development.

## ADR-001: Language Choice - Go for Backend

**Decision**: Use Go 1.21 for backend API server

**Rationale**:
- **Performance**: Fast execution, efficient memory usage - critical for high-throughput API
- **Concurrency**: Goroutines handle thousands of concurrent requests easily
- **Deployment**: Single binary, minimal dependencies, easy Docker containerization
- **gRPC Ready**: Go has first-class gRPC support for future internal service communication
- **Standard Library**: Robust HTTP, JSON, crypto packages reduce dependencies

**Alternatives Considered**:
- Python: Slower, requires runtime, but faster to develop (chose Go for scale)
- Node.js: Good concurrency, but less performant for data-heavy operations
- Rust: Better performance, but slower development cycle

**Status**: Accepted ✓

## ADR-002: Primary Database - PostgreSQL

**Decision**: Use PostgreSQL 16 as primary datastore

**Rationale**:
- **Reliability**: ACID compliance, proven in production
- **Schema Flexibility**: JSONB support for flexible metadata storage
- **Querying**: Complex filtering and aggregations on change records
- **Full-Text Search**: Built-in FTS for searching change descriptions
- **Transactions**: Multi-row transactions for data consistency
- **RDS Ready**: AWS RDS has excellent PostgreSQL support

**Alternatives Considered**:
- MongoDB: NoSQL flexibility, but SQL is better for structured change data
- MySQL: Similar to PostgreSQL, but PostgreSQL has better features
- DynamoDB: Good for scale, but overkill for initial data volume

**Status**: Accepted ✓

## ADR-003: Caching Layer - Redis

**Decision**: Use Redis 7 for distributed caching and session storage

**Rationale**:
- **Performance**: In-memory caching for frequently accessed data
- **Session Management**: JWT tokens stored with optional expiration
- **Pub/Sub**: Foundation for future real-time notifications
- **Persistence**: AOF persistence ensures no data loss on restart
- **Cluster Ready**: Redis Cluster support for horizontal scaling

**Alternatives Considered**:
- Memcached: Simpler, but no persistence or pub/sub
- In-process Cache (Go): Simple, but not distributed across instances
- DynamoDB: AWS-native, but higher latency than Redis

**Status**: Accepted ✓

## ADR-004: Frontend Framework - React + TypeScript + Vite

**Decision**: Build frontend with React 18, TypeScript 5.3, Vite 5.0

**Rationale**:
- **Developer Experience**: Fast HMR in Vite, excellent TypeScript integration
- **Type Safety**: TypeScript catches errors at compile time
- **Component Reusability**: React components well-suited for complex UI
- **Performance**: Vite produces optimized bundles with code splitting
- **Ecosystem**: Large ecosystem for UI components, testing, etc.

**Alternatives Considered**:
- Vue.js: Similar capabilities, but React has larger ecosystem
- Next.js: Overkill for SPA, would add unnecessary complexity
- jQuery: Too primitive for modern web app

**Status**: Accepted ✓

## ADR-005: Styling - Tailwind CSS

**Decision**: Use Tailwind CSS 3.3 for styling

**Rationale**:
- **Consistency**: Utility classes ensure consistent spacing, colors, typography
- **Performance**: Unused CSS is purged from production bundles
- **Customization**: Tailwind config allows brand-specific theming
- **Learning**: Developers can style without context-switching to CSS files

**Alternatives Considered**:
- CSS Modules: More flexible but more verbose
- Styled Components: Runtime performance overhead
- Bootstrap: Heavier, less customizable

**Status**: Accepted ✓

## ADR-006: State Management - React Query + Context API

**Decision**: Use React Query (TanStack) for server state, Context API for UI state

**Rationale**:
- **Server State**: React Query handles API caching, refetching, synchronization
- **UI State**: Context API sufficient for theme, layout, modal state
- **Separation**: Clear boundary between server and UI concerns
- **Performance**: React Query reduces unnecessary re-renders

**Alternatives Considered**:
- Redux: Overkill complexity for this app's state needs
- MobX: Good, but React Query more specialized for server state
- Zustand: Simpler than Redux, but React Query better for API data

**Status**: Accepted ✓

## ADR-007: Containerization - Docker

**Decision**: Use Docker for containerization with Docker Compose for orchestration

**Rationale**:
- **Reproducibility**: Same environment for dev, staging, production
- **Simplicity**: Single docker-compose.yml runs all services
- **Cloud Ready**: Images easily deployed to ECS, EKS, etc.
- **Developer Experience**: One command starts entire stack

**Alternatives Considered**:
- Kubernetes: Too complex for current scale, easy to add later
- VMs: Slower to start, larger footprint, less portable
- Serverless: Not suitable for stateful services (database, cache)

**Status**: Accepted ✓

## ADR-008: CI/CD - GitHub Actions

**Decision**: Use GitHub Actions for CI/CD pipeline

**Rationale**:
- **Native Integration**: Deep GitHub integration, no external service needed
- **Simple Syntax**: YAML workflows easy to understand
- **Cost**: Free for public repos, reasonable pricing for private
- **Matrix Testing**: Easy to test against multiple versions

**Alternatives Considered**:
- Jenkins: More powerful but requires self-hosted infrastructure
- GitLab CI: Requires GitLab, repository already on GitHub
- AWS CodePipeline: Vendor lock-in, more complex

**Status**: Accepted ✓

## ADR-009: Deployment Target - AWS

**Decision**: Deploy to AWS using EC2 (compute), RDS (database), ElastiCache (cache)

**Rationale**:
- **Ecosystem**: Comprehensive services (ALB, CloudWatch, SNS, etc.)
- **Reliability**: 99.99% uptime SLA, multi-AZ availability
- **Scaling**: Auto Scaling Groups for dynamic capacity
- **Security**: Mature IAM, Security Groups, encryption services
- **Cost**: Competitive pricing, Reserved Instances for commitment discounts

**Alternatives Considered**:
- GCP: Similar capabilities, team more familiar with AWS
- Azure: Similar capabilities, but less cost-effective for this scale
- DigitalOcean: Simpler but less powerful than major clouds

**Status**: Accepted ✓

## ADR-010: Authentication - JWT

**Decision**: Use JWT (JSON Web Tokens) for stateless authentication

**Rationale**:
- **Scalability**: No server-side session storage needed
- **Microservices Ready**: Tokens can be verified by any backend instance
- **Mobile Friendly**: Natural fit for mobile and API clients
- **Refresh Strategy**: Refresh tokens enable long sessions with short token expiry

**Alternatives Considered**:
- Session Cookies: Simpler but requires session storage
- OAuth2: More complex, needed only for 3rd party integration
- API Keys: Less secure, no expiration

**Status**: Accepted ✓

## ADR-011: Future Real-Time Communication - WebSockets

**Decision**: Plan for WebSocket support in v0.2 for real-time notifications

**Rationale**:
- **Low Latency**: Real-time updates without polling
- **Scalability**: Go's concurrency handles many WebSocket connections
- **User Experience**: Instant notification of new schema changes
- **Upgrade Path**: Can add to current architecture without major refactoring

**Implementation**: v0.2 (not v0.1)

**Alternatives Considered**:
- Server-Sent Events (SSE): Simpler but one-way communication
- Polling: Simple but inefficient and high latency

**Status**: Planned for v0.2 ✓

## ADR-012: API Design - RESTful with Structured Errors

**Decision**: Use RESTful API design with standardized error responses

**Rationale**:
- **Standard**: REST is well-understood, predictable
- **Errors**: Structured error responses enable consistent client handling
- **Pagination**: Cursor + offset pagination for large datasets
- **Versioning**: API versioning via `/api/v1` allows backward compatibility

**Alternatives Considered**:
- GraphQL: More flexible but adds complexity for current needs
- gRPC: Internal microservices only, not for public API

**Status**: Accepted ✓

## Decision Log

| ID | Decision | Accepted | Rationale |
|----|----------|----------|-----------|
| ADR-001 | Go backend | ✓ | Performance, concurrency, deployment |
| ADR-002 | PostgreSQL | ✓ | Reliability, ACID, querying |
| ADR-003 | Redis | ✓ | Caching performance, pub/sub |
| ADR-004 | React + TS + Vite | ✓ | DX, type safety, performance |
| ADR-005 | Tailwind CSS | ✓ | Consistency, performance |
| ADR-006 | React Query + Context | ✓ | Clear state separation |
| ADR-007 | Docker | ✓ | Reproducibility, portability |
| ADR-008 | GitHub Actions | ✓ | Native integration, simplicity |
| ADR-009 | AWS | ✓ | Reliability, ecosystem |
| ADR-010 | JWT | ✓ | Scalability, microservices-ready |
| ADR-011 | WebSockets (v0.2) | ✓ | Low latency, great UX |
| ADR-012 | RESTful API | ✓ | Standard, predictable |

## Future Decisions Needed

- **Message Queue**: NATS vs RabbitMQ vs SQS for async processing
- **Metrics**: Prometheus vs CloudWatch for metrics collection
- **Observability**: ELK vs DataDog for logs and tracing
- **Multi-Tenancy**: Shared database vs per-tenant database
- **Mobile App**: Native (iOS/Android) vs React Native vs PWA
