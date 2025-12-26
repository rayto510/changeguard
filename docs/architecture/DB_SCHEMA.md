# ChangeGuard Database Schema (v1)

This document outlines the database schema for ChangeGuard v1, focusing on tracking breaking schema/API changes.

---

## 1. Users Table

Stores information about registered users.

| Column       | Type         | Constraints           | Description                     |
|-------------|-------------|----------------------|---------------------------------|
| id          | UUID        | PK, not null         | Unique user ID                  |
| email       | VARCHAR     | Unique, not null     | User email                      |
| name        | VARCHAR     | Not null             | User name                       |
| password    | VARCHAR     | Not null             | Hashed password                 |
| role        | VARCHAR     | Default 'user'       | Role of the user (user/admin)  |
| created_at  | TIMESTAMP   | Default now()        | Creation timestamp              |
| updated_at  | TIMESTAMP   | Default now()        | Last update timestamp           |

---

## 2. Schema_Changes Table

Tracks breaking or non-breaking schema/API changes.

| Column             | Type       | Constraints       | Description                                      |
|-------------------|-----------|-----------------|--------------------------------------------------|
| id                | UUID      | PK, not null     | Unique schema change ID                           |
| name              | VARCHAR   | Not null         | Short description of the change                  |
| description       | TEXT      |                  | Detailed explanation of the change               |
| change_type       | VARCHAR   | Not null         | 'breaking' or 'non-breaking'                     |
| status            | VARCHAR   | Default 'open'   | 'open', 'resolved'                               |
| affected_services | JSONB     |                  | List of affected services                         |
| created_at        | TIMESTAMP | Default now()    | When the record was created                      |
| updated_at        | TIMESTAMP | Default now()    | When the record was last updated                 |

---

## 3. Comments Table

Stores discussion on schema changes.

| Column           | Type       | Constraints       | Description                                   |
|-----------------|-----------|-----------------|-----------------------------------------------|
| id              | UUID      | PK, not null     | Unique comment ID                              |
| schema_change_id | UUID      | FK -> schema_changes.id | Linked schema change ID                   |
| user_id         | UUID      | FK -> users.id   | Author of the comment                          |
| content         | TEXT      | Not null         | Comment text                                   |
| created_at      | TIMESTAMP | Default now()    | When the comment was created                   |
| updated_at      | TIMESTAMP | Default now()    | Last update timestamp                           |

---

## 4. Notifications Table

Tracks notifications for users regarding schema changes or comments.

| Column            | Type       | Constraints       | Description                                     |
|------------------|-----------|-----------------|-------------------------------------------------|
| id               | UUID      | PK, not null     | Unique notification ID                           |
| user_id          | UUID      | FK -> users.id   | Recipient of the notification                    |
| type             | VARCHAR   | Not null         | Notification type: 'breaking_change', 'comment'|
| payload          | JSONB     |                  | Extra data (e.g., schema_change_id)             |
| read             | BOOLEAN   | Default false    | Whether the notification has been read          |
| created_at       | TIMESTAMP | Default now()    | When the notification was created               |
| updated_at       | TIMESTAMP | Default now()    | Last update timestamp                            |

---

## 5. Relationships

- **Users → Comments**: One-to-many (a user can author many comments).  
- **Users → Notifications**: One-to-many (a user can have many notifications).  
- **Schema_Changes → Comments**: One-to-many (a schema change can have many comments).  

---

## Notes

- All timestamps use **UTC**.  
- `affected_services` is stored as JSONB for flexibility (can later be normalized if needed).  
- Future extensions could include **versioning for schema changes** or **integration with CI/CD pipelines**.
