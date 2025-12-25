# Database Schema

## Users Table
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| email | String | Unique user email |
| password_hash | String | Hashed password |
| created_at | Timestamp | Record creation |
| updated_at | Timestamp | Last update |

## Tasks Table
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| user_id | UUID | Foreign key to users |
| title | String | Task title |
| completed | Boolean | Task completion |
| created_at | Timestamp | Record creation |

[Add diagrams or other tables as needed]
