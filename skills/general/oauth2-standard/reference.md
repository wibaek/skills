# RFC 6749 Reference

Detailed reference for the OAuth 2.0 Authorization Framework. Definitions for items summarized in SKILL.md.

## Authorization Request (Authorization Code / Implicit)

| Parameter | Required/Optional | Description |
|-----------|------------------|-------------|
| response_type | Required | "code" (Authorization Code) or "token" (Implicit) |
| client_id | Required | Client identifier |
| redirect_uri | Optional* | *Required when multiple URIs registered, partial registration, or none registered |
| scope | Optional | Space-delimited list of scopes |
| state | Recommended | Opaque value for CSRF prevention |

## Authorization Response (Success)

- **Authorization Code**: redirect_uri **query** includes `code`, `state` (required if in request)
- **Implicit**: redirect_uri **fragment** includes `access_token`, `token_type`, `expires_in` (recommended), `scope` (required if different), `state` (required if in request)

## Token Request (Common)

- Method: POST
- Content-Type: application/x-www-form-urlencoded; charset=UTF-8
- grant_type: authorization_code | password | client_credentials | refresh_token | extension (absolute URI)

### Additional Parameters by Grant

| grant_type | Additional required | Notes |
|------------|---------------------|-------|
| authorization_code | code, redirect_uri* (same) | *Required if in auth request |
| password | username, password | |
| client_credentials | (none) | |
| refresh_token | refresh_token | scope must be within originally granted |

## Token Response (Success, Section 5.1)

| Parameter | Required/Optional |
|-----------|-------------------|
| access_token | Required |
| token_type | Required (case insensitive) |
| expires_in | Recommended |
| refresh_token | Optional |
| scope | Required if different from requested |

## Token Endpoint Errors (Section 5.2)

- HTTP 400 (default), 401 possible for invalid_client
- Body: JSON, `error` required, optional `error_description`, `error_uri`

| error | Meaning |
|-------|---------|
| invalid_request | Missing required parameter, duplicate, invalid value, multiple auth mechanisms, or otherwise malformed |
| invalid_client | Client authentication failed |
| invalid_grant | Grant (authorization code, refresh token, password, etc.) invalid, expired, revoked, or mismatch |
| unauthorized_client | Client not authorized to use this grant type |
| unsupported_grant_type | Grant type not supported |
| invalid_scope | Scope invalid or exceeds granted scope |

## Authorization Endpoint Errors (Redirect)

- query or fragment: `error`, `state` (required if in request), optional `error_description`, `error_uri`

| error | Meaning |
|-------|---------|
| invalid_request | Request format error |
| unauthorized_client | Not authorized to request authorization code this way |
| access_denied | Resource owner or server denied |
| unsupported_response_type | response_type not supported |
| invalid_scope | Scope invalid |
| server_error | Server internal error |
| temporarily_unavailable | Temporary overload or maintenance |

## Scope Syntax (ABNF)

```
scope = scope-token *( SP scope-token )
scope-token = 1*( %x21 / %x23-5B / %x5D-7E )
```

Space-delimited, case-sensitive. Server may grant a subset of requested scope; if granted scope differs, response must include `scope`.

## Client Types

- **Confidential**: Can maintain confidentiality of credentials (e.g. server apps).
- **Public**: Cannot maintain confidentiality (SPA, native apps). Authorization server must not rely on public client authentication to identify the client.

## Extension Grant

- Use absolute URI for `grant_type` (e.g. `urn:ietf:params:oauth:grant-type:saml2-bearer`).
- Additional parameters may be defined for token endpoint. Success/error response format is the same.

## Redirection URI Validation

- If redirect_uri is registered, request redirect_uri must match one of them per RFC 3986 Section 6.
- If full URI was registered, use string comparison (RFC 3986 Section 6.2.1).
