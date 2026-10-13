# Nephrolithiasis Metabolic Agent

Research prototype for evaluating **synthetic** numeric inputs through deterministic agent-style rules. It includes a Python CLI and FastAPI service, two older StoneMind implementations, and a standalone browser demonstration. It does **not** implement a validated 24-hour urine metabolic workup, kidney-stone recurrence risk model, or treatment guideline.

## Browser demonstration

Open `web/index.html` in a modern browser. It works offline without an API, Python runtime, or dependencies. Enter synthetic identifiers and two numeric values, evaluate the demonstration rules, and download the resulting JSON. The browser app does not transmit inputs, contact the server, or persist data. A GitHub Pages deployment workflow publishes the `web/` directory when Pages is enabled in repository settings; a public live URL should not be advertised before it has been verified.

The browser demonstration reproduces the generic rules in `agents/workers.py`, **not** the Python service's HMAC audit trail. It never fabricates a signed audit result.

## Rules and limitations

The main agent stack applies three generic, *unvalidated* conditions:

- `InvariantQCWorker`: flags a primary metric greater than **25**.
- `SafetyEscalationWorker`: flags a secondary metric greater than **12**, or a simulated critical flag.
- `ProtocolConformanceWorker`: flags a status descriptor containing a configured anomaly keyword.

**These quantities have no specified clinical units or analyte definitions.** They are not thresholds endorsed by AUA, EAU, KDIGO, or KDOQI. The `CRITICAL_STAT_PANIC` field is a prototype status code, **not a medical emergency determination**. Do not use outputs for clinical care, prescribing, triage, or patient management.

The `nephrolithiasis_metabolic_agent/` package and `stone_mind.py` are separate legacy implementations with different placeholder thresholds and schemas. They are retained for compatibility, not presented as equivalent or independently validated methods.

## Install and run

Requires Python 3.10–3.12 for the tested CI matrix. The package metadata requires Python 3.9+, although 3.9 is not in that matrix.

```bash
git clone https://github.com/abusuraihsakhri/nephrolithiasis-metabolic-agent.git
cd nephrolithiasis-metabolic-agent
python -m pip install -e '.[dev]'
export AUDIT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
python cli.py audit --task-id DEMO-001 --target SPEC-01 --primary 29.4 --secondary 14.8
python cli.py verify-audit
```

For Windows, set `AUDIT_SECRET_KEY` in the environment using a cryptographically secure randomly generated value with at least 32 characters.

Additional workflows:

```bash
python cli.py chat status
python cli.py batch -i sample.csv -o results.csv
python cli.py serve --host 127.0.0.1 --port 8000
python stone_mind_app.py audit
python nephrolithiasis_metabolic_agent_app.py audit
```

The API runs at `http://127.0.0.1:8000` by default, with OpenAPI docs at `/docs`; `/health`, `/metrics`, `/api/audit`, `/api/chat`, and `/api/audit/logs` are implemented in `agents/api.py`. Only the mock text responder is implemented; alternative model-provider names are rejected instead of silently claiming a real integration.

## Container use

```bash
export AUDIT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
docker compose up --build
```

Docker Compose requires a supplied signing key. Do not commit keys, supply a predictable fallback, or expose this prototype directly to untrusted networks. The service does not implement user authentication or production-grade access control.

## Testing

```bash
python -m pytest -q
python -m compileall -q agents nephrolithiasis_metabolic_agent cli.py stone_mind.py
node --check web/app.js
node --test web/app.test.cjs
```

GitHub Actions runs Python tests on 3.10, 3.11, and 3.12 with an ephemeral signing key, plus Node-based browser-logic tests.

## Security and data handling

The backend holds dossiers and audit records **in memory**; they are not a durable clinical record and are lost on restart. Its audit chain uses HMAC-SHA256 signatures; successful verification checks stored signatures and chain continuity but does not provide independent storage or external timestamping. A pattern-based identifier guard rejects some common personal identifiers, including common MRN, email, phone and SSN formats. **Regex screening cannot guarantee removal of all PHI or establish HIPAA compliance**. Do not submit identifiable patient information.

The standalone browser demonstration processes values locally and does not call the backend. The clinical rules do not need Pyodide; the static demonstration uses plain JavaScript to avoid Python/WASM download overhead. The Python API, authentication requirements, and in-memory audit state cannot be deployed as a functioning server on GitHub Pages.

## Technology and license

Python, Pydantic v2, FastAPI, Uvicorn, pytest; HTML/CSS/JavaScript and Node's built-in test runner for the browser demonstration. Current versions of Chromium, Firefox and Safari are expected to support the browser page; cross-browser manual testing is not included in CI.

Licensed under the [MIT License](LICENSE).
