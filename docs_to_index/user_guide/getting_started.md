# Getting Started with Forge

Forge is an infrastructure automation platform based on Ansible. It provides a web UI and REST API for managing Ansible playbooks, inventories, credentials, and job execution.

## Key Concepts

- **Job Template** — Defines what to run: a project, playbook, inventory, and credentials. Launch it to create a Job.
- **Job** — A single execution of a Job Template. Shows real-time output and results.
- **Inventory** — A collection of hosts and groups that playbooks run against.
- **Credential** — Encrypted secrets (SSH keys, passwords, cloud tokens) used by jobs.
- **Project** — A Git repository containing Ansible playbooks.
- **Schedule** — An iCal recurrence rule that launches a template automatically.
- **Workflow** — A DAG (directed acyclic graph) of job templates with success/failure/always branches.

## Creating Your First Job

1. **Add a Project** — Go to Projects > Add, enter your Git repository URL.
2. **Add an Inventory** — Go to Inventories > Add, then add hosts or configure a cloud source.
3. **Add a Credential** — Go to Credentials > Add, select the type (Machine for SSH), enter the key/password.
4. **Create a Job Template** — Go to Templates > Add Job Template. Select the project, playbook, inventory, and credential.
5. **Launch** — Click the Launch button on your template. Watch the output in real-time.

## RBAC (Role-Based Access Control)

Forge uses organizations, teams, and roles to control who can do what:
- **Organization** — Top-level container. Everything belongs to one.
- **Team** — A group of users within an organization.
- **Roles** — Admin, Execute, Read, Use — assigned per resource.
