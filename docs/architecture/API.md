# API Documentation

## Base URL
https://api.changeguard.com

## Auth
- JWT authentication required for all endpoints except `/login` and `/signup`

## Example Endpoints
- `POST /signup` - create a new user
- `POST /login` - authenticate user
- `GET /users/:id` - get user info
- `POST /tasks` - create a task
- `GET /tasks` - list tasks

## Error Codes
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 500: Internal Server Error
