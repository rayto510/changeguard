# ChangeGuard Data Flow (v1)

This document illustrates how data moves through ChangeGuard v1, specifically for tracking schema/API breaking changes, now aligned with the high-level architecture.

---

## 1. Overview

ChangeGuard v1 tracks breaking schema/API changes, notifies affected teams, and keeps an audit trail. Main components:

- **Frontend:** React + TypeScript UI for viewing schema changes, adding comments, and managing notifications.
- **Backend:** Go API handles CRUD operations, notifications, caching, and async messaging.
- **Database:** PostgreSQL stores schema changes, comments, users, and notifications.
- **Cache:** Redis for caching frequently accessed data.
- **Message Broker:** Facilitates async services like notifications, audit logging, and email alerts.

---

## 2. Data Flow for a Breaking Change

### Step 1: Record a Schema Change

1. Developer detects/plans a schema change (e.g., removing a column).
2. Frontend sends `POST /schema-changes` to backend.
3. Backend:
   - Validates the change.
   - Stores it in PostgreSQL.
   - Updates Redis cache if necessary.
   - Publishes a message to the message broker.
4. Message broker distributes events to async services.

---

### Step 2: Async Services Triggered

1. **Notification Service**
   - Sends notifications to affected users.
   - Updates PostgreSQL notification table.
   - Can push real-time updates via WebSocket to frontend.

2. **Audit Logging Service**
   - Logs the schema change and all updates/comments for historical tracking.

3. **Email Service**
   - Sends email alerts to affected users (optional for v1).

---

### Step 3: Comments & Collaboration

1. Developers comment on schema changes via `POST /schema-changes/:id/comments`.
2. Backend stores comments in PostgreSQL.
3. Async services may notify relevant users of new comments.
4. Frontend state updates to reflect new comments in real-time (via cache or WebSocket).

---

### Step 4: Resolve Changes

1. When a change is addressed, developer updates status via `PUT /schema-changes/:id`.
2. Backend updates PostgreSQL and Redis cache.
3. Async services notify stakeholders and log the resolution in audit service.
4. Frontend reflects resolved state and notifications are marked accordingly.

---

## 3. Notifications Flow

- **Trigger:** New breaking change or comment.
- **Backend:** Publishes event to message broker.
- **Notification Service:** Creates notification entries and pushes real-time updates.
- **Frontend:** Updates notifications list; users mark as read via `PUT /notifications/:id/read`.

---

## 4. Updated Data Flow Diagram

```mermaid
flowchart LR
    subgraph Frontend
        A[React App]
    end

    subgraph Backend
        B[Go API] --> C[PostgreSQL]
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
