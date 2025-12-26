# Architecture Overview for ChangeGuard

This document describes the overall system architecture, components, and their interactions.

---

## 1. System Components

### 1.1 Frontend
- **Technology:** React + TypeScript + Tailwind CSS + shadcn/ui  
- **Responsibilities:**
  - UI rendering
  - Input validation
  - Consuming backend API
  - Optional: WebSocket subscription for real-time updates

### 1.2 Backend
- **Technology:** Python (FastAPI)
- **Responsibilities:**
  - REST API endpoints for CRUD operations
  - Input validation and business logic
  - Authentication & authorization (JWT)
  - Interact with database and cache
  - Publish/consume events for async tasks

### 1.3 Database
- **Primary DB:** PostgreSQL
  - Stores users, tasks, comments, organizations, etc.
- **Cache:** Redis
  - Caching frequently accessed data (task lists, dashboard stats)
  - Optional: Pub/Sub for lightweight messaging

### 1.4 Messaging / Async Services
- **Options:** NATS or RabbitMQ
- **Use Cases:**
  - Notifications
  - Audit logging
  - Background jobs (emails, scheduled tasks)

### 1.5 Optional Services
- Email service (SMTP / SES)
- Analytics microservice
- Feature flag service (LaunchDarkly / Flagsmith)

---

## 2. Data Flow

- Refer to [DATA_FLOW.md](./DATA_FLOW.md) for detailed request and event flows.  
- Key patterns:
  - Backend as source of truth
  - Redis caching for performance
  - Event-driven architecture for async tasks
  - WebSocket for real-time updates

---

## 3. Deployment Architecture

- **Dockerized environment** for dev, staging, and production
- **CI/CD:** GitHub Actions
- **Cloud:** AWS (EC2 / ECS / RDS / S3)
- **Optional:** Kubernetes for microservice scaling

---

## 4. High-Level Architecture Diagram

```mermaid
flowchart LR
    subgraph Frontend
        A[React App]
    end

    subgraph Backend
        B[FastAPI Server] --> C[PostgreSQL]
        B --> D[Redis Cache]
        B --> E[Message Broker]
    end

    subgraph Async Services
        E --> F[Notification Service]
        E --> G[Audit Logging Service]
        E --> H[Email Service]
    end

    A --> B
    F --> A
    G --> A
