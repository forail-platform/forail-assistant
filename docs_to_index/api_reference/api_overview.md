# Forge API Reference

The Forge REST API is available at `/api/v2/`. All endpoints require authentication (session cookie or Basic Auth with username:password).

## Authentication

- **Session Auth** — Log in via the web UI; the session cookie authenticates API calls.
- **Basic Auth** — Send `Authorization: Basic base64(username:password)` header.
- **OAuth2 Token** — Create a personal access token at `/api/v2/users/{id}/personal_tokens/` and use `Authorization: Bearer <token>`.

## Pagination

List endpoints return paginated responses:
```json
{
  "count": 42,
  "next": "/api/v2/jobs/?page=2",
  "previous": null,
  "results": [...]
}
```

## Common Parameters

- `page` — Page number (default: 1).
- `page_size` — Results per page (default: 25, max: 200).
- `order_by` — Sort field (prefix with `-` for descending).
- `search` — Full-text search across name fields.

## Core Resource Endpoints

| Resource | List/Create | Detail |
|----------|------------|--------|
| Organizations | `/api/v2/organizations/` | `/api/v2/organizations/{id}/` |
| Users | `/api/v2/users/` | `/api/v2/users/{id}/` |
| Teams | `/api/v2/teams/` | `/api/v2/teams/{id}/` |
| Projects | `/api/v2/projects/` | `/api/v2/projects/{id}/` |
| Inventories | `/api/v2/inventories/` | `/api/v2/inventories/{id}/` |
| Hosts | `/api/v2/hosts/` | `/api/v2/hosts/{id}/` |
| Groups | `/api/v2/groups/` | `/api/v2/groups/{id}/` |
| Credentials | `/api/v2/credentials/` | `/api/v2/credentials/{id}/` |
| Credential Types | `/api/v2/credential_types/` | `/api/v2/credential_types/{id}/` |
| Job Templates | `/api/v2/job_templates/` | `/api/v2/job_templates/{id}/` |
| Workflow Job Templates | `/api/v2/workflow_job_templates/` | `/api/v2/workflow_job_templates/{id}/` |
| Jobs | `/api/v2/jobs/` | `/api/v2/jobs/{id}/` |
| Workflow Jobs | `/api/v2/workflow_jobs/` | `/api/v2/workflow_jobs/{id}/` |
| Schedules | `/api/v2/schedules/` | `/api/v2/schedules/{id}/` |
| Notification Templates | `/api/v2/notification_templates/` | `/api/v2/notification_templates/{id}/` |
| Instances | `/api/v2/instances/` | `/api/v2/instances/{id}/` |
| Instance Groups | `/api/v2/instance_groups/` | `/api/v2/instance_groups/{id}/` |
| Execution Environments | `/api/v2/execution_environments/` | `/api/v2/execution_environments/{id}/` |
| Activity Stream | `/api/v2/activity_stream/` | `/api/v2/activity_stream/{id}/` |
| Settings | `/api/v2/settings/` | `/api/v2/settings/{slug}/` |

## Advanced Feature Endpoints

| Feature | Endpoints |
|---------|-----------|
| Event Rules (EDA) | `/api/v2/event_rules/`, `/api/v2/event_logs/`, `/api/v2/outbound_webhooks/` |
| Drift Detection | `/api/v2/drift_detections/`, `/api/v2/drift_alert_rules/`, `/api/v2/drift_alerts/`, `/api/v2/fact_snapshots/` |
| Policy-as-Code | `/api/v2/policies/`, `/api/v2/policy_decisions/` |
| Scanners | `/api/v2/scanners/`, `/api/v2/scan_results/` |
| Service Catalog | `/api/v2/service_catalog_items/`, `/api/v2/service_requests/` |
| Tenancy | `/api/v2/tenants/`, `/api/v2/tenant_quota_events/` |
| WebAuthn | `/api/v2/webauthn/credentials/`, `/api/v2/webauthn/register/`, `/api/v2/webauthn/authenticate/` |
| Audit | `/api/v2/audit_events/` |
| Recommendations | `/api/v2/recommendations/` |
| Health | `/api/v2/ping/` |

## Launching Jobs

To launch a job template:
```
POST /api/v2/job_templates/{id}/launch/
Content-Type: application/json

{
  "extra_vars": {"env": "production"},
  "limit": "web-servers"
}
```

The response includes the job ID. Poll `/api/v2/jobs/{id}/` for status, or read stdout at `/api/v2/jobs/{id}/stdout/?format=txt`.
