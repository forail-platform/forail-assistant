# Security Policy

## Supported Versions

The latest released minor version receives security fixes. See [CHANGELOG.md](./CHANGELOG.md) for releases.

| Version | Supported |
|---------|-----------|
| 2026.05.x | Yes |
| < 2026.05 | No  |

## Reporting a Vulnerability

Please report security issues privately to **office@krletron.xyz**.

Do **not** open a public GitHub issue for suspected vulnerabilities.

Include:

- Component affected (assistant API, Ollama integration, ChromaDB indexing)
- Steps to reproduce, or proof-of-concept
- Impact assessment (prompt injection, data leak, model exfiltration, etc.)
- Suggested remediation if you have one

## Disclosure Timeline

- **48 hours** — acknowledgement of report
- **7 days** — initial assessment and severity classification
- **30 days** — fix released or mitigation provided for critical/high severity
- **90 days** — public disclosure after fix is available

We will credit you in the release notes unless you prefer to remain anonymous.

## Scope

In scope:

- forge-assistant (this repository) — FastAPI service, embedded Ollama/ChromaDB orchestration
- Prompt-injection vectors in user-controlled inputs flowing into the LLM
- Auth/authz on assistant endpoints

Out of scope:

- Vulnerabilities in Ollama, ChromaDB, or model weights themselves (please report upstream)
- Issues caused by replacing the bundled model with an untrusted custom model
