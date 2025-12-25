# Security

## Authentication
- JWT for API authentication
- OAuth2 optional

## Passwords
- Hash with bcrypt or argon2
- Never store plain text passwords

## HTTPS
- Use TLS for all production endpoints
- Managed by AWS / Cloudflare

## Secrets Management
- Environment variables or AWS Secrets Manager
- Do not commit secrets to Git
