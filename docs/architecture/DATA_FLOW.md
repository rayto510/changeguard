# ChangeGuard Data Flow (v1)

This document illustrates how data moves through ChangeGuard v1, specifically for tracking schema/API breaking changes.

---

## 1. Overview

ChangeGuard v1 tracks breaking changes in schemas or APIs, notifies affected teams, and keeps an audit trail. The main components are:

- **Frontend:** React + TypeScript UI for viewing schema changes, adding comments, and managing notifications.
- **Backend:** Go API handles CRUD operations, notifications, and change tracking.
- **Database:** PostgreSQL stores schema changes, comments, users, and notifications.
- **Cache / Messaging:** Redis for caching and optional pub/sub for real-time notifications.

---

## 2. Data Flow for a Breaking Change

### Step 1: Record a Schema Change

1. Developer detects or plans a schema change (e.g., removing a column).
2. Frontend sends `POST /schema-changes` to backend.
3. Backend:
   - Validates the change.
   - Stores it in PostgreSQL.
   - Marks the change as `open`.
   - Determines affected services or teams.

---

### Step 2: Notify Affected Teams

1. Backend generates notifications for all affected users/services.
2. Notifications are saved in PostgreSQL.
3. Optional: publish to Redis pub/sub for real-time updates to subscribed clients.
4. Users receive alerts in the frontend via WebSocket or polling.

---

### Step 3: Comment and Collaborate

1. Developers can comment on a schema change via `POST /schema-changes/:id/comments`.
2. Backend stores comments in PostgreSQL linked to the schema change.
3. All relevant users are notified of new comments.

---

### Step 4: Resolve Changes

1. When a change is addressed, a developer updates its status via `PUT /schema-changes/:id` (e.g., `status=resolved`).
2. Backend updates the record and notifies stakeholders.
3. Audit logs maintain history of changes, status updates, and comments.

---

## 3. Notifications Flow

- **Trigger:** Any new breaking change or comment.
- **Backend:** Creates notification entries per affected user.
- **Delivery:** Real-time via WebSocket or via frontend polling.
- **User Action:** `PUT /notifications/:id/read` marks notifications as read.

---

## 4. Data Flow Diagram

```mermaid
flowchart LR
    subgraph Frontend
        A[User Interface]
    end

    subgraph Backend
        B[Go API] --> C[PostgreSQL DB]
        B --> D[Redis Cache / PubSub]
    end

    subgraph Notifications & Audit
        D --> E[Notification Service]
        D --> F[Audit Log Service]
    end

    A --> B
    E --> A
