# Drift Detection

Drift Detection monitors configuration changes across your infrastructure by comparing Ansible facts between job runs. When a host's configuration changes unexpectedly, Forge detects the drift, categorizes it by severity, and can trigger alerts.

## How It Works

1. When a job runs with `gather_facts: true`, Forge captures a **Fact Snapshot** — the complete set of `ansible_facts` for each host.
2. On the next run, Forge compares the new snapshot against the previous one using the **compute_drift** algorithm.
3. Any differences are recorded as **Drift Detections**, categorized by type and severity.
4. If drift matches a **Drift Alert Rule**, an alert is fired and optionally a notification is sent.

## Drift Categories and Severity

Each changed fact is classified into a category with a default severity:

| Category | Severity | Example Facts |
|----------|----------|---------------|
| kernel | critical | `ansible_kernel`, `ansible_kernel_version`, sysctl settings |
| users_groups | high | `ansible_user_id`, `ansible_user_dir`, user accounts |
| network | high | `ansible_all_ipv4_addresses`, `ansible_default_ipv4`, ports |
| packages | medium | `ansible_packages`, pip packages |
| services | medium | `ansible_services`, systemd units |
| mounts | medium | `ansible_mounts`, filesystem changes |
| other | low | Any unrecognized fact |

Volatile facts (uptime, date_time, etc.) are automatically excluded from drift detection.

## Drift Alert Rules

Alert rules trigger when drift exceeds thresholds within a time window.

To create an alert rule:
1. Navigate to **Compliance > Alert Rules** and click **Add**.
2. Configure:
   - **Name** — Descriptive name.
   - **Inventory** — Optional: limit to a specific inventory.
   - **Host Filter** — Optional: fnmatch pattern (e.g., `web-*`).
   - **Categories** — Which drift categories to monitor (empty = all).
   - **Minimum Severity** — Minimum severity to trigger (default: medium).
   - **Threshold Count** — How many drift items to trigger (default: 1).
   - **Window (minutes)** — Time window for counting drift (default: 60).
   - **Cooldown (minutes)** — Minimum time between alerts (default: 30).
   - **Notification Template** — Optional: send notification when triggered.

## Acknowledging Drift

When a drift detection is expected (e.g., a planned upgrade), you can **acknowledge** it:
- Open the drift detection detail page.
- Click **Acknowledge**. This records who acknowledged it and when.
- Acknowledged drifts are excluded from future alert rule evaluation.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v2/fact_snapshots/` | List fact snapshots |
| GET | `/api/v2/drift_detections/` | List drift detections |
| POST | `/api/v2/drift_detections/{id}/acknowledge/` | Acknowledge drift |
| GET/POST | `/api/v2/drift_alert_rules/` | List or create alert rules |
| GET | `/api/v2/drift_alerts/` | List triggered alerts |
| GET | `/api/v2/hosts/{id}/drift/` | Drift history for a host |
