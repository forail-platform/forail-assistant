# Event-Driven Automation (EDA)

Event-Driven Automation lets Forge react to external events in real time. Incoming webhooks trigger automated actions — launching job templates, workflows, or sending notifications — based on configurable rules.

## Core Concepts

- **Event Rule** — A rule that listens on a webhook URL, evaluates conditions against the incoming payload, and fires actions when conditions match.
- **Event Log** — An immutable record of every webhook event received, with condition evaluation results and action outcomes.
- **Outbound Webhook** — Sends HTTP POST notifications to external URLs when Forge jobs change state (started, succeeded, failed, canceled).

## Event Rules

### Creating an Event Rule

1. Navigate to **Automation > Event Rules** and click **Add**.
2. Fill in:
   - **Name** — A descriptive name for the rule.
   - **Organization** — The owning organization.
   - **Source Type** — The type of webhook sender: `Generic`, `GitHub`, `GitLab`, `Alertmanager`, `PagerDuty`, `Datadog`, or `CloudWatch`.
   - **Webhook Path** — A unique slug that forms the inbound URL: `POST /api/v2/eda_webhooks/{webhook_path}/`
3. Add **Conditions** — Jinja2 expressions evaluated against `event` (the payload) and `headers`. All conditions must match (AND logic). Examples:
   - `event.action == "push"` — matches GitHub push events.
   - `event.ref == "refs/heads/main"` — only main branch.
   - `event.severity >= 3` — numeric comparison.
   - `"production" in event.labels` — list membership.
4. Add **Actions** — What to do when conditions match:
   - `launch_job_template` — Launch a specific Job Template with optional extra_vars.
   - `launch_workflow` — Launch a Workflow Job Template.
   - `send_notification` — Send a notification via a configured Notification Template.
5. Optional: Set **Throttle (seconds)** to prevent rapid re-firing. Default is 0 (no throttle).

### Signature Verification

Each event rule has a **Webhook Key** used for HMAC signature verification:
- **GitHub**: `X-Hub-Signature-256` header, SHA-256 HMAC.
- **GitLab**: `X-Gitlab-Token` header, direct token comparison.
- **Generic**: `X-Forge-Signature` header, SHA-256 HMAC.
- If the signature does not match, the event is rejected with `signature_failed` status.

### Event Deduplication

Events include a GUID (e.g., `X-GitHub-Delivery` header). If the same GUID is received twice, the duplicate is logged but not re-evaluated.

## Outbound Webhooks

Outbound webhooks push job lifecycle events to external systems (Slack, PagerDuty, CI/CD, custom endpoints).

1. Navigate to **Automation > Outbound Webhooks** and click **Add**.
2. Configure:
   - **URL** — The target endpoint.
   - **Events** — Which job events to send: `job.started`, `job.succeeded`, `job.failed`, `job.canceled`, `workflow.started`, `workflow.succeeded`, `workflow.failed`.
   - **Custom Headers** — Additional headers to include.
   - **SSL Verify** — Whether to verify TLS certificates (default: yes).
3. Each delivery is signed with `X-Forge-Signature` (SHA-256 HMAC) using the webhook key.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET/POST | `/api/v2/event_rules/` | List or create event rules |
| GET/PUT/DELETE | `/api/v2/event_rules/{id}/` | Event rule detail |
| POST | `/api/v2/event_rules/{id}/test/` | Test rule with sample payload |
| GET | `/api/v2/event_logs/` | List event logs |
| GET | `/api/v2/event_logs/{id}/` | Event log detail |
| GET/POST | `/api/v2/outbound_webhooks/` | List or create outbound webhooks |
| POST | `/api/v2/outbound_webhooks/{id}/test/` | Test webhook delivery |
| POST | `/api/v2/eda_webhooks/{path}/` | Inbound webhook receiver |
