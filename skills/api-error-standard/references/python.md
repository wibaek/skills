# Python — RFC 7807/9457 Problem Details

## Rule: Python

Use this when the API is implemented in **Python** (Flask, FastAPI, Starlette, Django, etc.).

## Implement directly (no external library)

Define a small Problem exception and convert it to a dict.

```python
from dataclasses import dataclass
from typing import Any

@dataclass
class Problem(Exception):
    type: str
    title: str
    status: int
    detail: str | None = None
    instance: str | None = None
    extensions: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        body: dict[str, Any] = {
            "type": self.type,
            "title": self.title,
            "status": self.status,
        }
        if self.detail is not None:
            body["detail"] = self.detail
        if self.instance is not None:
            body["instance"] = self.instance
        if self.extensions:
            body.update(self.extensions)
        return body
```

## Building a problem response

```python
body = Problem(
    type="about:blank",
    status=404,
    title="Not Found",
    detail="User with id 123 does not exist",
    instance="/users/123",
).to_dict()
# Return body with status=404, Content-Type: application/problem+json
```

## Catching exceptions and returning problem details

```python
try:
    user = get_user(user_id)
except UserNotFound as e:
    raise Problem(
        type="about:blank",
        status=404,
        title="Not Found",
        detail=str(e),
        instance=request.path,
    )
```

## FastAPI example (manual handler)

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(Problem)
async def problem_handler(request: Request, exc: Problem):
    return JSONResponse(
        status_code=exc.status,
        content=exc.to_dict(),
        media_type="application/problem+json",
    )
```

## Flask example (manual handler)

```python
import json
from flask import Flask, Response, request

app = Flask(__name__)

@app.errorhandler(Problem)
def problem_handler(exc: Problem):
    return Response(
        json.dumps(exc.to_dict()),
        status=exc.status,
        content_type="application/problem+json",
    )
```

## Validation errors (422)

Map Pydantic or other validation errors to an `errors` extension with `detail` and optional `pointer` (JSON Pointer into request body). Build `Problem(..., status=422, type=...)` and include `errors` via `extensions` or by updating `to_dict()` output before returning.
