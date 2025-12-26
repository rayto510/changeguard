# Backup & Recovery

## Overview

ChangeGuard maintains multiple backup strategies for different data types to ensure business continuity and disaster recovery.

## Database Backups

### PostgreSQL RDS Backups

#### Automated Backups
- **Frequency**: Daily at 03:00 UTC
- **Retention**: 7 days
- **Location**: AWS-managed, multi-AZ
- **Type**: Full snapshot with incremental backup
- **Size**: ~500MB per backup (dev), ~5GB per backup (prod)

#### Configuration
```bash
# Backup window (maintenance window)
Backup Retention Period: 7 days
Backup Window: 03:00-04:00 UTC
Multi-AZ: Enabled (automatic failover)
Copy Snapshots to Region: us-west-2 (disaster recovery)
```

#### Restore Procedure

**Restore to New Instance**:
```bash
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier changeguard-restored \
  --db-snapshot-identifier rds:changeguard-prod-20251225-0300 \
  --db-instance-class db.r6i.xlarge \
  --vpc-security-group-ids sg-12345 \
  --no-publicly-accessible
```

**Restore to Point-in-Time**:
```bash
aws rds restore-db-instance-to-point-in-time \
  --source-db-instance-identifier changeguard-prod \
  --target-db-instance-identifier changeguard-restored \
  --restore-time 2025-12-25T14:30:00Z
```

**Verification After Restore**:
```bash
# Connect to restored instance
psql -h changeguard-restored.xxx.rds.amazonaws.com -U app_user -d changeguard

# Verify table counts
SELECT schemaname, COUNT(*) FROM pg_tables GROUP BY schemaname;

# Check data integrity
SELECT COUNT(*) FROM schema_changes;
SELECT COUNT(*) FROM comments;
SELECT COUNT(*) FROM users;
```

### Schema Migrations

#### Version Control
- All migrations stored in `scripts/migrations/`
- Naming: `{timestamp}_{description}.sql`
- Example: `20251225_create_schema_changes_table.sql`

#### Direction
- **Up**: Applied during deployment
- **Down**: Rollback capability (not used in production)

#### Deployment Procedure
```bash
# Test migration on staging
migrate -path scripts/migrations \
  -database "postgresql://user:pass@staging-db:5432/changeguard" up

# Verify schema matches production
pg_dump -s > schema_after.sql

# Run on production (with approval)
migrate -path scripts/migrations \
  -database "postgresql://user:pass@prod-db:5432/changeguard" up
```

## Redis Backups

### Persistence Configuration
```
Appendonly: yes (AOF enabled)
Appendfsync: everysec (trade-off between durability and performance)
Save: 900 15   # Save if 15 changes in 900 seconds
      300 10   # Save if 10 changes in 300 seconds
      60 10000 # Save if 10000 changes in 60 seconds
```

### ElastiCache Redis Backups
- **Type**: Automatic snapshots
- **Frequency**: Daily
- **Retention**: 5 days
- **Location**: S3-backed
- **Export**: Weekly export to S3 for long-term archive

#### Manual Backup
```bash
aws elasticache create-snapshot \
  --cache-cluster-id changeguard-redis \
  --snapshot-name changeguard-redis-20251225-backup
```

#### Restore from Backup
```bash
# Create new cluster from snapshot
aws elasticache create-cache-cluster \
  --cache-cluster-id changeguard-redis-restored \
  --snapshot-name changeguard-redis-20251225-backup \
  --cache-node-type cache.r6g.xlarge
```

### Cache Invalidation Strategy
After restore, refresh cache:
```bash
# Clear all Redis keys
redis-cli FLUSHALL

# Let application repopulate cache on demand
# Or pre-warm cache:
curl -s http://backend:8080/api/v1/schema-changes?limit=1000
```

## Application Code & Configuration

### Git Repository Backups
- Primary: GitHub (industry-standard backup)
- Secondary: GitLab mirror for redundancy
- All commits auto-backed up
- Releases tagged and archived

### Configuration Backups
```bash
# Backup .env file (never to Git)
aws secretsmanager create-secret \
  --name changeguard/env \
  --secret-string file://.env

# Backup AWS resources (CloudFormation/Terraform)
aws cloudformation describe-stacks > infrastructure-backup.json
```

### Docker Images
- Stored in ECR (Elastic Container Registry)
- All images tagged with version and `latest`
- Images retention: 30 days minimum
- Export to backup registry: Weekly

```bash
# Export image for offline backup
docker save changeguard-backend:latest -o changeguard-backend-latest.tar.gz
aws s3 cp changeguard-backend-latest.tar.gz s3://changeguard-backups/images/
```

## Disaster Recovery

### Recovery Time Objective (RTO): 1 hour
### Recovery Point Objective (RPO): 1 hour

### Scenario: Database Corruption

**Steps**:
1. **Detect** (~5 min): Monitoring alerts data inconsistency
2. **Assess** (~5 min): Determine scope of corruption
3. **Stop Write** (~2 min): Redirect traffic to read-only mode
4. **Restore** (~30 min): Restore from latest clean snapshot
5. **Verify** (~5 min): Data integrity checks pass
6. **Resume** (~2 min): Traffic back to normal
7. **Investigate** (post-incident): Root cause analysis

