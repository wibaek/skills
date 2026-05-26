---
name: api-error-standard
description: Standardizes API error responses using RFC 9457/7807 (Problem Details). Recommends libraries and patterns for Python, JavaScript/TypeScript, and Java to return application/problem+json. Use for API error handling or when RFC 7807/9457, problem details, or standardized errors are mentioned.
---

# API Error Standard (RFC 9457 / RFC 7807)

Standardize API errors as **Problem Details**: JSON with `type`, `title`, `status`, `detail`, `instance`, and optional extensions. Response media type: `application/problem+json`.

## Problem Details Object (minimal)

| Member   | Type   | Description |
|----------|--------|-------------|
| type     | string | URI identifying problem type (default `about:blank`) |
| title    | string | Short human-readable summary |
| status   | number | HTTP status code (advisory; must match response status) |
| detail   | string | Explanation specific to this occurrence |
| instance | string | URI identifying this occurrence (optional) |

Extensions: add custom members (e.g. `errors`, `balance`). Clients must ignore unknown members. RFC 9457 defines full field semantics.

---

## Workflow: Catch Exception → Standard Output

1. **Identify framework** (FastAPI, Express, Spring, plain WSGI/ASGI, etc.).
2. **Apply the language-specific rule** (see sub-rules below).
3. **Map exception to problem**: set `status`, `type`, `title`, `detail`, `instance`; do not expose stack traces or internals.
4. **Return** with same status code and `Content-Type: application/problem+json`.

---

## Language sub-rules

Apply the rule that matches the project language:

| Language              | Sub-rule |
|-----------------------|----------|
| **Python**            | [references/python.md](references/python.md) — httpproblem, fastapi-rfc7807 |
| **JavaScript/TypeScript** | [references/javascript-typescript.md](references/javascript-typescript.md) — rfc-7807-problem-details (Express/Koa/Oak) |
| **Java**              | [references/java.md](references/java.md) — Spring ProblemDetail, ResponseEntityExceptionHandler |

---

## Validation Errors (RFC 9457 style)

For 422 Unprocessable Content with field-level errors, use an extension (e.g. `errors`) with an array of objects containing `detail` and optional `pointer` (JSON Pointer):

```json
{
  "type": "https://api.example.com/errors/validation",
  "title": "Your request is not valid.",
  "status": 422,
  "errors": [
    { "detail": "must be a positive integer", "pointer": "#/age" },
    { "detail": "must be 'green', 'red' or 'blue'", "pointer": "#/profile/color" }
  ]
}
```

Map validation libraries (Pydantic, class-validator, Bean Validation) to this shape in the relevant language sub-rule.

---

## Checklist

- [ ] Response status code matches `status` in body
- [ ] `Content-Type: application/problem+json`
- [ ] `type` is stable URI or omitted (→ `about:blank`)
- [ ] No stack traces or internals in `detail` or public extensions
- [ ] Validation errors use structured extension (e.g. `errors` + `pointer`)
