# ChangeGuard API Documentation (v1)

Complete REST API reference for schema and API change tracking, team collaboration, and notifications.

## Base URL

- **Production**: `https://api.changeguard.io/api/v1`
- **Staging**: `https://staging-api.changeguard.io/api/v1`
- **Local Development**: `http://localhost:8080/api/v1`

## Overview

ChangeGuard API provides endpoints for:
- User authentication and authorization
- Schema change tracking and management
- Team collaboration through comments
- Real-time notifications
- Change analytics and reporting

## Authentication

### JWT Token Flow

All endpoints (except `/auth/*`) require JWT token in the `Authorization` header:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Token claims:
```json
{
  "sub": "user-id-uuid",
  "email": "user@example.com",
  "permissions": ["create_changes", "comment", "admin"],
  "iat": 1703123456,
  "exp": 1703209856
}
```

### POST /auth/login

Authenticate user with email and password.

**Request**:
```json
{
  "email": "engineer@company.com",
  "password": "securepassword123"
}
```

**Response** (200 OK):
```json
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "engineer@company.com",
    "name": "Alice Engineer",
    "permissions": ["create_changes", "comment"]
  },
  "expiresIn": 86400
}
```

**Errors**:
- `400`: Missing email or password
- `401`: Invalid credentials
- `500`: Server error

### POST /auth/register

Create new user account.

**Request**:
```json
{
  "email": "newuser@company.com",
  "password": "securepassword123",
  "name": "Bob Developer",
  "company": "ACME Inc"
}
```

**Response** (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "email": "newuser@company.com",
  "name": "Bob Developer",
  "company": "ACME Inc",
  "createdAt": "2025-12-25T14:30:00Z"
}
```

**Errors**:
- `400`: Invalid email or weak password
- `409`: Email already registered
- `422`: Validation failed

### POST /auth/logout

Invalidate current JWT token.

**Request**: (no body)

**Response** (200 OK):
```json
{
  "message": "Logged out successfully"
}
```

## Schema Changes

### POST /schema-changes

Create a new schema change record.

**Request**:
```json
{
  "service_name": "user-service",
  "change_type": "breaking",
  "title": "Remove deprecated email_notifications field",
  "description": "The email_notifications boolean field is deprecated. Use notification_channels array instead.",
  "affected_teams": ["backend-team", "integration-team"],
  "deployment_date": "2025-12-27T10:00:00Z",
  "metadata": {
    "database": "users",
    "table": "user_preferences",
    "columns_affected": ["email_notifications"]
  }
}
```

**Response** (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440010",
  "service_name": "user-service",
  "change_type": "breaking",
  "title": "Remove deprecated email_notifications field",
  "description": "...",
  "status": "DRAFT",
  "owner_id": "550e8400-e29b-41d4-a716-446655440000",
  "affected_teams": ["backend-team", "integration-team"],
  "deployment_date": "2025-12-27T10:00:00Z",
  "created_at": "2025-12-25T14:30:00Z",
  "updated_at": "2025-12-25T14:30:00Z",
  "comment_count": 0
}
```

**Errors**:
- `400`: Validation failed (missing required fields)
- `401`: Unauthorized
- `422`: Invalid change_type or status

### GET /schema-changes

List schema changes with optional filtering.

**Query Parameters**:
```
?service=user-service           # Filter by service name
&changeType=breaking            # Filter by change_type (breaking|non-breaking|deprecation)
&status=OPEN                    # Filter by status (DRAFT|OPEN|IN_PROGRESS|RESOLVED|ARCHIVED)
&team=backend-team              # Filter by affected team
&dateFrom=2025-12-01T00:00:00Z  # Start date (ISO 8601)
&dateTo=2025-12-31T23:59:59Z    # End date (ISO 8601)
&page=1                         # Pagination (default: 1)
&limit=20                       # Results per page (default: 20, max: 100)
&sort=created_at                # Sort by field (created_at|updated_at|deployment_date)
&order=desc                     # Sort order (asc|desc, default: desc)
```

**Response** (200 OK):
```json
{
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440010",
      "service_name": "user-service",
      "change_type": "breaking",
      "title": "Remove deprecated email_notifications field",
      "status": "OPEN",
      "owner": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "Alice Engineer"
      },
      "affected_teams": ["backend-team", "integration-team"],
      "deployment_date": "2025-12-27T10:00:00Z",
      "created_at": "2025-12-25T14:30:00Z",
      "updated_at": "2025-12-25T14:30:00Z",
      "comment_count": 3
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 47,
    "pages": 3
  }
}
```

### GET /schema-changes/:id

