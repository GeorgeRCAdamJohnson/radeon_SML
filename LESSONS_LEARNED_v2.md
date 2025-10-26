## Lessons Learned — v2

This document captures concrete lessons learned from the current work on the Radeon SML knowledge-base, crawler, and reasoning-agent stack and proposes a prioritized plan for a v2 that moves faster and cleaner.

### Preface
- Context: we merged Wikipedia-derived content, repaired short KB entries, added diagnostics, and created runners and repair scripts on branch `repair-kb`.
- Goal for v2: make development/deployments deterministic, fail-fast on missing assets, and enable faster iteration with safe CI gates.

---

### Key lessons

1. Treat data as first-class infra
   - Large generated KB JSON files should not be treated like normal source. They bloat the repo and make builds/deploys fragile when the container doesn't include them.

2. Fail-fast on missing assets
   - Silent fallback to a builtin KB hides issues. Containers and CI must detect missing KB and return non-zero status with diagnostics.

3. Make local scripts runnable from any CWD
   - Runners that rely on ad-hoc sys.path modifications are fragile. Prefer package entrypoints or a short bootstrap that sets PYTHONPATH from repo root.

4. Surface diagnostics automatically
   - Write structured startup diagnostics (file checks, counts, git info) to stdout/artifacts so issues are easy to debug in logs or CI.

5. Add CI smoke-tests for critical paths
   - Unit tests for KB loader and a server health/integration test would have caught many regressions earlier (encoding, JSON shape differences, retrieval issues).

6. Use small, focused PRs with CI gates
   - Large, mixed changes increase review overhead and raise the chance of shipping regressions.

---

### Concrete prioritized plan (v2)

Priority 1 — Critical (blockers / fast wins)

- Add a fail-fast startup entrypoint
  - `entrypoint.sh` or `scripts/check_kb_and_start.py` that verifies `/app/data` contents, writes `data/kb_startup_debug.json`, and exits non-zero if required files are missing.
  - Either: COPY canonical `data/` into image at build time (simple) or download KB from a canonical artifact store at startup (recommended for production).

- Add a dev `docker-compose.override.yml` with `./data:/app/data:rw` so local containers see live KB.

Priority 2 — High (stability)

- Add unit and integration tests
  - `tests/test_kb_loader.py` to validate KB loads and handles dict/list formats and write diagnostics when missing/corrupt.
  - `tests/test_server_health.py` to assert `/api/health` and basic chat smoke-run.
  - Add GitHub Actions to run linters and tests on PRs.

- Normalize script entrypoints
  - Convert `scripts/*` to package entrypoints (`python -m radeon_sml.scripts.run_gundam_queries`) or add a small repo-bootstrap `bin/run` that sets PYTHONPATH.

Priority 3 — Medium (developer velocity)

- Implement a small in-memory index on agent load (title→article + keyword map) to improve retrieval relevance (Gundam-related queries failed to find matching sources).

- Add JSON Schema for KB and a `validate_kb.py` tool used by CI and the crawler to ensure canonical format.

Priority 4 — Long-term (scale & infra)

- Move large generated KB to an artifact store or use Git LFS.
- Create a deploy pipeline that builds the image, runs the KB-check container, then deploys to Cloud Run using a service account (secrets stored in CI secrets manager).

---

### Quick actionable checklist (first sprint)

1. Add `docker/entrypoint.sh` + patch `Dockerfile` to use it (or add build-time COPY for data).
2. Add `docker-compose.override.yml` for dev mounts.
3. Add `tests/test_kb_loader.py` and a minimal GitHub Actions `ci.yml`.
## Lessons Learned — v2

This document captures concrete lessons learned from the current work on the Radeon SML knowledge-base, crawler, and reasoning-agent stack and proposes a prioritized plan for a v2 that moves faster and cleaner.

