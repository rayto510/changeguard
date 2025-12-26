# Deployment Guide

Complete guide to deploying ChangeGuard to AWS with production-grade infrastructure, monitoring, and disaster recovery.

## Overview

This guide covers deploying ChangeGuard to AWS using:
- **Compute**: EC2 instances with Auto Scaling Groups
- **Database**: RDS PostgreSQL with Multi-AZ failover
- **Cache**: ElastiCache Redis with automatic failover
- **Load Balancing**: Application Load Balancer (ALB) with SSL/TLS
- **Observability**: CloudWatch for metrics, logs, and alarms
- **CI/CD**: GitHub Actions for automated deployments

**Deployment Architecture**:
```
Internet
    ↓
Route 53 (DNS)
    ↓
ALB (443 HTTPS) ← CloudFront (optional CDN)
    ↓ (port 8080)
Backend EC2 (x3) ← Auto Scaling Group
    ↓
PostgreSQL RDS (Multi-AZ)
    ↓
Redis ElastiCache (Multi-AZ)
```

**Timeline to Deploy**: 60-90 minutes (first time)

## Prerequisites

### AWS Account Setup
- AWS account with appropriate IAM permissions
- AWS CLI v2 installed and configured
- Terraform or CloudFormation for IaC (optional but recommended)

### Domain & DNS
- Registered domain (e.g., `changeguard.io`)
- Route 53 hosted zone created
- DNS records ready to point to ALB

### Credentials & Keys
- SSH key pair for EC2 access
- SSL certificate from ACM or Let's Encrypt
- Database master password (32+ chars, stored in Secrets Manager)

## Infrastructure Setup

### 1. VPC Configuration

Create a VPC with public and private subnets:

```bash
# VPC
VPC CIDR: 10.0.0.0/16
Name: changeguard-vpc
DNS Hostnames: Enable
DNS Resolution: Enable

# Internet Gateway
Name: changeguard-igw
Attach to: changeguard-vpc

# Subnets - Public (for ALB)
10.0.1.0/24 (us-east-1a, public)
10.0.2.0/24 (us-east-1b, public)

# Subnets - Private (for Backend, DB, Cache)
10.0.11.0/24 (us-east-1a, private)
10.0.12.0/24 (us-east-1b, private)

# NAT Gateway (in public subnet)
Allocate Elastic IP
Create in: 10.0.1.0/24

# Route Tables - Public
Destination: 0.0.0.0/0 → Target: IGW
Associated Subnets: 10.0.1.0/24, 10.0.2.0/24

# Route Tables - Private
Destination: 0.0.0.0/0 → Target: NAT Gateway
Associated Subnets: 10.0.11.0/24, 10.0.12.0/24
```

### 2. Security Groups

**ALB Security Group** (`sg-alb`):
```
Inbound:
  - HTTP (80) from 0.0.0.0/0 (redirect to HTTPS)
  - HTTPS (443) from 0.0.0.0/0

Outbound:
  - All to Backend SG
```

**Backend Security Group** (`sg-backend`):
```
Inbound:
  - 8080 (HTTP) from ALB SG only
  - 22 (SSH) from Bastion SG only
  - 22 (SSH) from 0.0.0.0/0 (for initial setup, restrict after)

Outbound:
  - 5432 (PostgreSQL) to RDS SG
  - 6379 (Redis) to Redis SG
  - 443 (HTTPS) to 0.0.0.0/0 (for docker pull, updates)
  - 53 (DNS) to 0.0.0.0/0
```

**RDS Security Group** (`sg-rds`):
```
Inbound:
  - 5432 (PostgreSQL) from Backend SG only

Outbound:
  - (None required - inbound only)
```

**Redis Security Group** (`sg-redis`):
```
Inbound:
  - 6379 (Redis) from Backend SG only

Outbound:
  - (None required - inbound only)
```

### 3. RDS PostgreSQL Setup

**Create RDS Instance**:
```bash
aws rds create-db-instance \
  --db-instance-identifier changeguard-prod \
  --db-instance-class db.t3.medium \
  --engine postgres \
  --engine-version 16.1 \
  --master-username app_user \
  --master-user-password <random-32-char-password> \
  --allocated-storage 100 \
  --storage-type gp3 \
  --iops 3000 \
  --storage-encrypted \
  --kms-key-id arn:aws:kms:us-east-1:xxx:key/xxx \
  --db-subnet-group-name changeguard-db-subnet \
  --vpc-security-group-ids sg-rds \
  --multi-az \
  --backup-retention-period 7 \
  --backup-window "03:00-04:00" \
  --preferred-maintenance-window "sun:04:00-sun:05:00" \
  --enable-cloudwatch-logs-exports postgresql \
  --enable-iam-database-authentication \
  --deletion-protection
```

**Database Initialization**:
```bash
# Wait for instance to be available
aws rds wait db-instance-available --db-instance-identifier changeguard-prod

# Get RDS endpoint
RDS_ENDPOINT=$(aws rds describe-db-instances \
  --db-instance-identifier changeguard-prod \
  --query 'DBInstances[0].Endpoint.Address' \
  --output text)

# Connect and initialize
PGPASSWORD=$DB_PASSWORD psql -h $RDS_ENDPOINT -U app_user -d postgres << 'EOF'
CREATE DATABASE changeguard;
\c changeguard
\i /path/to/scripts/init.sql
EOF

# Create read-only user for analytics
PGPASSWORD=$DB_PASSWORD psql -h $RDS_ENDPOINT -U app_user -d changeguard << 'EOF'
CREATE USER analytics WITH PASSWORD 'analytics_password';
GRANT CONNECT ON DATABASE changeguard TO analytics;
GRANT USAGE ON SCHEMA public TO analytics;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO analytics;
EOF
```

### 4. ElastiCache Redis Setup

**Create Redis Cluster**:
```bash
aws elasticache create-cache-cluster \
  --cache-cluster-id changeguard-redis \
  --cache-node-type cache.t3.medium \
  --engine redis \
  --engine-version 7.0 \
  --num-cache-nodes 1 \
  --cache-parameter-group-name changeguard-redis-params \
  --cache-subnet-group-name changeguard-cache-subnet \
  --security-group-ids sg-redis \
  --snapshot-retention-limit 5 \
  --snapshot-window "04:00-05:00" \
  --preferred-maintenance-window "sun:05:00-sun:06:00" \
  --auth-token $(openssl rand -base64 32) \
  --at-rest-encryption-enabled \
  --transit-encryption-enabled

# For multi-AZ (production):
aws elasticache create-replication-group \
  --replication-group-description "ChangeGuard Redis" \
  --engine redis \
  --engine-version 7.0 \
  --cache-node-type cache.r6g.xlarge \
  --replication-group-id changeguard-redis \
  --cache-subnet-group-name changeguard-cache-subnet \
  --security-group-ids sg-redis \
  --automatic-failover-enabled \
  --num-cache-clusters 2 \
  --auth-token $(openssl rand -base64 32)
```

**Verify Redis**:
```bash
aws elasticache describe-cache-clusters \
  --cache-cluster-id changeguard-redis \
  --show-cache-node-info
```

### 5. Application Load Balancer (ALB)

**Create ALB**:
```bash
# Create ALB
ALB_ARN=$(aws elbv2 create-load-balancer \
  --name changeguard-alb \
  --subnets subnet-public-1a subnet-public-1b \
  --security-groups sg-alb \
  --scheme internet-facing \
  --type application \
  --ip-address-type ipv4 \
  --query 'LoadBalancers[0].LoadBalancerArn' \
  --output text)

# Create target group
TG_ARN=$(aws elbv2 create-target-group \
  --name changeguard-backend \
  --protocol HTTP \
  --port 8080 \
  --vpc-id vpc-xxx \
  --health-check-protocol HTTP \
  --health-check-path /health \
  --health-check-interval-seconds 30 \
  --health-check-timeout-seconds 10 \
  --healthy-threshold-count 2 \
  --unhealthy-threshold-count 3 \
  --matcher HttpCode=200 \
  --query 'TargetGroups[0].TargetGroupArn' \
  --output text)

# Create HTTP listener (redirect to HTTPS)
aws elbv2 create-listener \
  --load-balancer-arn $ALB_ARN \
  --protocol HTTP \
  --port 80 \
  --default-actions Type=redirect,RedirectConfig="{Protocol=HTTPS,Port=443,StatusCode=HTTP_301}"

# Create HTTPS listener
aws elbv2 create-listener \
  --load-balancer-arn $ALB_ARN \
  --protocol HTTPS \
  --port 443 \
  --certificates CertificateArn=arn:aws:acm:us-east-1:xxx:certificate/xxx \
  --default-actions Type=forward,TargetGroupArn=$TG_ARN
```

**Enable sticky sessions** (optional):
```bash
aws elbv2 modify-target-group-attributes \
  --target-group-arn $TG_ARN \
  --attributes \
    Key=stickiness.enabled,Value=true \
    Key=stickiness.type,Value=lb_cookie \
    Key=stickiness.lb_cookie.duration_seconds,Value=86400
```

### 6. SSL/TLS Certificate

**Using AWS Certificate Manager (Recommended)**:

```bash
# Request certificate
aws acm request-certificate \
  --domain-name changeguard.io \
  --subject-alternative-names www.changeguard.io api.changeguard.io \
  --validation-method DNS

# Validate DNS (AWS Console or CLI)
# Update Route 53 with validation records

# Verify certificate
aws acm describe-certificate --certificate-arn arn:aws:acm:us-east-1:xxx:certificate/xxx
```

**Using Let's Encrypt (Manual)**:

```bash
# Install certbot
sudo apt-get update && sudo apt-get install -y certbot

# Request certificate
sudo certbot certonly \
  --standalone \
  --email admin@changeguard.io \
  --agree-tos \
  --non-interactive \
  -d changeguard.io \
  -d www.changeguard.io

# Certificate location: /etc/letsencrypt/live/changeguard.io/

# Import to ACM
aws acm import-certificate \
  --certificate fileb:///etc/letsencrypt/live/changeguard.io/cert.pem \
  --certificate-chain fileb:///etc/letsencrypt/live/changeguard.io/chain.pem \
  --private-key fileb:///etc/letsencrypt/live/changeguard.io/privkey.pem

# Auto-renewal (cron job)
0 3 * * * certbot renew --post-hook "aws acm import-certificate ..." >> /var/log/certbot-renewal.log
```

## Compute Setup

### 1. Create AMI

Build a custom AMI with all dependencies:

```bash
# Launch temporary EC2 instance (Ubuntu 22.04 LTS)
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.large \
  --key-name changeguard-key \
  --security-group-ids sg-backend \
  --subnet-id subnet-private-1a

# SSH into instance (via bastion if private)
ssh -i changeguard-key.pem ubuntu@<instance-ip>

# Install Docker and dependencies
sudo apt-get update
sudo apt-get install -y docker.io docker-compose
sudo usermod -aG docker ubuntu

# Install CloudWatch agent
wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
sudo dpkg -i -E ./amazon-cloudwatch-agent.deb

# Install monitoring tools
sudo apt-get install -y awscli htop iotop

# Setup app user
sudo useradd -m -s /bin/bash app

# Create AMI from instance
aws ec2 create-image \
  --instance-id i-xxx \
  --name changeguard-backend-v1 \
  --description "ChangeGuard backend with Docker and monitoring"
```

### 2. Create Launch Template

```bash
aws ec2 create-launch-template \
  --launch-template-name changeguard-backend \
  --launch-template-data '{
    "ImageId": "ami-changeguard-backend-v1",
    "InstanceType": "t3.medium",
    "KeyName": "changeguard-key",
    "SecurityGroupIds": ["sg-backend"],
    "IamInstanceProfile": {
      "Arn": "arn:aws:iam::xxx:instance-profile/ChangeguardBackendRole"
    },
    "UserData": "IyEvYmluL2Jhc2gKc2V0IC1l..."
  }'
```

**UserData script** (base64 encoded):
```bash
#!/bin/bash
set -e

# Pull latest image
docker pull myregistry/changeguard-backend:latest

# Load environment
export $(cat /home/app/.env | xargs)

# Start container
docker run -d \
  --name changeguard-backend \
  --restart unless-stopped \
  -p 8080:8080 \
  -e DB_HOST=$DB_HOST \
  -e DB_PASSWORD=$DB_PASSWORD \
  -e REDIS_URL=$REDIS_URL \
  myregistry/changeguard-backend:latest

# Send signal to ASG that instance is ready
/opt/aws/bin/cfn-signal -e $? --stack changeguard --resource BackendASG
```

### 3. Create Auto Scaling Group

```bash
aws autoscaling create-auto-scaling-group \
  --auto-scaling-group-name changeguard-backend-asg \
  --launch-template LaunchTemplateName=changeguard-backend,Version='$Latest' \
  --min-size 2 \
  --desired-capacity 3 \
  --max-size 6 \
  --vpc-zone-identifier "subnet-private-1a,subnet-private-1b" \
  --target-group-arns $TG_ARN \
  --health-check-type ELB \
  --health-check-grace-period 300 \
  --termination-policies "Default"

# Create scaling policies
# Scale up when CPU > 70%
aws autoscaling put-scaling-policy \
  --auto-scaling-group-name changeguard-backend-asg \
  --policy-name scale-up \
  --policy-type TargetTrackingScaling \
  --target-tracking-configuration "
    TargetValue=70.0,
    PredefinedMetricSpecification={PredefinedMetricType=ASGAverageCPUUtilization}
  "

# Scale down when CPU < 30%
aws autoscaling put-scaling-policy \
  --auto-scaling-group-name changeguard-backend-asg \
  --policy-name scale-down \
  --policy-type TargetTrackingScaling \
  --target-tracking-configuration "
    TargetValue=30.0,
    PredefinedMetricSpecification={PredefinedMetricType=ASGAverageCPUUtilization},
    ScaleInCooldown=300
  "
```

## DNS & Routing

### 1. Route 53 Configuration

```bash
# Create hosted zone (if not exists)
HOSTED_ZONE_ID=$(aws route53 create-hosted-zone \
  --name changeguard.io \
  --caller-reference $(date +%s) \
  --query 'HostedZone.Id' --output text)

# Create A record for ALB
aws route53 change-resource-record-sets \
  --hosted-zone-id $HOSTED_ZONE_ID \
  --change-batch '{
    "Changes": [{
      "Action": "CREATE",
      "ResourceRecordSet": {
        "Name": "changeguard.io",
        "Type": "A",
        "AliasTarget": {
          "HostedZoneId": "Z35SXDOTRQ7X7K",
          "DNSName": "changeguard-alb-xxx.us-east-1.elb.amazonaws.com",
          "EvaluateTargetHealth": true
        }
      }
    }]
  }'

# Create CNAME for www
aws route53 change-resource-record-sets \
  --hosted-zone-id $HOSTED_ZONE_ID \
  --change-batch '{
    "Changes": [{
      "Action": "CREATE",
      "ResourceRecordSet": {
        "Name": "www.changeguard.io",
        "Type": "CNAME",
        "TTL": 300,
        "ResourceRecords": [{"Value": "changeguard.io"}]
      }
    }]
  }'

# Create CNAME for API
aws route53 change-resource-record-sets \
  --hosted-zone-id $HOSTED_ZONE_ID \
  --change-batch '{
    "Changes": [{
      "Action": "CREATE",
      "ResourceRecordSet": {
        "Name": "api.changeguard.io",
        "Type": "CNAME",
        "TTL": 300,
        "ResourceRecords": [{"Value": "changeguard.io"}]
      }
    }]
  }'
```

## Monitoring & Observability

### 1. CloudWatch Logs

**Setup log groups**:
```bash
aws logs create-log-group --log-group-name /changeguard/backend
aws logs create-log-group --log-group-name /changeguard/rds
aws logs create-log-group --log-group-name /changeguard/alb

# Set retention
aws logs put-retention-policy \
  --log-group-name /changeguard/backend \
  --retention-in-days 30
```

### 2. CloudWatch Alarms

```bash
# High error rate
aws cloudwatch put-metric-alarm \
  --alarm-name changeguard-error-rate-high \
  --alarm-description "Alert when error rate > 5%" \
  --metric-name HTTPClientErrors \
  --namespace AWS/ApplicationELB \
  --statistic Sum \
  --period 300 \
  --threshold 50 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2 \
  --alarm-actions arn:aws:sns:us-east-1:xxx:Alerts

# High latency
aws cloudwatch put-metric-alarm \
  --alarm-name changeguard-latency-high \
  --alarm-description "Alert when p99 latency > 500ms" \
  --metric-name TargetResponseTime \
  --namespace AWS/ApplicationELB \
  --statistic Average \
  --period 60 \
  --threshold 0.5 \
  --comparison-operator GreaterThanThreshold \
  --alarm-actions arn:aws:sns:us-east-1:xxx:Alerts

# RDS storage full
aws cloudwatch put-metric-alarm \
  --alarm-name changeguard-rds-storage-low \
  --alarm-description "Alert when disk usage > 80%" \
  --metric-name FreeStorageSpace \
  --namespace AWS/RDS \
  --statistic Average \
  --period 300 \
  --threshold 20 \
  --comparison-operator LessThanThreshold \
  --alarm-actions arn:aws:sns:us-east-1:xxx:Alerts
```

### 3. Dashboard

```bash
aws cloudwatch put-dashboard \
  --dashboard-name changeguard-ops \
  --dashboard-body file://dashboard.json
```

## Deployment Process

### 1. Build & Push Images

```bash
# Build backend
docker build -f Dockerfile.backend -t changeguard-backend:v1.0.0 .
docker tag changeguard-backend:v1.0.0 myregistry/changeguard-backend:v1.0.0
docker tag changeguard-backend:v1.0.0 myregistry/changeguard-backend:latest
docker push myregistry/changeguard-backend:v1.0.0
docker push myregistry/changeguard-backend:latest

# Build frontend
docker build -f Dockerfile.frontend -t changeguard-frontend:v1.0.0 ./frontend
docker tag changeguard-frontend:v1.0.0 myregistry/changeguard-frontend:v1.0.0
docker tag changeguard-frontend:v1.0.0 myregistry/changeguard-frontend:latest
docker push myregistry/changeguard-frontend:v1.0.0
docker push myregistry/changeguard-frontend:latest
```

### 2. Update Launch Template

```bash
aws ec2 create-launch-template-version \
  --launch-template-name changeguard-backend \
  --source-version 1 \
  --launch-template-data '{
    "ImageId": "ami-updated"
  }'
```

### 3. Rolling Update

```bash
# Start instance refresh (rolling update)
aws autoscaling start-instance-refresh \
  --auto-scaling-group-name changeguard-backend-asg \
  --preferences 'MinHealthyPercentage=100,InstanceWarmupSeconds=300'

# Monitor progress
watch 'aws autoscaling describe-instance-refreshes \
  --auto-scaling-group-name changeguard-backend-asg \
  --query "InstanceRefreshes[0]"'

# Wait for completion
aws autoscaling wait instance-refresh-succeeded \
  --auto-scaling-group-name changeguard-backend-asg
```

## Backup & Disaster Recovery

### 1. Database Backups

RDS automatic backups run daily at 03:00 UTC, retained for 7 days. Cross-region copy to us-west-2.

**Restore from snapshot**:
```bash
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier changeguard-restored \
  --db-snapshot-identifier rds:changeguard-prod-20251225-0300

# Wait for ready
aws rds wait db-instance-available --db-instance-identifier changeguard-restored

# Verify data
psql -h changeguard-restored.xxx.rds.amazonaws.com -U app_user -d changeguard -c "SELECT COUNT(*) FROM schema_changes;"
```

### 2. Test Restore Procedure

Monthly (first Monday of month):
```bash
# Create test snapshot
aws rds create-db-snapshot \
  --db-instance-identifier changeguard-prod \
  --db-snapshot-identifier changeguard-test-$(date +%Y%m%d)

# Restore to test environment
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier changeguard-test \
  --db-snapshot-identifier changeguard-test-$(date +%Y%m%d)

# Run verification tests
# ...

# Clean up
aws rds delete-db-instance \
  --db-instance-identifier changeguard-test \
  --skip-final-snapshot
```

## Troubleshooting

### Deployment Failed
```bash
# Check ASG events
aws autoscaling describe-scaling-activities \
  --auto-scaling-group-name changeguard-backend-asg \
  --max-records 5

# Check instance status
aws ec2 describe-instance-status \
  --instance-ids i-xxx \
  --query 'InstanceStatuses[0]'

# View logs
docker logs changeguard-backend
```

### Database Connection Issues
```bash
# Verify security group
aws ec2 describe-security-groups --group-ids sg-backend

# Test connectivity from backend
psql -h $RDS_ENDPOINT -U app_user -d changeguard -c "SELECT 1"

# Check RDS status
aws rds describe-db-instances --db-instance-identifier changeguard-prod \
  --query 'DBInstances[0].[DBInstanceStatus,DBInstanceIdentifier]'
```

### High Error Rate
```bash
# Check backend logs
aws logs tail /changeguard/backend --follow

# Check ALB target health
aws elbv2 describe-target-health --target-group-arn $TG_ARN

# Check database performance
psql -h $RDS_ENDPOINT -U app_user -d changeguard << 'EOF'
SELECT query, calls, mean_time FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;
EOF
```

## Rollback Procedure

If issues detected post-deployment:

```bash
# Option 1: Revert to previous AMI
aws ec2 create-launch-template-version \
  --launch-template-name changeguard-backend \
  --source-version <previous-version> \
  --launch-template-data '{"ImageId": "ami-previous"}'

# Option 2: Scale down new instances
aws autoscaling update-auto-scaling-group \
  --auto-scaling-group-name changeguard-backend-asg \
  --desired-capacity 2

# Option 3: Point DNS to previous environment
aws route53 change-resource-record-sets ...
```

## Security Hardening

### 1. Database User Privileges

```bash
# Application user - minimal privileges
CREATE USER app_user WITH PASSWORD 'xxx';
GRANT CONNECT ON DATABASE changeguard TO app_user;
GRANT USAGE ON SCHEMA public TO app_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO app_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO app_user;

# Analytics user - read-only
CREATE USER analytics WITH PASSWORD 'xxx';
GRANT CONNECT ON DATABASE changeguard TO analytics;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO analytics;
```

### 2. Network ACLs

Backend security group inbound:
- Port 8080 from ALB only
- Port 22 from specific IPs (bastion)

### 3. Encryption Keys

- Database encryption: AWS KMS CMK (Customer Managed Key)
- Backups: Encrypted with same KMS key
- Secrets: AWS Secrets Manager with automatic rotation

## Cost Optimization

### Reserved Instances
```bash
# Purchase 1-year reserved for baseline capacity
# 2x t3.medium backend instances: ~$40/month savings
# 1x db.t3.medium RDS: ~$25/month savings
# 1x cache.t3.medium Redis: ~$15/month savings
# Total monthly savings: ~$80 (40% discount)
```

### Cost Monitoring
```bash
# Daily cost report
aws ce get-cost-and-usage \
  --time-period Start=2025-12-01,End=2025-12-31 \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --group-by Type=DIMENSION,Key=SERVICE
```

## Maintenance

### Weekly Tasks
- Verify backups completed successfully
- Review CloudWatch alarms
- Check disk usage (target: <80%)

### Monthly Tasks
- Test database restore procedure
- Review and optimize slow queries
- Analyze cost trends

### Quarterly Tasks
- Full disaster recovery drill
- Security audit
- Capacity planning review
