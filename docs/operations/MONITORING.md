# Monitoring

## CloudWatch Metrics

### Application Metrics
- HTTP request count (total, by endpoint, by status code)
- HTTP latency (p50, p95, p99)
- Error rate (4xx, 5xx errors)
- Active connections (database, Redis)
- Cache hit rate (Redis)
- Database query performance

### Infrastructure Metrics
- EC2 CPU utilization (target: <70%)
- EC2 memory usage (target: <80%)
- EC2 disk usage (target: <85%)
- RDS CPU utilization (target: <70%)
- RDS connections (target: <80% of max)
- RDS replica lag (target: <100ms)
- ElastiCache CPU (target: <70%)
- ElastiCache memory (target: <90%)
- Network I/O (bytes in/out)
- ALB target health
- ALB response time

## Logging Strategy

### Backend Logs
```
Format: JSON structured logging
Fields: timestamp, level, service, request_id, user_id, message, duration_ms, error
Destinations: 
  - stdout (Docker logs)
  - CloudWatch Logs
  - S3 (archive after 30 days)
```

### Frontend Logs
```
Format: JavaScript console logs
Fields: timestamp, level, component, message, error_stack
Sent to: CloudWatch via custom endpoint
```

### Database Logs
```
Format: RDS enhanced monitoring
Data:
  - Slow query log (queries > 1s)
  - Connection logs
  - Error logs
Retention: 7 days in RDS, archive to S3
```

## Alerting

### Critical Alerts (Page Oncall)
- Error rate > 5% for 5 minutes
- API latency p99 > 1 second for 10 minutes
- Database replication lag > 5 seconds
- Any service marked unhealthy
- Disk usage > 95%

### Warning Alerts (Slack notification)
- Error rate > 1% for 10 minutes
- API latency p95 > 500ms for 10 minutes
- Cache hit rate < 70%
- Database connections > 70% of max
- Deployment failed
- Certificate expiring in < 30 days

### Alert Channels
- **Critical**: PagerDuty → oncall engineer
- **Warning**: Slack #changeguard-alerts
- **Info**: GitHub Actions logs

## Dashboards

### Operations Dashboard
- Real-time service health status
- Error rate sparkline
- Latency percentiles (p50, p95, p99)
- Request volume by endpoint
- Top errors

### Infrastructure Dashboard
- CPU/memory/disk utilization
- Database connections and query performance
- Redis memory and operations/sec
- Network I/O
- ALB metrics (target health, response time)

### Business Dashboard
- Active users (daily, weekly, monthly)
- Schema changes created (count, by type)
- Teams using platform
- Comments per change (engagement)
- Average time to resolve change

## Health Checks

### Service Health Checks
```
Backend: GET /health
  Response: {"status": "ok", "timestamp": "..."}
  Frequency: Every 30 seconds
  Timeout: 10 seconds
  Failure threshold: 3 consecutive failures

Frontend: GET / (HTTP 200 response)
  Frequency: Every 30 seconds
  Timeout: 5 seconds
  Failure threshold: 3 consecutive failures

Database: pg_isready -U app_user
  Frequency: Every 30 seconds
  Timeout: 5 seconds

Redis: PING command
  Frequency: Every 30 seconds
  Timeout: 5 seconds
```

### Dependency Health
- Can backend connect to database?
- Can backend connect to Redis?
- Can frontend reach backend?
- Is database in replication sync?
- Is Redis replicating correctly?

## Performance Monitoring

### Database Performance
```
Slow Query Log:
  - Queries taking > 1 second
  - Auto-vacuum performance
  - Index usage
  - Table bloat

Query Metrics:
  - Avg execution time by query type
  - Lock wait times
  - Connection pooling efficiency
```

### API Performance
```
Endpoint Metrics:
  - Requests per second
  - Average response time
  - p99 response time
  - Error rate
  - Traffic spike detection

Database Query Performance:
  - Query count per endpoint
  - Slow query detection
  - N+1 query detection
```

### Frontend Performance
```
Web Vitals:
  - Largest Contentful Paint (LCP) - target: < 2.5s
  - First Input Delay (FID) - target: < 100ms
  - Cumulative Layout Shift (CLS) - target: < 0.1
  - Time to First Byte (TTFB) - target: < 600ms

Resource Metrics:
  - Bundle size
  - JavaScript execution time
  - API call duration
  - Cache effectiveness
```

## Retention Policies

| Data | Retention | Location | Archive |
|------|-----------|----------|---------|
| Application Logs | 30 days | CloudWatch | S3 (1 year) |
| Database Logs | 7 days | RDS | S3 (1 year) |
| Metrics | 15 days | CloudWatch | S3 (5 years) |
| Traces | 7 days | X-Ray | None |
| Database Backups | 7 days | RDS | Cross-region (ongoing) |
| Error Tracking | 90 days | Error log DB | Deleted after 90 days |

## Incident Response

### On Alert
1. PagerDuty/Slack notification → Oncall checks alert
2. Assess severity:
   - **Critical** (data loss, security): Immediate action required
   - **High** (user-facing outage): Action within 15 min
   - **Medium** (degraded performance): Action within 1 hour
   - **Low** (warning signs): Action within 1 day

### Investigation
1. Check relevant service logs
2. Review metrics graph at time of incident
3. Check recent deployments or changes
4. Review error stack traces
5. Check database and cache health

### Resolution
1. Identify root cause
2. Apply fix (hotfix, rollback, or scaling)
3. Verify service recovery (health checks pass)
4. Monitor for 30 minutes
5. Document incident

### Post-Incident
1. Postmortem meeting (within 24 hours)
2. Update runbooks
3. Add monitoring/alerting if gaps found
4. Communicate findings to team
