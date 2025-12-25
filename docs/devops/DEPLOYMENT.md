# Deployment

## Staging
- Deploy Docker containers to AWS ECS or EC2
- Environment variables from `.env.staging`
- Test new features before production

## Production
- Deploy Docker containers to AWS ECS or Kubernetes
- Environment variables from `.env.production`
- Ensure monitoring & alerting is active

## Rollback
- Keep previous Docker images for rollback
- Use CI/CD pipeline to redeploy previous stable version
