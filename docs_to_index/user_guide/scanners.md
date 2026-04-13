# IaC Scanners

Forge integrates static analysis tools to scan Ansible playbooks, infrastructure-as-code, and Python dependencies before job execution. Scanners can warn about issues or block launches that have findings above a severity threshold.

## Supported Tools

| Tool | What It Scans | Finding Types |
|------|---------------|---------------|
| **ansible-lint** | Ansible playbooks and roles | Best practice violations, deprecated syntax, security issues |
| **checkov** | Infrastructure-as-code (Terraform, CloudFormation, Ansible) | Misconfigurations, CIS benchmarks, security checks |
| **pip-audit** | Python dependencies (requirements.txt) | Known CVEs in installed packages |

## Creating a Scanner

1. Navigate to **Compliance > Scanners** and click **Add**.
2. Configure:
   - **Name** — Descriptive name.
   - **Tool** — Select `ansible-lint`, `checkov`, or `pip-audit`.
   - **Severity Threshold** — Findings at or above this level trigger the scanner: `info`, `low`, `medium`, `high`, `critical`.
   - **Enforcement** — `warn` (log only) or `enforce` (block launch on findings above threshold).
   - **Applies To** — Resource types: `job_template`, `workflow_job_template`, `ad_hoc_command`. Empty = all.
   - **Organization** — Scope to an organization, or leave empty for global.

## How Scanning Works

1. User launches a job template.
2. Forge checks all enabled scanners that apply to the resource type.
3. For each scanner, the tool runs against the project files.
4. Output is parsed into **normalized findings** with rule_id, severity, file_path, line, and message.
5. The **aggregate status** is computed:
   - `ok` — No findings.
   - `warn` — Findings exist but all below threshold.
   - `blocked` — At least one finding at or above threshold.
6. Based on enforcement: `warn` logs the result; `enforce` blocks the launch.

## Severity Ordering

From lowest to highest: `info` < `low` < `medium` < `high` < `critical`.

A scanner with threshold `high` will block on `high` and `critical` findings but allow `medium` and below.

## Scan Results

Every scan produces a **Scan Result** viewable at **Compliance > Scan Results**. Each result includes:
- Overall status (ok/warn/blocked/error/timeout)
- Duration in milliseconds
- Finding count and highest severity
- Individual findings with file paths and line numbers

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET/POST | `/api/v2/scanners/` | List or create scanners |
| GET/PUT/DELETE | `/api/v2/scanners/{id}/` | Scanner detail |
| GET | `/api/v2/scan_results/` | List scan results |
| GET | `/api/v2/scan_results/{id}/` | Scan result with findings |
