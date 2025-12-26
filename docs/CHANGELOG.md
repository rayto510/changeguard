# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned for v0.2
- WebSocket support for real-time notifications
- Slack/Teams integration with action buttons
- User mentions in comments (@mention system)
- Status workflow enhancement (Open → In Review → Approved)
- Service impact analysis
- Email notification service
- Audit trail for all changes
- Advanced search and filtering

### Planned for v1.0
- Team management and provisioning
- Advanced RBAC with custom roles
- Multi-step approval workflows
- Integration hub (GitHub, GitLab, Jira)
- Comprehensive analytics dashboard
- Change templates and standardization

---

## [v0.1.0] - 2025-12-25

### Added
- **Backend API**: Complete REST API with 15+ endpoints
  - Schema change CRUD operations
  - Comment threads with nested replies
  - Notification management
  - User and role endpoints
  - Health check and metrics endpoints
- **Frontend Application**: React dashboard with TypeScript
  - Change listing and detail views
  - Create/update schema change forms
  - Comment interface with nested threads
  - User authentication pages
  - Team and notification management
- **Database**: PostgreSQL schema with audit support
  - Schema changes table with version tracking
  - Comments table with parent-child relationships
  - Users table with role-based access
  - Teams and memberships
  - Notifications with read status
  - Audit logs for compliance
- **Cache Layer**: Redis integration
  - User session caching (TTL: 12 hours)
  - Token blacklist for logout
  - Query result caching
  - Rate limit counters
- **Authentication**: JWT-based stateless auth
  - Bcrypt password hashing (cost factor 12)
  - 12-character minimum password requirement
  - Token expiration (12 hours)
  - Refresh token mechanism
  - Account lockout (5 failed attempts → 15 min lockout)
- **Authorization**: Role-based access control
  - Admin: Full system access
  - Owner: Organization-level management
  - Member: Standard user access
  - Guest: Read-only access
- **Infrastructure**:
  - Docker multi-stage builds
  - Docker Compose orchestration
  - PostgreSQL 16 containerized
  - Redis 7 with AOF persistence
  - Backend on port 8080
  - Frontend on port 3000
- **DevOps & Deployment**:
  - AWS-targeted deployment guide (795 lines)
  - VPC, RDS, ElastiCache, ALB configuration
  - SSL/TLS certificate setup
  - Auto-scaling group configuration
  - CloudWatch monitoring and alerting
  - GitHub Actions CI/CD pipeline (719 lines)
  - Test, build, and deploy stages
  - Staging and production environments
  - Blue-green deployment strategy
  - Rollback procedures
- **Operations & Security**:
  - Comprehensive security framework (216 lines)
  - Enterprise monitoring strategy (216 lines)
  - Backup and disaster recovery procedures (328 lines)
  - RTO < 1 hour, RPO < 1 hour
  - Multi-AZ database replication
  - Cross-region backup support
- **Documentation**:
  - Complete API reference (473 lines)
  - Architecture and design patterns
  - Database schema documentation
  - State management patterns
  - Data flow diagrams
  - Product feature specifications
  - User flow documentation
  - UI guidelines and design system
  - Deployment procedures
  - CI/CD pipeline documentation
  - 12 architectural decision records (ADRs)
  - Developer setup guide
  - Comprehensive README (276 lines)

### Security
- JWT tokens with configurable expiration
- Bcrypt password hashing with salt rounds
- SQL injection prevention via parameterized queries
- CORS protection with configurable origins
- Rate limiting on authentication endpoints
- Secure password reset flow with token validation
- Account lockout after failed attempts
- HTTPS/TLS 1.3 enforcement in production
- Secrets manager for credentials (AWS Secrets Manager)
- Encrypted database backups (AES-256)
- Audit logging of all sensitive operations

### Performance
- Redis caching for frequently accessed data
- Database query optimization with indexes
- Connection pooling for database efficiency
- Gzip compression for API responses
- CDN-ready static asset serving
- <200ms p95 API response time target
- Horizontal scaling via container orchestration

### Known Limitations
- Single-region deployment in v0.1
- Real-time updates via polling only (WebSocket in v0.2)
- No service dependency visualization (planned for v0.3)
- Manual approval workflows (automated gates in v1.0)
- Limited third-party integrations (more in v1.1)
- No self-hosted option (planned for v2.0)

---

## Release Schedule

### v0.1 (Current)
- **Beta Start**: 2025-12-20
- **Public Beta**: 2025-12-25
- **Status**: Stable - Accepting feedback
- **Planned End of Beta**: 2026-02-28

### Upcoming
- **v0.2**: 2026-03-31 (Real-time + Collaboration)
- **v0.3**: 2026-06-30 (Analytics + Dashboards)
- **v1.0**: 2026-09-30 (Production Ready)
- **v1.1**: 2026-12-31 (Integrations)
- **v2.0**: 2027-Q2 (Enterprise & Security)
