---
name: oss-monitor-operator
description: Run and extend the ClawsTrack workflow to monitor admin-configured GitHub repos with Scrapling, compare them using OpenAI analysis, manage user subscriptions, and trigger notifications.
---

# OSS Monitor Operator

Use this skill when you need to operate or extend the OSS monitor application in this repository.

## Workflow
1. Read environment variables from `.env` (or deployment env).
2. Ensure monitored repositories come from `MONITORED_REPOS`.
3. Run ingestion worker to persist raw snapshots and release snapshots.
4. Use compare API to generate explainable criteria-based scores.
5. Manage user subscriptions and trigger notifications as part of update workflows.

## Important constraints
- Never hardcode repository targets in code paths that should rely on `MONITORED_REPOS`.
- Keep `score + rationale + confidence` in outputs.
- Preserve separation between:
  - raw scraped inputs
  - AI analysis outputs

## Runbook
- Start API: `uvicorn main:app --reload`
- Run ingest once: `python workers/ingest.py`
- Health check: `curl http://127.0.0.1:8000/api/health`
- View snapshots: `curl http://127.0.0.1:8000/api/snapshots`
- Trigger notification: `curl -X POST 'http://127.0.0.1:8000/api/notify/1?message=New+release+detected'`
