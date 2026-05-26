---
name: oauth2-standard
description: Standardizes OAuth 2.0 authentication flows per RFC 6749. Covers authorization code, implicit, resource owner password, and client credentials grants; token and authorization endpoints; client authentication; token/error response formats. Use when implementing or reviewing OAuth 2.0, authorization servers, token endpoints, or when the user mentions RFC 6749, OAuth 2.0, or OAuth flows.
---

# OAuth 2.0 Standard (RFC 6749)

Standard to follow when implementing or reviewing OAuth 2.0 authentication flows per RFC 6749.

## Roles

| Role | Description |
|------|-------------|
| **resource owner** | Entity that can grant access to a protected resource (end-user) |
| **resource server** | Server hosting protected resources and accepting requests with access tokens |
| **client** | Application that requests protected resources on behalf of the resource owner with their authorization |
| **authorization server** | Server that issues access tokens to the client after authenticating the resource owner |

## Protocol Endpoints

- **Authorization endpoint**: URI where the client redirects the user-agent to obtain authorization from the resource owner. **GET** required; POST optional.
- **Token endpoint**: URI where the client exchanges an authorization grant or refresh token for an access token. **POST** required.
- **Redirection endpoint**: Client-registered URI where the authorization server returns the authorization result (code or token) to the client.

**TLS** is required for authorization and token endpoint requests/responses. `redirect_uri` must be an absolute URI and must not include a fragment.

## Grant Type Selection

| Grant | `response_type` / `grant_type` | When to use |
|-------|--------------------------------|-------------|
| **Authorization Code** | `response_type=code` → `grant_type=authorization_code` | Recommended for confidential clients and when refresh tokens are needed |
| **Implicit** | `response_type=token` | Public clients (browser); no refresh token. Prefer Authorization Code for security |
| **Resource Owner Password** | `grant_type=password` | Only when trust between client and resource owner is high and other flows are not viable |
| **Client Credentials** | `grant_type=client_credentials` | Confidential clients only; client accessing its own resources |

## Authorization Code Grant

1. **Authorization Request** (user-agent → authorization endpoint, GET)
   - Required: `response_type=code`, `client_id`
   - Recommended: `state` (CSRF prevention)
   - Optional: `redirect_uri`, `scope`
   - Content: `application/x-www-form-urlencoded` (query)

2. **Authorization Response** (redirect to client's redirect_uri)
   - Success: query includes `code`, `state` (required if present in request)
   - Failure: query includes `error`, optional `error_description`, `error_uri`, `state`

3. **Access Token Request** (client → token endpoint, POST)
   - Body `application/x-www-form-urlencoded`, UTF-8:
     - `grant_type=authorization_code`, `code`, and `redirect_uri` (same value as in authorization request if it was included)
   - Confidential client: authenticate with HTTP Basic or `client_id` and `client_secret` in body

4. **Access Token Response**: See "Token Response Format" section.

## Implicit Grant

- Authorization Request: `response_type=token`, `client_id`, optional `redirect_uri`, `scope`, recommended `state`.
- On success, pass `access_token`, `token_type`, `expires_in`, optional `scope`, `state` in the **fragment** of redirect_uri. Must not issue a refresh token.
- Errors also in fragment: `error`, `error_description`, `error_uri`, `state`.

## Resource Owner Password Credentials

- POST to token endpoint with body: `grant_type=password`, `username`, `password`, optional `scope`.
- Confidential clients must authenticate. Protect endpoint against brute force.

## Client Credentials

- POST to token endpoint with body: `grant_type=client_credentials`, optional `scope`.
- Client authentication required. Do not issue a refresh token.

## Refresh Token

- POST to token endpoint: `grant_type=refresh_token`, `refresh_token`, optional `scope` (must be within originally granted scope).
- Client authentication required if confidential or if client credentials were issued.
- On success, return a new access token (and optionally a new refresh token). If a new refresh token is issued, discard the old one.

## Token Response Format (Success)

- HTTP 200, `Content-Type: application/json;charset=UTF-8`
- Headers: `Cache-Control: no-store`, `Pragma: no-cache`
- Body: `access_token` (required), `token_type` (required), `expires_in` (recommended), `refresh_token` (optional), `scope` (required if different from requested)

## Token / Authorization Error Response Format

- Token endpoint errors: HTTP 400 (or 401 for invalid_client), JSON body with `error` (required), optional `error_description`, `error_uri`
- Standard error values: `invalid_request`, `invalid_client`, `invalid_grant`, `unauthorized_client`, `unsupported_grant_type`, `invalid_scope`
- Authorization redirect errors: in redirect_uri query or fragment include `error`, `state`, optional `error_description`, `error_uri`
- Authorization error codes: `invalid_request`, `unauthorized_client`, `access_denied`, `unsupported_response_type`, `invalid_scope`, `server_error`, `temporarily_unavailable`

## Client Authentication (Token Endpoint)

- **Recommended**: HTTP Basic. `username` = `client_id` (application/x-www-form-urlencoded), `password` = `client_secret`.
- **Alternative**: `client_id` and `client_secret` in body (only when Basic cannot be used). Never include in URI.
- Confidential clients or clients with credentials must authenticate when requesting tokens.

## Implementation Checklist

- [ ] Use TLS for authorization and token endpoints
- [ ] Use `state` in authorization requests (redirect flows)
- [ ] Authorization code: single use only, short lifetime (recommended ≤10 minutes)
- [ ] Compare `redirect_uri` exactly with registered value (registration required for public/implicit clients)
- [ ] Include `Cache-Control: no-store` and `Pragma: no-cache` in token responses
- [ ] Client credentials only in body; never expose in URI or logs

## Additional References

- Endpoint parameters ABNF, full error code list, extension grants: [reference.md](reference.md)
- Bearer token usage: RFC 6750
