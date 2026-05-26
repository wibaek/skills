# JavaScript / TypeScript — RFC 7807/9457 Problem Details

## Rule: JavaScript / TypeScript

Use this when the API is implemented in **JavaScript or TypeScript** (Express, Koa, Oak, etc.).

## Recommended library

- **rfc-7807-problem-details** — Zero dependencies, Express/Koa/Oak middleware, TypeScript.
  ```bash
  npm i rfc-7807-problem-details
  ```

## Setup and usage

```ts
import { problemDetailsMiddleware, ProblemDetails } from "rfc-7807-problem-details";

// Register middleware (e.g. Express) — add near end of chain
app.use(problemDetailsMiddleware());

// In route or error handler: throw ProblemDetails
throw new ProblemDetails({
  status: 404,
  title: "Not Found",
  detail: "User not found",
  instance: req.path,
});
```

Middleware catches thrown `ProblemDetails` and sends the response with `Content-Type: application/problem+json` and the correct status code.

## Catching exceptions and throwing ProblemDetails

In a catch block or error handler, map the error to `ProblemDetails` and rethrow (or throw) so the middleware can serialize it:

```ts
try {
  const user = await getUser(userId);
  // ...
} catch (e) {
  if (e instanceof UserNotFound) {
    throw new ProblemDetails({
      status: 404,
      title: "Not Found",
      detail: e.message,
      instance: req.path,
    });
  }
  throw e;
}
```

## Validation errors (422)

Throw `ProblemDetails` with `status: 422` and add an `errors` extension (array of `{ detail, pointer? }`). Ensure the middleware or library passes through custom properties so `errors` is included in the JSON body.
