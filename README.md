# Backend Kata – FastAPI, PostgreSQL & MongoDB

This project implements a **CQRS-inspired backend** using **FastAPI** with:
- **PostgreSQL** as the write model (source of truth)
- **MongoDB** as the read model (query-optimized)
- **Alembic** for PostgreSQL schema migrations
- **Docker Compose** for local development and execution

---

## Architecture Overview

- **Write Path**
  - All mutations (create/update/delete) go to PostgreSQL
  - Managed via SQLAlchemy ORM + Alembic migrations

- **Read Path**
  - Optimized read models stored in MongoDB
  - Updated synchronously after successful PostgreSQL commits

- **Pattern**
  - CQRS (Command Query Responsibility Segregation)
  - Dual persistence with explicit consistency boundaries

---

## Prerequisites

- Docker & Docker Compose
- No local Python / DB installation required

---

## Getting Started

### 1. Start Services

```bash
docker compose up --build
```

Ensure the following services are running:
- api (FastAPI)
- postgres
- mongo

---

## Database Migrations (PostgreSQL)

All Alembic commands **must be executed inside the api container**.

### Apply latest migrations

### Downgrade all migrations (reset schema)

```bash
docker compose exec api alembic downgrade base
```

```bash
docker compose exec api alembic upgrade head
```

### Create a new migration (autogenerate)

```bash
docker compose exec api alembic revision --autogenerate -m "create users items tags"
```


> ⚠️ Note: Alembic only manages PostgreSQL schema.  
> MongoDB data must be handled separately.

---

## MongoDB Utilities

### Clean MongoDB read models

```bash
docker compose exec api python app/scripts/clean_mongo.py
```

This script removes all read-model collections:
- users_read
- items_read

---

## Seeding Data

### Seed PostgreSQL + MongoDB

```bash
docker compose exec api python app/scripts/seed.py
```

This script:
- Creates users in PostgreSQL
- Creates items and tags in PostgreSQL
- Builds corresponding read models in MongoDB

---

## API Routes Overview

### Users

| Method | Path        | Description              |
|------|-------------|--------------------------|
| GET  | /users      | List all users (Mongo)   |
| POST | /users      | Create user (Postgres → Mongo) |

---

### Items

| Method | Path              | Description |
|------|-------------------|-------------|
| GET  | /items            | List items (Mongo) |
| GET  | /items/{id}       | Get item by id |
| POST | /items            | Create item |
| PUT  | /items/{id}       | Update item |
| DELETE | /items/{id}    | Delete item |

---

## Testing

This project includes both **unit tests** and **integration tests** covering:

- Users routes
- Items routes
- Read model behavior (MongoDB projections)
- Database migrations (Postgres + Alembic)

### Test Types

- **Unit tests**
  - Domain logic
  - Validation rules
  - Error handling
- **Integration tests**
  - FastAPI routes
  - Postgres write model
  - MongoDB read model
  - Cross-database consistency (eventual consistency)

### Coverage

- Branch coverage: **~84%**
- Focus on:
  - Conditional branches
  - Error paths
  - Edge cases in routes

### Running Tests

Make sure Docker containers are running:

```bash
docker exec kata-backend pytest --cov --cov-branch
```

## Notes

Tests are isolated and idempotent

Databases are cleaned between test runs

MongoDB is treated as a derived read model

Alembic migrations are tested separately




## Consistency Model

- PostgreSQL is the **source of truth**
- MongoDB is a **derived read model**
- MongoDB is updated **after successful DB transactions**
- Downgrades or schema resets require **manual Mongo cleanup**

---

## Operational Notes

- Never write directly to MongoDB outside read-model sync
- Always run Alembic migrations before seeding
- For full reset:
  1. `alembic downgrade base`
  2. `clean_mongo.py`
  3. `alembic upgrade head`
  4. `seed.py`

---

## Documentation

- `ADR-004.md` – Storage Choices & Indices
- `EVIDENCE.md` – Query plans, indices, validation
- `README.md` – Project usage (this file)

If operational procedures grow, a **runbook.md** can be added.

---

## Status

✅ Production-ready kata  
✅ Explicit architectural decisions  
✅ Fully reproducible environment  
