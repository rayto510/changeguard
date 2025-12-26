# ChangeGuard State Management (v1)

This document describes how state is managed in the frontend application for ChangeGuard v1, focusing on schema/API breaking changes, comments, and notifications.

---

## 1. State Overview

The frontend state is divided into three main domains:

1. **Schema Changes**
   - Tracks all schema/API changes visible to the user.
   - Includes `id`, `name`, `description`, `change_type`, `status`, `affected_services`, timestamps.
   - Used for rendering change lists, details, and filtering by status or service.

2. **Comments**
   - Stores comments associated with a specific schema change.
   - Includes `id`, `schema_change_id`, `user_id`, `content`, timestamps.
   - Used to render discussion threads on each schema change.

3. **Notifications**
   - Stores all notifications for the current user.
   - Includes `id`, `type`, `payload`, `read`, timestamps.
   - Supports real-time updates and marking notifications as read.

---

## 2. State Management Approach

- **Frontend Framework:** React + TypeScript  
- **State Management Library:** `zustand` or `redux-toolkit` (lightweight, efficient)  
- **Data Fetching / Caching:** `React Query` or `SWR` for server state  

---

## 3. State Structure Example

```ts
interface User {
  id: string;
  email: string;
  name: string;
  role: 'user' | 'admin';
}

interface SchemaChange {
  id: string;
  name: string;
  description: string;
  change_type: 'breaking' | 'non-breaking';
  status: 'open' | 'resolved';
  affected_services: string[];
  created_at: string;
  updated_at: string;
}

interface Comment {
  id: string;
  schema_change_id: string;
  user_id: string;
  content: string;
  created_at: string;
  updated_at: string;
}

interface Notification {
  id: string;
  type: 'breaking_change' | 'comment';
  payload: { schema_change_id: string };
  read: boolean;
  created_at: string;
  updated_at: string;
}

interface State {
  user: User | null;
  schemaChanges: SchemaChange[];
  comments: Record<string, Comment[]>; // keyed by schema_change_id
  notifications: Notification[];
}
