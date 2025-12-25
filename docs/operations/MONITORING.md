# Monitoring

## Metrics
- Prometheus for collecting metrics from Go backend
- Grafana for dashboards
- Key metrics: requests per second, latency, error rate

## Logging
- Structured logging with Zap or Logrus
- Send logs to Loki / ELK stack

## Alerts
- High error rate → PagerDuty / Slack notifications
- Slow response time → alert for backend investigation
