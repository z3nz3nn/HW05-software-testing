# EShop performance-testing reference

## Selected account-lifecycle workflow

| Group | Request | Required runtime behavior |
| --- | --- | --- |
| Auth-heavy | `POST /api/register` | Generate a UUID email; extract positive `$.id` |
| Read-heavy | `GET /api/admin/users` | Bearer JWT; parsed list must contain one object with the exact ID and email |
| Transactional cleanup | `DELETE /api/admin/users/:id` | Run whenever an ID exists, even after a failed read assertion |

Default base URL: `http://localhost:3000`.

The current SUT source—not this reference—is authoritative. Known version-specific facts to recheck:

- `/api/register` returns HTTP 200 JSON with `id`.
- Email uniqueness is specified but not implemented.
- The admin-user endpoints authenticate JWT but do not enforce the admin role.
- Backend startup drops/recreates/seeds the database.
- JWT has no configured expiry.

## Required JTL fields

Preserve at least `timeStamp`, `elapsed`, `label`, `responseCode`, `responseMessage`, `threadName`, `success`, `failureMessage`, `bytes`, `sentBytes`, `grpThreads`, `allThreads`, `Latency`, and `Connect`.

Use nearest-rank percentiles unless the report declares another method. Calculate error rate as failed endpoint samples divided by endpoint samples. Calculate endpoint sample throughput across the observed wall interval. Divide by three only when estimating completed workflows per second and every iteration contains exactly three successful endpoint samples.

## Default workload hypotheses

These are starting configurations, not measured capacities:

- Load: 15 users, 30-second ramp, 5-minute hold.
- Stress: overlapping built-in Thread Groups producing 10/20/30/40-user steps.
- Spike: 10-user baseline, +40-user 60-second spike, then recovery to baseline.
- Soak: 15 minutes at a level selected after Load/Stress evidence.

Adjust only with a documented reason and retain enough duration to separate ramp, steady state, and recovery.