### Purpose of this update
This revision clarifies the environment model (Dev / Stage / Prod), adds explicit agent engineering guidelines, expands the testing recommendations (API and E2E), and provides a clearer design for an NLP/reasoning agent aligned with the goals you outlined.

> Note: per your instruction, this change updates only documentation. No code or runtime changes were applied.

---

### High-level lessons (recap)

- Data must be treated as first-class infrastructure. Generated KB files must be managed as canonical artifacts, not randomly checked-in large blobs.
- Containers and CI should fail-fast when required assets are missing; silent fallbacks hide issues and make debugging difficult.
- Scripts must be runnable from multiple CWDs or converted to package entrypoints; avoid ad-hoc sys.path fixes.
- Add structured diagnostics that are written to logs and artifacts at startup for quick triage.
- Enforce CI gates and small PRs to reduce sprawl and regressions.

---

### Environment model (Dev / Stage / Prod)

Clear environment responsibilities prevent the confusion we experienced.

- Dev (local builds)
   - Purpose: fastest iteration loop for developers.
   - Typical workflow: run Python directly (virtualenv) or use `docker compose` with `docker-compose.override.yml` that mounts local `./data` and source for hot reload.
   - Expectations: quick startup, debuggable logs, lightweight local data; no real secrets.

- Stage (local Docker deployment)
   - Purpose: smoke-test the containerized stack in a reproducible environment that resembles Prod.
   - Typical workflow: `docker compose -f docker-compose.yml -f docker-compose.stage.yml up --build` and run smoke tests against the services.
   - Expectations: production-like startup sequence (entrypoint checks), health/readiness endpoints, structured logs.

- Prod (GCP Cloud Run)
   - Purpose: production runtime with autoscaling and managed infra.
   - Typical workflow: CI builds the image, runs a pre-deploy KB-check container that validates the presence and shape of KB artifacts, then deploys using a service account.
   - Expectations: fail-fast if KB missing, controlled secrets via Secret Manager, logging to Cloud Logging, and readiness probes.

Implementation note: For Prod, prefer a canonical KB in an artifact store (GCS) and fetch at build time or startup; ensure startup times are bounded (small index in image, lazy fetch of heavy assets if needed).

---

### Agent engineering guidelines (rules to enforce)

These enforceable rules are meant to reduce sprawl and improve long-term maintainability.

1. Document the contract first
    - Every agent function must declare inputs, outputs, and failure modes (2–4 bullets). Example: process_query(query:str, format:str)-> {answer, sources, retrieval_count}

2. Fix canonical paths before adding scripts
    - If something is broken in the main flow (`reasoning_agent.py`, `server.py`, existing retriever), try to fix it there. New scripts may be added only when they are packaged as reusable CLI entrypoints and covered by tests.

3. Tests required for behavior changes
    - Any change to agent logic or retrieval must include unit tests (happy path + at least one edge case). CI must run these tests on PRs.

4. No silent fallbacks
    - Fallbacks to built-in KB are allowed only with explicit detection and logging; Stage and Prod must fail-fast instead of operating silently.

5. Structured logs & metrics
    - Emit retrieval_count, top_k sources (title,score), fallback flags, git commit id, and agent version as structured JSON to stdout.

6. PR size & review discipline
    - Keep PRs focused: < 300 lines ideally; larger changes should be split into multiple PRs.

---

### API & testing strategy (comprehensive)

Tests to implement in the short term:

- Unit tests
   - `tests/test_kb_loader.py` — KB load (list vs dict), malformed JSON, missing-file behavior (should write diagnostics and raise/exit depending on env).
   - `tests/test_indexer.py` — index build, mapping titles/keywords.
   - `tests/test_reasoning_pipeline.py` — given a mocked retriever and a fixed prompt, agent returns expected shape.

- Server tests
   - `tests/test_server_health.py` — use FastAPI TestClient to assert `/api/health` and `/api/ready` and that `/api/health` exposes KB counts when present.
   - `tests/test_api_chat.py` — mock the agent and validate API schema and error modes.

