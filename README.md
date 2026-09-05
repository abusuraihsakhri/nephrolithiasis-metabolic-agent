# Nephrolithiasis Metabolic Agent

> **Domain:** Computational Biology & AI Drug Discovery
> **Reference Guidelines & Standards:** `wwPDB, IUPAC & CLSI Computational Guidelines`

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)
![Audit Trail](https://img.shields.io/badge/Audit-HMAC--SHA256_Tamper--Evident-brightgreen.svg)
![Zero-PHI Guard](https://img.shields.io/badge/Guard-Zero--PHI_Outbound-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)

</div>

---

## 📖 What It Does

**Nephrolithiasis Metabolic Agent** is an advanced analytical and computational platform implementing 24h Urine Supersaturation & Recurrence Prevention Planner. It provides multi-agent evaluation of clinical metrics with cryptographic audit trails and zero-PHI outbound protection.

---

## ⚙️ Key Capabilities & Algorithmic Modules

### 🔬 Core Algorithmic & Evaluation Engines

- **`Severity`** — dedicated module for severity evaluation and state verification.
- **`DomainKnowledgeRegistry`**: Enterprise domain rules, guideline matrices, and evidence benchmarks.
- **`AgentAlert`** — dedicated module for agent alert evaluation and state verification.
- **`SupersaturationIndexAgent`**: Specialized Sub-Agent 1 for nephrolithiasis-metabolic-agent
- **`DietaryMetabolicEvaluatorAgent`**: Specialized Sub-Agent 2 for nephrolithiasis-metabolic-agent
- **`PharmacologicPreventionAgent`**: Specialized Sub-Agent 3 for nephrolithiasis-metabolic-agent

---

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/abusuraihsakhri/nephrolithiasis-metabolic-agent.git
cd nephrolithiasis-metabolic-agent

# Install dependencies
pip install fastapi uvicorn pydantic pytest
```

---

## 💻 CLI Quickstart & Usage

### 1. Guided Interactive Mode
```bash
python cli.py
```

### 2. Direct Parameterized Evaluation
```bash
python cli.py --task-id <value> --target <value> --primary <value> --secondary <value>
```

### Parameter Reference
- `--task-id`: Specifies input measurement or parameter value.
- `--target`: Specifies input measurement or parameter value.
- `--primary`: Specifies input measurement or parameter value.
- `--secondary`: Specifies input measurement or parameter value.
- `--critical`: Specifies input measurement or parameter value.
- `--status`: Specifies input measurement or parameter value.
- `--input`: Specifies input measurement or parameter value.
- `--output`: Specifies input measurement or parameter value.

### Input Data Schema

| Field | Description | Requirement |
|:------|:------------|:------------|
| `case_id` | Parameter / observation metric | Required |
| `patient_synthetic_id` | Parameter / observation metric | Required |
| `metric_primary` | Parameter / observation metric | Required |
| `metric_secondary` | Parameter / observation metric | Required |
| `is_stat` | Parameter / observation metric | Required |
| `status_flag` | Parameter / observation metric | Required |

---

## 🛡️ Security & Enterprise Architecture

* **Zero-PHI Outbound Interceptor:** Active AST and regex inspection blocking SSNs, MRNs, phone numbers, and patient identifiers.
* **Tamper-Evident HMAC-SHA256 Audit Trail:** Chained, cryptographically signed logs for every evaluation and state transition.
* **Air-Gapped LLM Reasoning Adapter:** Agnostic integration for local Ollama instances (`llama3`, `mistral`), Claude 3.5 Sonnet, GPT-4o, and deterministic test mocks.
* **Active Learning Bayesian Calibration:** Dynamic tracker updating worker reliability weights and monitoring Brier calibration drift.
* **FastAPI & Prometheus Telemetry:** Exposes OpenAPI 3.1 REST endpoints and operational Prometheus metrics (`/metrics`).

### Security Configuration

The audit trail requires a secure secret key. Set the `AUDIT_SECRET_KEY` environment variable:

```bash
# Linux/macOS
export AUDIT_SECRET_KEY="your-secure-random-key-at-least-32-chars"

# Windows
set AUDIT_SECRET_KEY=your-secure-random-key-at-least-32-chars
```

---

## 🧪 Testing & Verification

Run the automated test suite:

```bash
pytest -v
```

Execute high-throughput batch simulation benchmarks:

```bash
python simulator.py --tasks 1000 --concurrency 8
```

---

## 🐳 Container Deployment

```bash
# Build and run with Docker
docker build -t nephrolithiasis-metabolic-agent .
docker run -p 8000:8000 -e AUDIT_SECRET_KEY=your-secure-key nephrolithiasis-metabolic-agent

# Or use docker-compose
AUDIT_SECRET_KEY=your-secure-key docker-compose up
```

---

## 📁 Project Structure

```
nephrolithiasis-metabolic-agent/
├── agents/                          # Core agent modules
│   ├── api.py                       # FastAPI REST server
│   ├── base.py                      # Security, PHI Guard, Audit Trail
│   ├── models.py                    # Pydantic data models
│   ├── supervisor.py                # Supervisor orchestrator
│   ├── workers.py                   # Specialized domain workers
│   ├── llm_factory.py               # LLM provider factory
│   ├── learning.py                  # Bayesian calibration engine
│   ├── metrics.py                   # Prometheus metrics
│   └── streamer.py                  # WebSocket telemetry
├── tests/                           # Test suite
│   ├── test_nephrolithiasis_metabolic_agent.py
│   └── test_enrichment.py
├── nephrolithiasis_metabolic_agent/ # Alternative package implementation
├── cli.py                           # Command-line interface
├── stone_mind.py                    # StoneMind clinical engine
├── enrichment.py                    # Enrichment feature engines
├── simulator.py                     # High-throughput simulator
├── web/index.html                   # Operations console UI
├── Dockerfile                       # Container definition
├── docker-compose.yml               # Container orchestration
└── pyproject.toml                   # Project configuration
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
