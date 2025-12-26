1. API.md (Schema-Breaking Version)
# ChangeGuard API Documentation (v1)

Tracks schema and API changes, alerts relevant teams, and provides discussion threads for breaking changes.

---

## Base URL

- Production: `https://api.changeguard.com/v1`  
- Local: `http://localhost:8080/api/v1`

---

## Authentication

### Login

- **POST /auth/login**  
- **Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}


Response:

{
  "access_token": "JWT_TOKEN",
  "refresh_token": "REFRESH_TOKEN",
  "expires_in": 3600
}

Register

POST /auth/register

Request Body:

{
  "email": "user@example.com",
  "password": "password123",
  "name": "John Doe"
}


Response:

{
  "id": "uuid",
  "email": "user@example.com",
  "name": "John Doe"
}

Schema Changes
Create Schema Change Record

POST /schema-changes

Request Body:

{
  "name": "users.email column removed",
  "description": "The email column was dropped from users table",
  "change_type": "breaking",
  "affected_services": ["auth-service", "notification-service"],
  "timestamp": "2025-12-25T12:00:00Z"
}


Response:

{
  "id": "uuid",
  "name": "users.email column removed",
  "change_type": "breaking",
  "status": "open",
  "created_at": "2025-12-25T12:00:00Z"
}

Update Schema Change

PUT /schema-changes/:id

Request Body:

{
  "status": "resolved",
  "notes": "Updated downstream services to handle missing email column"
}


Response:

200 OK

List Schema Changes

GET /schema-changes

Query Parameters (optional):

status=open|resolved

affected_service=auth-service

Response:

[
  {
    "id": "uuid",
    "name": "users.email column removed",
    "change_type": "breaking",
    "status": "open",
    "created_at": "2025-12-25T12:00:00Z"
  }
]

Delete Schema Change

DELETE /schema-changes/:id

Response:

204 No Content

Comments
Add Comment to Schema Change

POST /schema-changes/:id/comments

Request Body:

{
  "content": "Auth-service needs an update for this change"
}


Response:

{
  "id": "uuid",
  "schema_change_id": "uuid",
  "user_id": "uuid",
  "content": "Auth-service needs an update for this change",
  "created_at": "2025-12-25T12:10:00Z"
}

Get Comments for Schema Change

GET /schema-changes/:id/comments

Response:

[
  {
    "id": "uuid",
    "schema_change_id": "uuid",
    "user_id": "uuid",
    "content": "Auth-service needs an update for this change",
    "created_at": "2025-12-25T12:10:00Z"
  }
]

Notifications
Get Notifications

GET /notifications

Headers: Authorization: Bearer JWT_TOKEN

Response:

[
  {
    "id": "uuid",
    "type": "breaking_change",
    "payload": {"schema_change_id": "uuid"},
    "read": false,
    "created_at": "2025-12-25T12:15:00Z"
  }
]

Mark Notification Read

PUT /notifications/:id/read

Response:

200 OK

Notes

All endpoints require JWT auth except /auth/*.

Standard HTTP codes: 200 OK, 201 Created, 204 No Content, 400 Bad Request, 401 Unauthorized, 404 Not Found, 500 Internal Server Error.

Dates use ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ.