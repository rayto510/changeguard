# CI/CD Pipeline

Complete GitHub Actions-based CI/CD pipeline for automated testing, building, and deployment of ChangeGuard.

## Overview

The CI/CD pipeline automates:
1. **Testing**: Unit tests, integration tests, linting on every push
2. **Building**: Docker image creation and push to registry
3. **Staging**: Automated deployment to staging environment
4. **Production**: Manual approval followed by production deployment

**Pipeline Triggers**:
- Push to `main` → Test, build, deploy to production (with approval)
- Push to `develop` → Test, build, deploy to staging
- Pull requests → Test and lint (no deployment)
- Scheduled daily → Security scan at 2 AM UTC

## GitHub Actions Workflow Files

### `.github/workflows/ci.yml` - Continuous Integration

```yaml
name: CI - Testing & Linting

on:
  push:
    branches:
      - main
      - develop
  pull_request:
    branches:
      - main
      - develop

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_password
          POSTGRES_DB: changeguard_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      redis:
        image: redis:7-alpine
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run linter
        run: |
          pip install flake8
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
          flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

      - name: Run type checker
        run: |
          pip install mypy
          mypy . --ignore-missing-imports

      - name: Run tests
        run: |
          pip install pytest pytest-cov
          pytest -v --cov=. --cov-report=xml
        env:
          DATABASE_URL: postgresql://test_user:test_password@localhost:5432/changeguard_test
          REDIS_URL: redis://localhost:6379/0
          JWT_SECRET: test-secret-key

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
          flags: backend
          name: backend-coverage

      - name: Run security scan
        run: |
          pip install bandit
          bandit -r . -f json -o bandit-report.json || true

      - name: Check for secret leaks
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          head: HEAD

  frontend-tests:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Node
        uses: actions/setup-node@v3
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      - name: Install dependencies
        run: |
          cd frontend
          npm ci

      - name: Run linter
        run: |
          cd frontend
          npm run lint

      - name: Run type check
        run: |
          cd frontend
          npm run type-check

      - name: Run tests
        run: |
          cd frontend
          npm run test:ci
          npm run test:coverage
        env:
          CI: true

      - name: Build for production
        run: |
          cd frontend
          npm run build

      - name: Check bundle size
        run: |
          cd frontend
          size=$(du -sh dist | cut -f1)
          echo "Bundle size: $size"
          if [ "${size%M}" -gt 500 ]; then
            echo "⚠️ Bundle size exceeded 500M limit"
            exit 1
          fi

      - name: Run security audit
        run: |
          cd frontend
          npm audit --production

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./frontend/coverage/coverage-final.json
          flags: frontend
          name: frontend-coverage
```

### `.github/workflows/build.yml` - Docker Build & Push

```yaml
name: Build - Docker Images

on:
  push:
    branches:
      - main
      - develop
    tags:
      - 'v*'

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Log in to Container Registry
        uses: docker/login-action@v2
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata - Backend
        id: meta-backend
        uses: docker/metadata-action@v4
        with:
          images: ${{ env.REGISTRY }}/changeguard/backend
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha

      - name: Build and push Backend
        uses: docker/build-push-action@v4
        with:
          context: .
          file: ./Dockerfile.backend
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta-backend.outputs.tags }}
          labels: ${{ steps.meta-backend.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Extract metadata - Frontend
        id: meta-frontend
        uses: docker/metadata-action@v4
        with:
          images: ${{ env.REGISTRY }}/changeguard/frontend
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha

      - name: Build and push Frontend
        uses: docker/build-push-action@v4
        with:
          context: ./frontend
          file: ./Dockerfile.frontend
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta-frontend.outputs.tags }}
          labels: ${{ steps.meta-frontend.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### `.github/workflows/deploy-staging.yml` - Staging Deployment

```yaml
name: Deploy - Staging

on:
  push:
    branches:
      - develop

jobs:
  deploy:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'

    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Run database migrations
        run: |
          export DATABASE_URL=${{ secrets.STAGING_DATABASE_URL }}
          migrate -path scripts/migrations -database $DATABASE_URL up

      - name: Update ECS service - Backend
        run: |
          aws ecs update-service \
            --cluster changeguard-staging \
            --service backend-service \
            --force-new-deployment \
            --region us-east-1

      - name: Update ECS service - Frontend
        run: |
          aws ecs update-service \
            --cluster changeguard-staging \
            --service frontend-service \
            --force-new-deployment \
            --region us-east-1

      - name: Wait for deployment
        run: |
          aws ecs wait services-stable \
            --cluster changeguard-staging \
            --services backend-service frontend-service \
            --region us-east-1

      - name: Run smoke tests
        run: |
          sleep 30
          curl -f https://staging-api.changeguard.io/health || exit 1
          curl -f https://staging.changeguard.io/ || exit 1

      - name: Notify Slack
        if: success()
        uses: slackapi/slack-github-action@v1
        with:
          webhook-url: ${{ secrets.SLACK_WEBHOOK_STAGING }}
          payload: |
            {
              "text": "✅ Staging deployment successful",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*Staging Deployment Successful*\nBranch: develop\nCommit: ${{ github.sha }}\n<${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}|View Details>"
                  }
                }
              ]
            }

      - name: Notify Slack on failure
        if: failure()
        uses: slackapi/slack-github-action@v1
        with:
          webhook-url: ${{ secrets.SLACK_WEBHOOK_STAGING }}
          payload: |
            {
              "text": "❌ Staging deployment failed",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*Staging Deployment Failed*\nBranch: develop\nCommit: ${{ github.sha }}\n<${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}|View Details>"
                  }
                }
              ]
            }
```

### `.github/workflows/deploy-production.yml` - Production Deployment

```yaml
name: Deploy - Production

on:
  push:
    branches:
      - main
    tags:
      - 'v*'

jobs:
  approval:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - run: echo "Production deployment approved"

  deploy:
    needs: approval
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Create deployment
        id: deployment
        run: |
          DEPLOYMENT_ID=$(aws ecs create-service \
            --cluster changeguard-prod \
            --service-name backend-service-green \
            --task-definition backend:$(aws ecs describe-services \
              --cluster changeguard-prod \
              --services backend-service \
              --query 'services[0].taskDefinition' \
              --output text | cut -d: -f3 | xargs -I {} expr {} + 1) \
            --desired-count 3 \
            --query 'service.serviceArn' \
            --output text)
          echo "deployment_id=$DEPLOYMENT_ID" >> $GITHUB_OUTPUT

      - name: Wait for service stability
        run: |
          aws ecs wait services-stable \
            --cluster changeguard-prod \
            --services backend-service-green \
            --region us-east-1

      - name: Run smoke tests
        run: |
          sleep 60
          curl -f https://api.changeguard.io/health || exit 1
          curl -f https://changeguard.io/ || exit 1

      - name: Health check monitoring (5 minutes)
        run: |
          for i in {1..30}; do
            ERROR_RATE=$(aws cloudwatch get-metric-statistics \
              --metric-name HTTPClientErrors \
              --namespace AWS/ApplicationELB \
              --start-time $(date -u -d '1 minutes ago' +%Y-%m-%dT%H:%M:%S) \
              --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
              --period 60 \
              --statistics Sum \
              --query 'Datapoints[0].Sum' \
              --output text)
            
            if [ "$ERROR_RATE" -gt 50 ]; then
              echo "High error rate detected: $ERROR_RATE"
              # Trigger rollback
              exit 1
            fi
            sleep 10
          done

      - name: Switch traffic (Blue-Green)
        run: |
          aws elbv2 modify-target-group \
            --target-group-arn arn:aws:elasticloadbalancing:us-east-1:xxx:targetgroup/changeguard-prod/xxx \
            --targets Id=green-instance-1 Id=green-instance-2 Id=green-instance-3

      - name: Monitor for 10 minutes post-deployment
        run: |
          for i in {1..60}; do
            HEALTH=$(aws elbv2 describe-target-health \
              --target-group-arn arn:aws:elasticloadbalancing:us-east-1:xxx:targetgroup/changeguard-prod/xxx \
              --query 'TargetHealthDescriptions[*].[Target.Id,TargetHealth.State]' \
              --output text)
            
            if echo "$HEALTH" | grep -q "unhealthy"; then
              echo "Unhealthy targets detected: $HEALTH"
              exit 1
            fi
            sleep 10
          done

      - name: Tag release
        run: |
          git tag v$(date +%Y.%m.%d.%H%M%S)
          git push origin --tags

      - name: Create GitHub Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
          body: |
            Production deployment completed successfully.
            Commit: ${{ github.sha }}
            Deployment ID: ${{ steps.deployment.outputs.deployment_id }}

      - name: Notify Slack
        uses: slackapi/slack-github-action@v1
        with:
          webhook-url: ${{ secrets.SLACK_WEBHOOK_PROD }}
          payload: |
            {
              "text": "✅ Production deployment successful",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*Production Deployment Successful*\nVersion: ${{ github.ref }}\nCommit: ${{ github.sha }}\n<${{ github.server_url }}/${{ github.repository }}/releases/tag/${{ github.ref }}|View Release>"
                  }
                }
              ]
            }

  rollback-on-failure:
    runs-on: ubuntu-latest
    if: failure()
    steps:
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Rollback to previous version
        run: |
          aws ecs update-service \
            --cluster changeguard-prod \
            --service backend-service \
            --task-definition backend:$(expr $(aws ecs describe-services \
              --cluster changeguard-prod \
              --services backend-service \
              --query 'services[0].taskDefinition' \
              --output text | cut -d: -f3) - 1) \
            --force-new-deployment

      - name: Notify Slack of rollback
        uses: slackapi/slack-github-action@v1
        with:
          webhook-url: ${{ secrets.SLACK_WEBHOOK_PROD }}
          payload: |
            {
              "text": "🚨 Production deployment failed and rolled back",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*Production Deployment Rollback*\nVersion: ${{ github.ref }}\n<${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}|View Details>"
                  }
                }
              ]
            }
```

### `.github/workflows/security.yml` - Security Scanning

```yaml
name: Security - Scans

on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM UTC
  push:
    branches:
      - main
      - develop

jobs:
  dependency-check:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Run dependency check
        run: |
          go list -json -m all | nancy sleuth

      - name: Run npm audit
        run: |
          cd frontend
          npm audit --production

  sast:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Run Trivy container scan
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'config'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload Trivy results to GitHub
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'

  container-scan:
    runs-on: ubuntu-latest
    needs: [build]

    steps:
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'ghcr.io/changeguard/backend:latest'
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
```

## GitHub Secrets Configuration

Create these secrets in GitHub repository settings:

```
AWS_ACCESS_KEY_ID          - AWS IAM access key
AWS_SECRET_ACCESS_KEY      - AWS IAM secret key
DOCKER_REGISTRY_URL        - ghcr.io or your registry
STAGING_DATABASE_URL       - PostgreSQL connection string (staging)
PRODUCTION_DATABASE_URL    - PostgreSQL connection string (prod)
SLACK_WEBHOOK_STAGING      - Slack webhook for staging alerts
SLACK_WEBHOOK_PROD         - Slack webhook for production alerts
```

## Branch Strategy

### Main Branch
- Protected branch
- Requires:
  - 2 approving reviews
  - All CI checks passing
  - Up-to-date with develop
  - Branch must be squashed and merged
- Auto-deploys to production (with environment approval)
- Tagged with semantic versioning (v1.2.3)

### Develop Branch
- Integration branch
- Requires:
  - 1 approving review
  - CI checks passing
- Auto-deploys to staging
- Pre-release snapshot (v1.2.3-rc1)

### Feature Branches
- Naming: `feature/short-description`
- Create from: `develop`
- Merge back to: `develop` (via PR)
- Delete after merge: Yes

### Hotfix Branches
- Naming: `hotfix/issue-description`
- Create from: `main`
- Merge to both: `main` and `develop`
- Tagged and released immediately

## Deployment Flow

```
Code Push
  ↓
CI Tests (lint, test, security scan)
  ├─ If PR → Stop (results show in PR)
  └─ If main/develop → Continue
  ↓
Build Docker Images
  ├─ Backend image tagged with commit SHA
  ├─ Frontend image tagged with commit SHA
  └─ Both tagged as 'latest'
  ↓
Push to Registry
  └─ ghcr.io/changeguard/backend:{sha}
  └─ ghcr.io/changeguard/frontend:{sha}
  ↓
[develop branch] → Auto-deploy to Staging
  ├─ Run migrations
  ├─ Update ECS task definitions
  ├─ Deploy services
  ├─ Run smoke tests
  └─ Notify Slack
  ↓
[main branch] → Wait for Production Approval
  ├─ Manual approval in GitHub environment
  ├─ Run migrations (if any)
  ├─ Deploy with canary/blue-green
  ├─ Health check monitoring
  ├─ Switch traffic
  ├─ Monitor for 10 minutes
  ├─ Create GitHub Release
  └─ Notify Slack
```

## Rollback Procedures

### Staging Rollback
```bash
# Automatic on test failure
# Manual via AWS Console or:
aws ecs update-service \
  --cluster changeguard-staging \
  --service backend-service \
  --task-definition backend:<previous-revision>
```

### Production Rollback
```bash
# Automatic on smoke test failure
# Manual:
aws ecs update-service \
  --cluster changeguard-prod \
  --service backend-service \
  --task-definition backend:<previous-revision> \
  --force-new-deployment
```

## Monitoring Pipeline Health

### Success Metrics
- Build success rate: >95%
- Average test time: <10 minutes
- Average deployment time: <20 minutes (staging), <30 minutes (prod)
- MTTR (Mean Time to Rollback): <5 minutes

### Failed Deployment Response
1. Alert team via Slack
2. Automatic rollback initiated
3. Investigation in Slack thread
4. Postmortem created
5. Prevention measures implemented
