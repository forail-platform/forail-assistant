# Setup Wizards

Forail provides guided wizards that walk you through setting up each major feature area. Wizards are multi-step forms with validation, review, and smart defaults.

## Available Wizards

| Wizard | URL | What It Sets Up |
|--------|-----|-----------------|
| **Getting Started** | `/wizards/getting-started` | Organization, Project, Inventory (with SSH credentials), Credential, and a first Job Template. This is the recommended starting point for new installations. |
| **Automation** | `/wizards/automation` | Event rules, outbound webhooks, and schedules for automated workflows. |
| **Self-Service** | `/wizards/self-service` | Service catalog items and approval workflows for end-user self-service. |
| **Tenancy** | `/wizards/tenancy` | Multi-tenant setup: organization, quotas, branding, and isolation. |
| **Compliance** | `/wizards/compliance` | Drift detection rules, policies, and scanners. |
| **Resources** | `/wizards/resources` | Bulk setup of inventories, credentials, and execution environments. |
| **Access** | `/wizards/access` | Teams, users, and role assignments for RBAC. |

## Wizard Flow

Each wizard follows the same pattern:
1. **Step-by-step form** — Fill in fields for each resource.
2. **Review step** — See a summary of everything before committing.
3. **Submit** — All resources are created in one batch.

Wizards are **idempotent** — if a resource already exists (e.g., an organization with the same name), the wizard updates it instead of creating a duplicate.

## Getting Started Wizard Details

The Getting Started Wizard creates everything needed for your first job run:
1. **Organization** — Name and description.
2. **Project** — Git URL, branch, and SCM credential.
3. **Inventory** — Hosts (comma-separated) with SSH user, password, and optional private key.
4. **Credential** — Machine credential with the SSH details from step 3.
5. **Job Template** — Links project, inventory, credential, and a selected playbook.

After completion, the wizard offers to launch the template immediately.
