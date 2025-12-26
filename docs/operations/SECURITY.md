# Security

## Overview

ChangeGuard follows security best practices across authentication, authorization, data protection, and infrastructure.

## Authentication

### User Registration & Login
- Email + password authentication
- Passwords hashed with bcrypt (cost factor: 12)
- Minimum password requirements: 12 characters, upper/lower/digit/special
- Failed login throttling: 5 attempts → 15 minute lockout
- Session timeout: 24 hours of inactivity

### JWT Tokens
- Signed with HS256 algorithm
- Secret key: 32+ character random string
- Expiration: 24 hours
- Refresh mechanism: User can extend session
- Token revocation: Immediately on logout

### OAuth2 (Future)
- Support for GitHub, Google, Okta for SSO
- PKCE flow for client applications
- OpenID Connect compliant

## Authorization

### Role-Based Access Control (RBAC)
```
Admin:
  - All permissions
  - User management
  - System configuration

Team Lead:
  - Create schema changes
  - Manage team members
  - View team analytics

Engineer:
  - Create schema changes
  - Comment on changes
  - View affected changes
  - Mark notifications read

Viewer:
  - Read-only access to changes
  - Comment on changes
  - View notifications
```

### Permission Scopes
- `schema_changes:create` - Create new changes
- `schema_changes:read` - View changes
- `schema_changes:update` - Update changes
- `schema_changes:delete` - Delete changes
- `comments:write` - Add comments
- `notifications:manage` - Manage notifications
- `teams:manage` - Manage team membership
- `users:manage` - Manage users (admin only)

### Change Ownership
- Only owner or admin can update/delete change
- Team leads can manage their team's changes
- Comments are owned by author
- Deletion is soft-delete (data preserved for audit)

## Data Protection

### Encryption At Rest
- Database: PostgreSQL with encrypted tablespaces (AES-256)
- Redis: Redis encryption at rest enabled
- Backups: Encrypted with KMS master key
- Secrets: AWS Secrets Manager with automatic rotation

### Encryption In Transit
- TLS 1.3 for all connections
- HTTPS/WSS only (HTTP redirects to HTTPS)
- Certificate: Let's Encrypt (auto-renewed)
- HSTS enabled (1 year)
- Certificate pinning: Optional for critical clients

### Secrets Management
- Never commit secrets to Git
- Use `.env` file locally (in `.gitignore`)
- Production secrets in AWS Secrets Manager
- Environment-based configuration
- Secrets auto-rotated every 90 days

### Sensitive Data Handling
- Passwords: Hashed, never logged
- API tokens: Masked in logs, rotate every 90 days
- PII (emails, names): Encrypted in database if required
- Audit trail: Immutable log of all data access

## API Security

### Rate Limiting
- Public endpoints: 100 requests/hour per IP
- Authenticated endpoints: 1000 requests/hour per user
- Burst protection: 50 requests/minute
- Rate limit headers: `X-RateLimit-*`

### Input Validation
- All input sanitized and validated
- SQL injection prevention: Parameterized queries
- XSS prevention: HTML escaping on output
- CSRF protection: Token-based CSRF defense
- File upload: Whitelist MIME types, scan for malware

### CORS & CSRF
- CORS: Only allow trusted origins
- CSRF: Token required for state-changing requests
- SameSite cookies: Strict mode

## Infrastructure Security

### Network Security
```
Security Groups:
  - ALB: Allow 80, 443 from internet
  - Backend: Allow 8080 only from ALB
  - Database: Allow 5432 only from backend
  - Redis: Allow 6379 only from backend
  - No SSH directly accessible from internet
  - SSH via Bastion host only
```

### Database Security
- No public IP for RDS
- VPC endpoint for private access
- Database user: app_user (no admin password in application)
- Connection: SSL required
- Backup encryption: KMS master key
- Multi-AZ: Automatic failover

### Secrets & Keys
- AWS KMS for key management
- Automatic key rotation every 2 years
- Different key per environment
- Secrets Manager for credentials
- Never store secrets in Docker images
- Secrets Scanner: Pre-commit hooks

## Compliance

### Data Retention
- User data: Deleted 90 days after account deletion
- Change records: Retained per customer policy (default 7 years)
- Logs: 30 days CloudWatch, 1 year S3 archive
- Backups: 7 days RDS + cross-region copy

### Audit Logging
- All API calls logged: User, timestamp, action, resource
- Authentication events logged: Login, logout, failed attempts
- Authorization failures logged: Permission denied events
- Data changes logged: What changed, by whom, when
- Log retention: Immutable for 7 years

### Privacy
- GDPR compliant data handling
- User right to deletion (soft delete)
- Data portability: Export user data
- Privacy policy accessible
- Data processing agreements for customers

## Incident Response

### Security Incident Procedures
1. **Detect**: Monitoring alerts security team
2. **Contain**: Isolate affected systems
3. **Investigate**: Determine scope and impact
4. **Eradicate**: Fix root cause
5. **Recover**: Restore normal operations
6. **Post-Incident**: Review and improve

### Breach Notification
- Notify affected users within 72 hours
- Notify regulators if required
- Publish incident report
- Update security measures

## Security Scanning

### Automated Scanning
- SAST (Static Analysis): gosec (Go), ESLint (JS)
- Dependency scanning: `npm audit`, `nancy` (Go)
- Container scanning: Trivy on Docker images
- Infrastructure scanning: CloudFormation policy checking
- Secret detection: Pre-commit hooks

### Penetration Testing
- Annual external penetration test
- Monthly internal security review
- Bug bounty program
- Security advisories: HackerOne

## Security Checklist

- [ ] Secrets not committed to Git
- [ ] HTTPS/TLS enabled in production
- [ ] Database passwords complex (12+ chars)
- [ ] Backups tested monthly
- [ ] Access logs reviewed weekly
- [ ] Dependencies updated monthly
- [ ] Security patches applied immediately
- [ ] Rate limiting configured
- [ ] Input validation on all endpoints
- [ ] Output encoding to prevent XSS
- [ ] CORS configured for trusted origins
- [ ] Security headers set (CSP, X-Frame-Options, etc.)
- [ ] Audit logging enabled
- [ ] MFA enabled for production access
- [ ] Incident response plan documented
