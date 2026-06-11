# Observability

Forail integrates with OpenTelemetry for distributed tracing, metrics, and health monitoring.

## Architecture

Forail exports telemetry data via the **OTLP protocol** to an OpenTelemetry Collector sidecar (`forail-otel-collector`). The collector can forward data to backends like Tempo (traces), Prometheus (metrics), Loki (logs), or Grafana Cloud.

## Configuration

Observability is controlled via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `OTEL_ENABLED` | `true` | Master switch for telemetry |
| `OTEL_EXPORTER_ENDPOINT` | `http://forail-otel-collector:4317` | OTLP endpoint |
| `OTEL_SERVICE_NAME` | `forail` | Service name in traces |
| `OTEL_TRACES_SAMPLER` | `parentbased_traceidratio` | Sampling strategy |
| `OTEL_TRACES_SAMPLER_ARG` | `0.1` | Sampling rate (0.0 to 1.0) |

## Health Monitoring

The health system aggregates component status:
- **Database** — PostgreSQL connectivity.
- **Redis** — Cache and message broker.
- **OPA** — Policy engine availability.
- **Ollama** — AI assistant availability.

Health data is cached with a configurable TTL (default: 30 seconds). Stale health data triggers a re-check.

## Endpoints

- **Ping**: `GET /api/v2/ping/` — Returns version, active node, instance groups, and cluster health.
- **Observability Dashboard**: Navigate to **Compliance > Observability** in the UI.

## Grafana Dashboard

A pre-built Grafana dashboard is available at `forail-deploy/grafana/dashboards/forail-overview.json`. It includes panels for:
- Job execution rate and duration.
- API request latency (p50, p95, p99).
- Task queue depth per tenant.
- Error rates by endpoint.

## Recommendations

The Forail Recommendations engine checks observability status and suggests enabling OpenTelemetry if it's disabled (`rule_no_observability`).
