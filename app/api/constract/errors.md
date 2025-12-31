# Error Catalog — Gilded Rose Inventory API

This document defines all error types used by the Gilded Rose Inventory API.

All errors follow **RFC 7807 – Problem Details for HTTP APIs** and are returned
with the content type:


Each error type defined here is part of the **public API contract** and must be
kept in sync with `openapi.yaml`.

---

## INVALID_INPUT

- **HTTP Status:** `400 Bad Request`
- **Type:** `https://example.com/problems/invalid-input`
- **Title:** Invalid input

### When it occurs
- Request payload fails validation
- Required fields are missing
- Field values are out of allowed range
- Request body structure is invalid

### Example response

```json
{
  "type": "https://example.com/problems/invalid-input",
  "title": "Invalid input",
  "status": 400,
  "detail": "Quality must be between 0 and 50"
}
```

## ITEM_NOT_FOUND

HTTP Status: 404  
Type: https://example.com/problems/item-not-found  
Title: Item not found

Triggered when:
- Item identifier does not exist
- Requested resource has already been deleted

Example:
```json
{
  "type": "https://example.com/problems/item-not-found",
  "title": "Item not found",
  "status": 404,
  "detail": "Item with given id does not exist"
}
```


## INTERNAL_ERROR

HTTP Status: 500
Type: https://example.com/problems/internal-error

Title: Internal server error

Triggered when:

Unexpected server failure

Unhandled exception

Example:
```json
{
  "type": "https://example.com/problems/internal-error",
  "title": "Internal server error",
  "status": 500
}
```

- **Guarantees** 

# All errors must be documented here

# All errors must appear in openapi.yaml

# New error types require ADR update