# Smart Recommendations

Forail includes an intelligent recommendations engine that analyzes your platform configuration and suggests improvements across security, compliance, automation, and operational health.

## How It Works

The engine evaluates 12 rules against a context snapshot of your platform. Each rule produces a recommendation with a severity level and actionable guidance.

Recommendations are shown in the **Dashboard** and in **Wizard** flows.

## Available Rules

### Critical Severity
- **default_admin_password** — The admin account still uses the default password. Change it immediately to prevent unauthorized access.

### Warning Severity
- **no_scanners** — You have job templates but no IaC scanners enabled. Enable scanners to catch security issues before deployment.
- **multi_org_no_tenancy** — Multiple organizations exist but tenancy is not enabled. Enable tenancy for quota enforcement and resource isolation.
- **tenant_near_quota** — A tenant is using more than 80% of its quota. Consider raising limits before they hit the cap.

### Info Severity
- **all_policies_warn** — All policies are in warn-only mode. Promote tested policies to enforce mode for real protection.
- **no_observability** — OpenTelemetry is disabled. Enable it for distributed tracing and monitoring.
- **stale_project** — A project has not been synced in 14+ days. Re-sync to pull latest changes.
- **no_schedules** — Job templates exist but no schedules are configured. Add schedules to automate recurring tasks.
- **no_drift** — No drift detections exist. Configure fact gathering jobs to monitor configuration drift.
- **few_surveys** — Less than half of your job templates have surveys. Add surveys to enable self-service usage.
- **no_catalog_items** — No service catalog items are published. Publish items to enable the self-service portal.
- **only_default_team** — Only one team exists. Create additional teams for better RBAC organization.

## Scopes

Recommendations are grouped by scope:
- **dashboard** — General platform health (shown on Dashboard).
- **compliance** — Security and compliance posture.
- **tenancy** — Multi-tenancy configuration.
- **automation** — Automation best practices.
- **self_service** — Self-service portal readiness.
- **access** — Access control organization.

## API Endpoint

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v2/recommendations/` | Get all recommendations for the current state |
| GET | `/api/v2/recommendations/?scope=compliance` | Filter by scope |
