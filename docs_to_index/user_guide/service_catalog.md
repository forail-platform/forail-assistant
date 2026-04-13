# Self-Service Portal & Service Catalog

The Self-Service Portal allows end users to request automation through a curated catalog, without needing to understand the underlying templates, inventories, or credentials. Administrators publish catalog items; users browse, request, and track their requests.

## Concepts

- **Service Catalog Item** — A curated entry wrapping a Job Template or Workflow Job Template. It has a friendly name, icon, category, and optional approval requirement.
- **Service Request** — A user's request to run a catalog item. Follows a state machine: pending_approval → approved → running → successful/failed/canceled.
- **Approval Workflow** — If a catalog item requires approval, the request stays in `pending_approval` until an authorized approver approves or rejects it.

## For Administrators: Publishing Catalog Items

1. Navigate to **Self-Service > Catalog Admin** and click **Add**.
2. Configure:
   - **Name** — User-facing name (e.g., "Deploy Web Application").
   - **Category** — Grouping label (e.g., "Deployment", "Provisioning").
   - **Icon** — A Lucide icon name for visual identification.
   - **Job Template** or **Workflow Job Template** — The underlying automation.
   - **Requires Approval** — If checked, requests must be approved before running.
   - **Approver Team** — Which team can approve. Falls back to organization admins if not set.

## For Users: Requesting Services

1. Navigate to **Self-Service > Service Portal**.
2. Browse available items by category.
3. Click an item and fill in any survey fields.
4. Click **Submit**.
5. If approval is required, your request goes to `pending_approval`. Track it at **My Requests**.
6. If no approval is needed, the job launches immediately.

## Approval Flow

Approvers see pending requests at **Self-Service > Approvals**.

Who can approve:
- Superusers can always approve.
- Members of the configured **Approver Team**.
- If no team is set, **Organization Admins** can approve.

When approving, the underlying job or workflow launches automatically. When rejecting, a reason can be provided.

## Request Statuses

| Status | Meaning |
|--------|---------|
| `pending_approval` | Waiting for approver action |
| `approved` | Approved, about to launch |
| `rejected` | Rejected by approver |
| `running` | Job is executing |
| `successful` | Job completed successfully |
| `failed` | Job failed |
| `canceled` | Job was canceled |

## Workflow Support

Catalog items can wrap workflow job templates. When a workflow item includes surveys on individual workflow nodes, the `node_survey_data` field carries per-node responses.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET/POST | `/api/v2/service_catalog_items/` | List or create catalog items |
| GET/PUT/DELETE | `/api/v2/service_catalog_items/{id}/` | Item detail |
| POST | `/api/v2/service_catalog_items/{id}/submit/` | Submit a request |
| GET | `/api/v2/service_requests/` | List service requests |
| POST | `/api/v2/service_requests/{id}/approve/` | Approve request |
| POST | `/api/v2/service_requests/{id}/reject/` | Reject request |
