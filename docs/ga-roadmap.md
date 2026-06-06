# GA Roadmap

Forge Assistant currently ships as a **preview** (see the status banner in
the [README](../README.md)). This document defines what "preview" means,
what has to be true to drop that label, and the planned path to General
Availability (GA).

## Why it's a preview

The assistant is a young, optional service. The pieces that are still
moving:

- **Models & prompts** — the default model (`gemma3:1b`) is small enough
  to run CPU-only; default prompts and the RAG chunking strategy are
  still being tuned. Output quality varies by hardware and model.
- **API surface** — `/api/v1/chat`, `/api/v1/index`, `/api/v1/health` are
  stable in shape but not yet frozen; fields may be added.
- **Operational story** — backup/restore and index recovery exist (see
  [disaster-recovery.md](disaster-recovery.md)) but have not been
  exercised at scale.

Treat it as **non-critical**: the platform runs identically with the
assistant removed, and the chat button simply disappears when its health
check fails.

## Exit criteria (preview → GA)

GA is declared when **all** of the following hold:

- [ ] **API freeze** — `/api/v1/*` request/response schemas are versioned
      and covered by contract tests; breaking changes require a `/api/v2`.
- [ ] **Pinned, documented models** — a default model with a published
      quality/latency baseline on a reference CPU and GPU profile, and a
      documented support matrix for alternatives.
- [ ] **Index lifecycle** — automated, idempotent re-index; documented and
      tested recovery from index loss/corruption (RRO/RTO targets met,
      see DR doc); schema-version stamp on the ChromaDB collection.
- [ ] **Resource envelope** — published CPU/GPU/RAM requirements and the
      Kubernetes PVC sizing guidance, validated under sustained load.
- [ ] **Observability** — health, latency, and error metrics exported
      (OTel), so operators can alert on the assistant like any other
      Forge component.
- [ ] **Security review** — prompt-injection handling for indexed content,
      and confirmation that no chat content or documents leave the host
      (the privacy guarantee that motivates a self-hosted LLM).
- [ ] **CI gates** — lint + tests + Trivy already gate releases; add an
      end-to-end smoke test (start container → index → chat → assert).

## Milestones

| Stage | Focus | Outcome |
|-------|-------|---------|
| **Preview** (now) | Feedback, model/prompt tuning | Opt-in, non-critical, may change |
| **Beta** | API freeze, metrics, DR tested | Safe to enable in staging; stable API |
| **GA** | All exit criteria met | Supported for production, semver'd API |

Until GA, the assistant tracks the platform **CalVer** release train
(`YYYY.MM.PATCH`) like the other platform components — see
[Versioning policy](../../forge-deploy/docs/00-platform-architecture.md#versioning-policy).
At GA the `/api/v1` contract gains its own stability guarantee
independent of the platform calendar.

## See also

- [disaster-recovery.md](disaster-recovery.md) — ChromaDB index backup, restore, and recovery
- [deployment.md](deployment.md) — install, GPU/CPU, backup/restore
- [architecture.md](architecture.md) — RAG pipeline and data flow
