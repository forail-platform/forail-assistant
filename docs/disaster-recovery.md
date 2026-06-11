# Disaster Recovery — ChromaDB Index & Models

The assistant keeps **all** persistent state in one place:

| Deployment | Location | Holds |
|------------|----------|-------|
| Docker Compose | volume `assistant_data` mounted at `/data` | ChromaDB vector store + pulled Ollama models |
| Kubernetes (forail-helm) | PVC `forail-assistant-data` (default **20Gi**) at `/data` | same |

Inside `/data`:

- **ChromaDB** — the embedded vector store; collection `forail_docs`
  (configurable via `FORAIL_ASSISTANT_CHROMA_COLLECTION`). This is the
  RAG index built from your documentation.
- **Ollama models** — the pulled LLM (`gemma3:1b` by default) and the
  embedding model (`nomic-embed-text`).

## Key principle: the index is *rebuildable*, not precious

The ChromaDB index is **derived data** — it is generated from your source
documentation by the indexing pipeline. Losing it is a *fast, automatic*
recovery, not a data-loss event:

```bash
# Compose
curl -X POST "http://localhost:8100/api/v1/index?rebuild=true"

# Kubernetes
kubectl -n forail exec deploy/forail-assistant -- \
  curl -sX POST "http://localhost:8100/api/v1/index?rebuild=true"
```

Likewise, **Ollama models re-download automatically** on first start if
they are missing. So the realistic worst case — total loss of `/data` —
recovers by: start the container (models re-pull) → re-index (index
rebuilds). No restore from backup is strictly required.

> This is why the assistant is safe to run with `assistant.enabled=false`
> by default and to add/remove freely: it carries no irreplaceable state.

## Recovery scenarios

| Scenario | Symptom | Recovery |
|----------|---------|----------|
| **Index empty / never built** | Chat answers with no doc context | `POST /api/v1/index` |
| **Index stale** (docs changed) | Answers cite old content | `POST /api/v1/index?rebuild=true` |
| **Index corrupted** | Chat errors, ChromaDB read failures in logs | Delete the Chroma dir under `/data`, restart, then `?rebuild=true` |
| **Models missing** | Health check fails on startup, "model not found" | Just restart — entrypoint re-pulls `gemma3:1b` + `nomic-embed-text` |
| **Total `/data` loss** | Fresh/empty volume | Restart (models re-pull) → `POST /api/v1/index?rebuild=true` |
| **PVC lost (k8s)** | Pod stuck / volume gone | Recreate PVC (helm re-apply), pod re-pulls models, re-index |

## Optional: back up `/data` to skip re-download/re-index

Re-indexing and model re-download are usually faster than a restore, but
for air-gapped hosts (no registry to re-pull models from) or very large
corpora, back up the volume:

```bash
# Compose — backup
docker run --rm -v forail-assistant_assistant_data:/data -v "$(pwd)/backups":/backup \
  alpine tar czf /backup/assistant-data.tar.gz /data

# Compose — restore
docker run --rm -v forail-assistant_assistant_data:/data -v "$(pwd)/backups":/backup \
  alpine tar xzf /backup/assistant-data.tar.gz -C /
```

```bash
# Kubernetes — snapshot the PVC with your CSI VolumeSnapshot class, or copy it out:
kubectl -n forail exec deploy/forail-assistant -- tar czf - /data > assistant-data.tar.gz
```

For air-gapped clusters, back up `/data` **after** the first successful
model pull + index so the restore is fully self-contained.

## Recovery objectives

| | Target | Notes |
|---|--------|-------|
| **RPO** (index) | ~0 | Index is derived from source docs; rebuild reproduces it exactly. |
| **RTO** (index rebuild) | minutes | Scales with corpus size; `?rebuild=true` is idempotent. |
| **RTO** (model re-pull) | ~2 min | Network-dependent; ~1–2 GB for `gemma3:1b` + embeddings. |
| **RTO** (restore from backup) | minutes | Use when re-pull/re-index is impractical (air-gapped, huge corpus). |

## See also

- [deployment.md](deployment.md#backup-and-restore) — backup/restore commands and removal
- [ga-roadmap.md](ga-roadmap.md) — index lifecycle is a GA exit criterion
- [configuration.md](configuration.md) — `FORAIL_ASSISTANT_CHROMA_*` settings
