# Java — RFC 7807/9457 Problem Details

## Rule: Java

Use this when the API is implemented in **Java** with **Spring Framework 6+** (Spring Boot 3.1+).

## Built-in support (no extra library)

Spring provides `ProblemDetail`, `ErrorResponse`, and `ResponseEntityExceptionHandler`. Enable problem details:

- **Spring Boot 3.1+:** `spring.mvc.problemdetails.enabled=true`

## Returning ProblemDetail from exception handlers

```java
@ControllerAdvice
public class ProblemDetailsAdvice extends ResponseEntityExceptionHandler {

    @ExceptionHandler(UserNotFoundException.class)
    public ProblemDetail handleUserNotFound(UserNotFoundException ex, WebRequest req) {
        ProblemDetail pd = ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, ex.getMessage());
        pd.setTitle("Not Found");
        pd.setInstance(URI.create(((ServletWebRequest) req).getRequest().getRequestURI()));
        return pd;
    }
}
```

Return `ProblemDetail` or `ErrorResponse` from `@ExceptionHandler`; Spring serializes with `application/problem+json`.

## Mapping exception to problem

- **status** — Use `ProblemDetail.forStatusAndDetail(HttpStatus.XXX, detail)` or `setStatus()`.
- **title** — `setTitle(...)`.
- **detail** — From exception message or safe description (avoid stack traces).
- **type** — `setType(URI.create("https://api.example.com/errors/..."))` or omit for `about:blank`.
- **instance** — `setInstance(URI.create(request.getRequestURI()))` when useful.

## Validation errors (422)

For Bean Validation (e.g. `@Valid`), use an extension such as `errors` with a list of `{ "detail": "...", "pointer": "#/fieldName" }`. Build a `ProblemDetail` with status 422 and add the list via `pd.setProperty("errors", listOfErrors)`.