Get detailed information about a specific change.

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440010",
  "service_name": "user-service",
  "change_type": "breaking",
  "title": "Remove deprecated email_notifications field",
  "description": "The email_notifications boolean field is deprecated. Use notification_channels array instead.",
  "status": "OPEN",
  "owner": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Alice Engineer",
    "email": "alice@company.com"
  },
  "affected_teams": ["backend-team", "integration-team"],
  "deployment_date": "2025-12-27T10:00:00Z",
  "metadata": {
    "database": "users",
    "table": "user_preferences",
    "columns_affected": ["email_notifications"]
  },
  "created_at": "2025-12-25T14:30:00Z",
  "updated_at": "2025-12-25T15:45:00Z",
  "comments": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440020",
      "author": "Bob Developer",
      "text": "Need to coordinate with mobile team for this change",
      "created_at": "2025-12-25T14:45:00Z"
    }
  ],
  "notifications_sent": 5
}
```

**Errors**:
- `404`: Change not found
- `401`: Unauthorized

### PUT /schema-changes/:id

Update a schema change record.

**Request**:
```json
{
  "status": "IN_PROGRESS",
  "title": "Remove deprecated email_notifications field (updated)",
  "deployment_date": "2025-12-28T10:00:00Z"
}
```

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440010",
  "status": "IN_PROGRESS",
  "title": "Remove deprecated email_notifications field (updated)",
  "deployment_date": "2025-12-28T10:00:00Z",
  "updated_at": "2025-12-25T16:00:00Z"
}
```

**Errors**:
- `403`: Forbidden (only owner or admin can update)
- `404`: Change not found
- `409`: Invalid state transition

### DELETE /schema-changes/:id

Delete a schema change record (soft delete).

**Response** (204 No Content)

**Errors**:
- `403`: Forbidden (only owner or admin can delete)
- `404`: Change not found

## Comments & Discussion

### POST /schema-changes/:id/comments

Add a comment to a schema change.

**Request**:
```json
{
  "text": "We need to verify this with the mobile team before deployment"
}
```

**Response** (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440020",
  "schema_change_id": "550e8400-e29b-41d4-a716-446655440010",
  "author": {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "name": "Bob Developer"
  },
  "text": "We need to verify this with the mobile team before deployment",
  "created_at": "2025-12-25T15:00:00Z",
  "updated_at": "2025-12-25T15:00:00Z"
}
```

### GET /schema-changes/:id/comments

Get all comments for a schema change.

**Response** (200 OK):
```json
{
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440020",
      "author": {
        "id": "550e8400-e29b-41d4-a716-446655440001",
        "name": "Bob Developer"
      },
      "text": "We need to verify this with the mobile team before deployment",
      "created_at": "2025-12-25T15:00:00Z"
    }
  ],
  "total": 1
}
```

### PUT /schema-changes/:id/comments/:comment_id

Update a comment (only own comments or admin).

**Request**:
```json
{
  "text": "Updated comment text"
}
```

**Response** (200 OK)

### DELETE /schema-changes/:id/comments/:comment_id

Delete a comment.

**Response** (204 No Content)

## Notifications

### GET /notifications

Get user's notifications.

**Query Parameters**:
```
?read=false        # Filter unread only
&limit=20
&offset=0
```

**Response** (200 OK):
```json
{
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440030",
      "type": "change_created",
      "title": "New schema change in user-service",
      "message": "Remove deprecated email_notifications field",
      "related_change_id": "550e8400-e29b-41d4-a716-446655440010",
      "read": false,
      "created_at": "2025-12-25T14:30:00Z"
    }
  ],
  "unread_count": 5
}
```

### PUT /notifications/:id/read

Mark notification as read.

**Response** (200 OK)

### PUT /notifications/read-all

Mark all notifications as read.

**Response** (200 OK)

## Error Responses

All endpoints return error responses in this format:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      {
        "field": "title",
        "message": "Title is required"
      }
    ]
  }
}
```

**Common HTTP Status Codes**:
- `200`: Success
- `201`: Created
- `204`: No Content (success with no body)
- `400`: Bad Request (validation error)
- `401`: Unauthorized (missing or invalid token)
- `403`: Forbidden (insufficient permissions)
- `404`: Not Found
- `409`: Conflict (invalid state transition)
- `422`: Unprocessable Entity (business logic violation)
- `429`: Too Many Requests (rate limited)
- `500`: Internal Server Error

## Rate Limiting

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1703210000
```

Limits:
- Public endpoints: 100 requests/hour
- Authenticated endpoints: 1000 requests/hour
- Admin endpoints: 10000 requests/hour

## Pagination

List endpoints support cursor-based and offset-based pagination:

```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 147,
    "pages": 8,
    "cursor": "550e8400-e29b-41d4-a716-446655440010"
  }
}
```

## Webhooks (Future v1.1)

Subscribe to events:
- `change.created`
- `change.updated`
- `change.resolved`
- `comment.added`

Configure at: `/settings/webhooks`