- Integration / Stage E2E tests
   - `tests/e2e_stage.py` (compose-driven) that:
      - builds the image locally, starts compose, waits for readiness, and runs a set of representative queries (Gundam sample) asserting the response includes either a top-k source or a documented fallback reason.

CI pipeline (recommended GH Actions steps on PRs):

1. Checkout, setup Python (pin/interpreter), install dependencies from `requirements.txt` or `pyproject`.
2. Run formatters/lint (black, ruff). Fail on lint errors.
3. Run unit tests (pytest). Fail on failures.
4. Build Docker image and run a KB-check container (entrypoint) to validate KB assets. If this fails, stop the pipeline.
5. Optional: run stage E2E smoke tests (can be gated to manual or main branch due to time).

---

### NLP / Reasoning Agent design (improved architecture)

Goal: deliver a reasoning agent that composes retrieval, planning, and synthesis steps with traceable outputs and better relevance.

Core components:

- Retriever & Index
   - Title → article map, keyword inverted index, and an optional vector index (FAISS / hnswlib) for semantic search.
   - Persist a compact serialized index in-image for fast startup and optionally refresh it from canonical KB.

- Reasoner Controller
   - Short planner stage: decomposes the query into subtasks or decides which tools to call.
   - Chain-of-thought / trace capturing (internal steps logged but can be omitted from final answer for privacy/perf).
   - Final synthesis stage: generate answer with citations to retrieved sources.

- Tooling
   - Basic tools: web_search, code_executor (sandbox), calculator, kb_updater.
   - Tool calls are optional and invoked by the controller with guarded inputs.

- Model choices & hybrid approach
   - For local dev, use a small open-source LLM (Llama2 7B, Mistral 7B, RedPajama 7B) quantized for CPU/GGML if necessary.
   - For production or heavy tasks, either host a larger model on a managed instance or call a hosted LLM via API.
   - Hybrid: use a small local model for planning and a hosted model for the final synthesis.

Agent output contract (required)

- Inputs: { query: str, format: enum, max_sources: int }
- Outputs: {
   answer: str,
   sources: [{title, url, score, excerpt}],
   retrieval_count: int,
   reasoning_trace: [ {step, tool, result} ],
   success: bool,
   error: optional
}

Failure modes and handling

- Missing KB: success=false; diagnostics file written; stage/prod startup fails.
- Empty retrieval: return success=false with suggestion to broaden query or source set; log the event.
- LLM error: retry with backoff (configurable) or queue for manual review if persistent.

---

### Developer and contributor checklist (short)

- Before committing: run formatters and tests locally.
- Small PR: include tests and update `data/kb_schema.json` when data shape changes.
- If adding a script: make it a package entrypoint and add tests.
- If adding large data files: propose an artifact plan (GCS or Git LFS) in the PR description.

---

### Files recommended to add (quick list)

- `docker/entrypoint.sh` or `scripts/check_kb_and_start.py` (fail-fast)
- `docker-compose.override.yml` (dev mounts)
- `data/kb_schema.json` (JSON Schema)
- `data/README.md` (how to regenerate KB and canonical storage)
- `tests/*` (unit + server + e2e)
- `.github/workflows/ci.yml` (CI)
- `AGENT_GUIDELINES.md` (short version of agent engineering rules)

---

### Timeline & next-step recommendation

Immediate (0–2 days)
- Update docs (this file) and add the fail-fast entrypoint + dev compose override (low-risk). Add `data/README.md` describing the KB canonical location.

Short (3–7 days)
- Add unit tests for KB loader and server health. Add CI skeleton (lint + pytest + build + kb-check).

Medium (1–2 weeks)
- Implement index + retrieval improvements and a small reasoning-controller prototype. Add stage E2E smoke tests.

Long (2–4 weeks)
- Move KB to artifact store, finalize Cloud Run deploy pipeline, and test production rollout.

---

Updated: 2025-10-25
