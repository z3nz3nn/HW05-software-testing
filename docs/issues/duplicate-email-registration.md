# Bug report — FR-01 duplicate email accepted

## Title

`POST /api/register accepts the same email twice instead of enforcing FR-01 uniqueness`

## Environment

- SUT: `ttbhanh/eshop-sut`, backend on `http://localhost:3000`
- OS: Windows 11 Pro 10.0.26200
- Node.js: v24.16.0
- Captured: 2026-08-14 00:54:20 ICT

## Preconditions

Start the backend from a clean seed database. No user exists with `duplicate-evidence@loadtest.local`.

## Steps to reproduce

1. Send `POST /api/register` with `Content-Type: application/json` and this body:

   ```json
   {"email":"duplicate-evidence@loadtest.local","name":"Duplicate Evidence","password":"Duplicate123!"}
   ```

2. Send the identical request a second time.

## Actual result

Both requests return HTTP 200 and create different user IDs:

```text
First:  HTTP 200 {"message":"User registered successfully","id":3}
Second: HTTP 200 {"message":"User registered successfully","id":4}
```

## Expected result

FR-01 states that email must be unique. The second request should be rejected with a safe 4xx response, and no second row should be inserted.

## Impact

Duplicate identities make authentication/account ownership ambiguous and allow unbounded duplicate rows. Performance tests must generate UUID emails to avoid silently exercising this regression.

## Evidence

- `evidence/issues/duplicate-email/reproduction.json`
- `evidence/issues/duplicate-email/reproduction.html`
- `evidence/screenshots/04-duplicate-email-reproduction.png`
- Reproduction script: `scripts/reproduce-duplicate-email.ps1`

## Suggested fix direction

Add a migration/constraint such as `UNIQUE COLLATE NOCASE` for normalized email, validate before insert, and map uniqueness errors to a stable 409 response. Migration behavior and case/whitespace normalization need explicit tests; do not modify the database schema only for the performance-test assignment without owner approval.

Published as [GitHub Issue #1](https://github.com/z3nz3nn/HW05-software-testing/issues/1) on 2026-08-17. The source-backed report includes the committed reproduction screenshot; the repository was verified as Private, so public visibility remains pending. The suggested fix has not been implemented or benchmarked.