**Restore from Snapshot**:
```bash
# 1. Create new RDS instance from snapshot
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier changeguard-prod-restored \
  --db-snapshot-identifier rds:changeguard-prod-20251225-0300

# 2. Wait for instance to be ready
aws rds wait db-instance-available \
  --db-instance-identifier changeguard-prod-restored

# 3. Update backend connection string
aws ec2-instances modify-attribute \
  --environment-variables "DB_HOST=changeguard-prod-restored.xxx.rds.amazonaws.com"

# 4. Restart backend services
docker-compose restart backend

# 5. Monitor error logs
docker-compose logs -f backend
```

### Scenario: EC2 Instance Failure

**Steps**:
1. **Detect** (~30 sec): Health check fails
2. **Failover** (~3 min): ASG launches replacement instance
3. **Initialize** (~2 min): New instance pulls image, starts container
4. **Health Check** (~1 min): New instance passes health checks
5. **Total Downtime**: 0 min (ALB routes to healthy instances)

**Manual Recovery** (if ASG fails):
```bash
# 1. Launch new instance from AMI
aws ec2 run-instances \
  --image-id ami-changeguard-backend \
  --instance-type t3.large \
  --subnet-id subnet-private

# 2. Tag for identification
aws ec2 create-tags \
  --resources i-newinstance123 \
  --tags Key=Name,Value=backend-recovered

# 3. Register with ALB target group
aws elbv2 register-targets \
  --target-group-arn arn:aws:elasticloadbalancing:... \
  --targets Id=i-newinstance123
```

### Scenario: Complete Data Center Failure

**Steps**:
1. **Failover Database**: RDS multi-AZ → secondary AZ (~30 sec)
2. **Failover Cache**: ElastiCache multi-AZ → secondary AZ (~30 sec)
3. **Failover Compute**: Scale up healthy AZ instances
4. **Verify**: Health checks pass
5. **Notify**: Alert team of failover

**Cross-Region Disaster**:
```bash
# Restore database from backup in different region
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier changeguard-dr \
  --db-snapshot-identifier arn:aws:rds:us-east-1:xxx:snapshot:rds:changeguard-prod \
  --region us-west-2

# Deploy application in us-west-2
docker-compose -f docker-compose.prod.yml up -d
```

## Testing & Validation

### Backup Verification Schedule
- **Weekly**: Verify latest snapshot exists
- **Monthly**: Test restore to staging environment
- **Quarterly**: Full disaster recovery drill

### Monthly Restore Test
```bash
# Create test environment
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier changeguard-test \
  --db-snapshot-identifier <latest-snapshot>

# Run data integrity checks
psql -d changeguard_test << 'EOF'
  SELECT COUNT(*) as user_count FROM users;
  SELECT COUNT(*) as changes_count FROM schema_changes;
  SELECT COUNT(*) as comment_count FROM comments;
  
  -- Verify foreign keys work
  SELECT COUNT(*) FROM schema_changes WHERE owner_id NOT IN (SELECT id FROM users);
  
  -- Verify no orphaned records
  SELECT COUNT(*) FROM comments WHERE schema_change_id NOT IN (SELECT id FROM schema_changes);
EOF

# Clean up
aws rds delete-db-instance \
  --db-instance-identifier changeguard-test \
  --skip-final-snapshot
```

### Quarterly Disaster Recovery Drill
1. Simulate database failure
2. Initiate failover procedure
3. Verify data consistency
4. Document time to recovery
5. Identify improvements
6. Update runbooks

## Backup Retention & Compliance

| Data Type | Retention | Location | Archive Policy |
|-----------|-----------|----------|-----------------|
| RDS Snapshots | 7 days | AWS RDS | Auto-copy to us-west-2 |
| Redis Snapshots | 5 days | ElastiCache | Daily export to S3 |
| S3 Export Archives | 1 year | S3 (changeguard-backups) | Glacier after 90 days |
| Application Logs | 30 days | CloudWatch | S3 archive, then delete |
| Database Logs | 7 days | RDS | S3 archive, then delete |
| Git Repository | Indefinite | GitHub + GitLab | Automatic via platform |
| Configuration Backups | Indefinite | AWS Secrets Manager | Versioned |

## Backup Monitoring

### Backup Health Dashboard
- Last successful backup timestamp
- Backup size trend
- Restore test results
- RTO/RPO targets met

### Alerts
- Backup failed: Alert within 1 hour
- Backup size anomaly: Investigate size changes >50%
- Restore test failed: Investigate immediately
- Retention policy violation: Alert daily

## Runbooks

### Runbook: Restore Database from Snapshot
See "Scenario: Database Corruption" section above

### Runbook: Failover to Replica
Automated by RDS multi-AZ, documented in AWS console

### Runbook: Restore from Point-in-Time
See "Restore to Point-in-Time" section above

### Runbook: Cross-Region Disaster Recovery
See "Cross-Region Disaster" section above
