# Policy-as-Code

Policy-as-Code allows administrators to define guardrails that evaluate before any job, workflow, or ad-hoc command launches. Policies are written in Rego (the Open Policy Agent language) and evaluated against a context that includes the template, user, organization, and extra variables.

## How It Works

1. An administrator writes a Rego policy and registers it in Forail.
2. Forail syncs the policy to the OPA sidecar (`forail-opa` container).
3. When a user launches a job template, Forail sends a query to OPA with the launch context.
4. OPA evaluates all applicable policies and returns allow/warn/deny decisions.
5. Based on the effective enforcement level, Forail either allows the launch, shows a warning, or blocks it.

## Enforcement Levels

Policies have a three-level enforcement model with a global kill switch and per-organization override:

| Level | Behavior |
|-------|----------|
| **none** | Policy is disabled — no evaluation. |
| **warn** | Policy is evaluated; warnings are shown but the launch proceeds. |
| **enforce** | Policy is evaluated; denies block the launch. |

The effective enforcement is: `min(global_setting, org_override, policy.enforcement)`. If the global setting is off, no policies run regardless of per-policy settings.

### Fail-Safe Behavior

If OPA is unreachable:
- **allow mode** (default): Launches proceed — no policy evaluation.
- **deny mode**: Launches are blocked until OPA recovers.

## Writing Rego Policies

Example: Block launches outside business hours:
```rego
package forail.launch

deny["Launches not allowed outside business hours (9-17 UTC)"] {
    hour := time.clock(time.now_ns())[0]
    hour < 9
}

deny["Launches not allowed outside business hours (9-17 UTC)"] {
    hour := time.clock(time.now_ns())[0]
    hour >= 17
}
```

The policy context includes:
- `input.template_name` — Name of the template being launched.
- `input.template_type` — Type: `job_template`, `workflow_job_template`, `ad_hoc_command`.
- `input.user` — Username of the person launching.
- `input.organization` — Organization name.
- `input.extra_vars` — Extra variables provided at launch.

## Policy Decisions

Every policy evaluation is logged as a **Policy Decision** with:
- **Decision**: allow, warn, or deny.
- **Message**: The deny/warn reason from the Rego rule.
- **Context**: The full input that was evaluated.

View decisions at **Compliance > Policy Decisions**.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET/POST | `/api/v2/policies/` | List or create policies |
| GET/PUT/DELETE | `/api/v2/policies/{id}/` | Policy detail |
| POST | `/api/v2/policies/{id}/test/` | Test policy with sample input |
| GET | `/api/v2/policy_decisions/` | List policy decisions |
