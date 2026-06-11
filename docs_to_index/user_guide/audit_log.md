# Audit Log

The Audit Log provides compliance-grade logging of security-sensitive operations. Every credential access, authentication event, and permission change is recorded immutably.

## Audit Event Categories

| Category | What It Tracks |
|----------|----------------|
| **auth** | Login, logout, login failures, MFA challenges, password changes |
| **credential_access** | Credential usage in jobs, credential views, secret decryption |
| **permission_change** | Role grants, role revocations, team membership changes |
| **resource_change** | Creation, modification, deletion of resources |
| **system** | System events, configuration changes, maintenance tasks |

## Audit Event Fields

Each event records:
- **Timestamp** — When the event occurred.
- **Actor** — Who performed the action (username, IP address, User-Agent, session ID).
- **Category** — Classification of the event.
- **Severity** — `info`, `warning`, or `critical`.
- **Action** — Specific action (e.g., `login`, `credential_used`, `role_granted`).
- **Resource** — What was affected (type, ID, name).
- **Detail** — Additional structured data (JSON).
- **Organization** — Scoping for RBAC filtering.
- **Action Node** — Which cluster node processed the event.

## Immutability

Audit events cannot be updated or deleted through the application. They are append-only records designed for compliance requirements.

## SIEM Integration

The `AuditEventSIEMSerializer` provides a flattened format suitable for ingestion into SIEM systems (Splunk, Elastic, etc.):
- Detail fields are flattened with `detail_` prefix.
- A `source` field is set to `forail`.
- An `event_type` field combines category and action.

## Viewing Audit Events

Navigate to **Views > Audit Log** in the UI. You can filter by:
- Category
- Severity
- Date range
- Actor username
- Resource type

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v2/audit_events/` | List audit events (filterable) |
| GET | `/api/v2/audit_events/{id}/` | Audit event detail |

Note: POST/PUT/DELETE are not available — events are created internally by the system.
