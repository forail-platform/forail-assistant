# Multi-Tenancy

Multi-Tenancy provides resource isolation, quota enforcement, and per-tenant branding for organizations sharing a single Forge installation.

## Features

### Resource Isolation (Row-Level Security)

When enabled, PostgreSQL Row-Level Security (RLS) policies ensure that users in one tenant (organization) cannot see or modify resources belonging to another tenant. This operates at the database level for defense in depth.

Isolation modes:
- **Off** — All organizations share visibility (default).
- **Audit only** — Cross-tenant access is logged but not blocked.
- **Strict** — Cross-tenant access is blocked and logged.

The isolation middleware sets a PostgreSQL session variable (`forge.current_tenant_id`) on each request.

### Quota Management

Each tenant can have quotas limiting resource usage:
- **Max Concurrent Jobs** — How many jobs can run simultaneously.
- **Max Daily Launches** — Total launches per day (resets at midnight UTC).
- **Max Hosts** — Maximum hosts in the tenant's inventories.
- **Storage (MB)** — Maximum project storage.

When a quota is exceeded, the operation is blocked and a **Tenant Quota Event** is logged.

### Per-Tenant Rate Limiting

API rate limiting can be configured per tenant using a token bucket algorithm:
- **tenant_api_rate_limit** — Requests per second allowed for the tenant.
- Burst capacity is 2x the rate limit.
- Implemented via Redis Lua script for atomicity.

### Tenant Queue Routing

Each tenant gets a dedicated Celery queue (`tenant-{org_id}`) for job execution. This prevents one tenant's heavy workload from starving another tenant's jobs.

### Branding

Each tenant can have custom branding:
- **Primary Color** — Hex color code (e.g., `#5B47E0`).
- **Logo URL** — Custom logo for the tenant.
- **Login Message** — Custom message on the login page.

## Creating a Tenant

Tenants map to Organizations. To enable tenancy features:
1. Navigate to **Tenancy > Tenants** and click **Add** (or use the Tenancy Wizard at `/wizards/tenancy`).
2. Configure quotas, branding, and isolation settings.
3. The provisioning system creates the organization, admin user, default team, and sets up RLS policies.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET/POST | `/api/v2/tenants/` | List or create tenants |
| GET/PUT/DELETE | `/api/v2/tenants/{id}/` | Tenant detail |
| GET | `/api/v2/tenant_quota_events/` | Quota violation events |

## Provisioning Payload

When creating a tenant via API, provide:
```json
{
  "name": "Acme Corp",
  "admin_username": "acme-admin",
  "admin_email": "admin@acme.example",
  "admin_password": "securepassword",
  "quota": {
    "max_concurrent_jobs": 10,
    "max_daily_launches": 500,
    "max_hosts": 200
  },
  "branding": {
    "primary_color": "#5B47E0"
  }
}
```
