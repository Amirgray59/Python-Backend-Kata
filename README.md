# Python Backend Kata – FastAPI (Stage 3)

A contract-first FastAPI service built incrementally through staged PRs.
This repository demonstrates **clean architecture, HTTP correctness, Problem Details errors,
structured logging, and production-ready service baselines**.

---

## Project Goals

- Practice **contract-first API development**
- Apply **Clean Code & Architecture** principles
- Build a **predictable, debuggable FastAPI service**
- Demonstrate **production-readiness** (health, readiness, logs, tests, Docker)

---

## Stages Overview

### Stage 1 — Clean Code & Architecture
- Refactor kata (Gilded Rose)
- Clean modules, naming, tests
- 80%+ branch coverage
- ADR-001, RUNBOOK, CLEAN-CODE-NOTES

### Stage 2 — API Contract (No Service Code)
- OpenAPI 3.1 (`openapi.yaml`)
- Error catalog (`errors.md`)
- Postman collection
- ADR-002 HTTP Semantics & Error Model

### Stage 3 — FastAPI Service Baseline (Current)
- FastAPI implementation of Stage-2 contract
- Problem Details error responses
- Health & readiness endpoints
- Structured logs
- Integration tests
- Docker & docker-compose
- ADR-003 Observability & Config

---

## Tech Stack

- Python 3.11
- FastAPI
- Pydantic v2
- Pytest
- Structlog
- Docker / Docker Compose

---

## Project Structure

```
.
├── Dockerfile
├── README.md
├── app
│   ├── api
│   │   ├── deps.py
│   │   └── routes.py
│   ├── domain
│   │   ├── errors.py
│   │   └── models.py
│   ├── main.py
│   └── utils
│       └── logging.py
├── docker-compose.yaml
├── docs
│   └── adr
│       └── ADR-003.md
├── kata
│   └── gilded_rose
│       ├── after
│       └── before
├── requirements.txt
└── tests
    ├── conftest.py
    ├── integration
    │   ├── test_health.py
    │   ├── test_items_error.py
    │   └── test_items_positive.py
    └── unit
        └── test_error.py

```
---

## Running Locally

### 1. Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the service

```bash
uvicorn app.main:app --reload
```

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- Health: `/health`
- Readiness: `/ready`

---

## Running Tests

```bash
pytest --cov=app --cov-branch
```

Coverage target: (After merging stage-1) * 
- **≥ 85% branch coverage**
---

## Docker

### Build image

```bash
docker build -t python-backend-kata .
```

### Run with Docker Compose

```bash
docker compose up --build
```

---

## Error Handling

All errors follow **RFC 7807 – Problem Details**:

```json
{
  "type": "https://example.com/problems/item-not-found",
  "title": "Item not found",
  "status": 404,
  "detail": "Item with id 'xyz' was not found"
}
```

---

## Logging

- Structured logs (JSON)
- Includes request / correlation IDs
- Ready for ELK, Loki, or Cloud logging systems

---

## How to Work With This Repo

- Each stage = **separate PR**
- PR includes:
  - Evidence snippets
  - CI results
  - Coverage report
  - ADR updates

---

## Author

Built as a **portfolio-grade backend kata** to demonstrate
professional backend engineering practices with FastAPI.
