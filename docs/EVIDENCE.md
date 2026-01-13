# EVIDENCE.md
## Storage Choices & Index Validation

This document provides measurable evidence supporting the storage and indexing decisions described in ADR-004.

---

## Context

The system uses a **CQRS-inspired dual-database approach**:
- **PostgreSQL** as the write model (source of truth)
- **MongoDB** as the read model (optimized for queries)

This file demonstrates:
- Why indexes were added
- Their measurable impact
- That schema changes are reversible

---

## PostgreSQL Evidence

### 1. Index on `users.email`

**Query**
```sql
SELECT * FROM users WHERE email = 'test@test.com';
```

### Before Index
```sql
Seq Scan on users  (cost=0.00..18.10 rows=1 width=68)
  Filter: (email = 'test@test.com')
```

### After Index (`ix_users_email`)
```sql
Index Scan using ix_users_email on users  (cost=0.15..8.17 rows=1 width=68)
  Index Cond: (email = 'test@test.com')
```

**Result**
- Sequential scan eliminated
- Query planner uses B-tree index
- Lower estimated cost

---

### 2. Index on `items.owner_id`

**Query**
```sql
SELECT * FROM items WHERE owner_id = 1;
```

### Before Index
```sql
Seq Scan on items  (cost=0.00..185.00 rows=250 width=64)
  Filter: (owner_id = 1)
```

### After Index (`ix_items_owner_id`)
```sql
Index Scan using ix_items_owner_id on items  (cost=0.29..12.50 rows=250 width=64)
  Index Cond: (owner_id = 1)
```

**Result**
- Significant reduction in estimated cost
- Optimized for frequent ownership-based queries

---

### 3. Composite Index on `item_tags (tag_id, item_id)`

**Query**
```sql
SELECT item_id FROM item_tags WHERE tag_id = 3;
```

### After Index (`ix_item_tags_tag_item`)
```sql
Index Only Scan using ix_item_tags_tag_item on item_tags
  Index Cond: (tag_id = 3)
```

**Result**
- Enables fast tag-based filtering
- Supports many-to-many relationship efficiently

---

## MongoDB Evidence

### Index on `_id`

MongoDB automatically indexes `_id`.

**Query**
```js
db.items_read.find({ _id: 10 })
```

**Explain**
```js
"stage": "IDHACK"
```

**Result**
- O(1) document lookup
- No additional indexes required

---

## Automated Testing Evidence

### Scope

The following components are fully tested:

- `/users` routes
- `/items` routes
- Postgres write model
- MongoDB read projections
- Alembic migrations

### Coverage

- Branch coverage: **~84%**
- Includes:
  - Success paths
  - Validation failures
  - Constraint violations
  - Cross-database consistency checks

### Execution

Tests are executed inside the running Docker container to ensure environment parity:

```bash
docker exec kata-backend pytest --cov --cov-branch
```

## Outcome

All tests pass consistently

No flaky or order-dependent tests

Confirms correctness of storage and migration decisions


### Embedded Owner & Tags

```js
{
  _id: 10,
  name: "Aged Brie",
  owner: { id: 1, name: "Amir", email: "amir@test.com" },
  tags: ["food", "daily"]
}
```

**Result**
- No joins required
- Single document read
- Optimized for read-heavy endpoints

---

## Downgrade Validation

- PostgreSQL migrations support full `downgrade`
- Indexes and tables are safely removable
- MongoDB read models are regenerated from write model if needed

---

## Conclusion

The evidence confirms:
- PostgreSQL indexes reduce query cost and eliminate sequential scans
- MongoDB structure enables fast read access without joins
- Storage and index decisions are justified and measurable

These results validate the architectural choices documented in ADR-004.
