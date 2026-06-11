# Getting Started with Forail

Forail is an infrastructure automation platform based on Ansible. It provides a web UI and REST API for managing Ansible playbooks, inventories, credentials, and job execution.

## Key Concepts

- **Job Template** — Defines what to run: a project, playbook, inventory, and credentials. Launch it to create a Job.
- **Job** — A single execution of a Job Template. Shows real-time output and results.
- **Inventory** — A collection of hosts and groups that playbooks run against.
- **Credential** — Encrypted secrets (SSH keys, passwords, cloud tokens) used by jobs.
- **Project** — A Git repository containing Ansible playbooks.
- **Schedule** — An iCal recurrence rule that launches a template automatically.
- **Workflow** — A DAG (directed acyclic graph) of job templates with success/failure/always branches.
- **Organization** — Top-level container for RBAC. Everything belongs to one.
- **Team** — A group of users within an organization with shared permissions.
- **Execution Environment** — A container image with Ansible and dependencies used to run jobs in isolation.

## Creating Your First Job

1. **Add a Project** — Go to Projects > Add, enter your Git repository URL.
2. **Add an Inventory** — Go to Inventories > Add, then add hosts or configure a cloud source.
3. **Add a Credential** — Go to Credentials > Add, select the type (Machine for SSH), enter the key/password.
4. **Create a Job Template** — Go to Templates > Add Job Template. Select the project, playbook, inventory, and credential.
5. **Launch** — Click the Launch button on your template. Watch the output in real-time.

You can also use the **Getting Started Wizard** at `/wizards/getting-started` which walks you through all five steps in a guided flow.

## RBAC (Role-Based Access Control)

Forail uses organizations, teams, and roles to control who can do what:
- **Admin** — Full control over the resource.
- **Execute** — Can launch templates and read results.
- **Read** — Can view the resource but not modify or launch.
- **Use** — Can use the resource as part of another resource (e.g., use a credential in a template).

## Navigation

The left sidebar organizes the UI into sections:
- **Views** — Dashboard, Jobs, Schedules, Activity Stream, Audit Log, Analytics
- **Automation** — Event Rules, Event Logs, Outbound Webhooks (EDA)
- **Self-Service** — Service Portal, My Requests, Approvals, Catalog Admin
- **Tenancy** — Tenants, Quota Events
- **Compliance** — Drift, Policies, Scanners, Observability
- **Resources** — Templates, Inventories, Hosts, Projects, Credentials
- **Access** — Organizations, Users, Teams
- **Admin** — Instances, Instance Groups, Execution Environments, Notifications, Topology, Settings
