# Human review of the AI-assisted design

## Source facts checked by the student/agent

- `database.js` creates one `sqlite3.Database` connection and reinitializes all tables whenever the backend starts.
- It does not enable WAL or set a busy timeout.
- `users.email` has no `UNIQUE` constraint and `/api/register` does not reject duplicates, contrary to FR-01.
- `/api/admin/users` and `/api/admin/users/:id` require a valid JWT but do not check `role = admin`, contrary to FR-12/SEC-03.
- The JWT is generated without an expiry in this SUT version.

## Rejected or corrected AI content

1. **Unsupported bottleneck prediction.** Gemini initially asserted that `SQLITE_BUSY` would be the primary bottleneck. A single shared driver connection may instead serialize operations. The test treats contention mode as a measurement question.
2. **False uniqueness premise.** The initial prompt stated duplicate emails fail, reflecting the specification rather than implementation. Source review corrected this and identified a reproducible functional bug candidate.
3. **Simplistic Node.js model.** “Single-threaded means one-core saturation dictates the ceiling” ignores asynchronous native work and SQLite-driver behavior. CPU, latency, throughput, and memory are all measured.
4. **Wrong listener interpretation.** HTML dashboard graph names do not satisfy “three distinct listener/report types.” The final plans contain Summary Report, Aggregate Report, and View Results Tree respectively.
5. **Wasteful input generation.** A 50,000-row CSV is unnecessary. CSV supplies realistic seed fields; a cached Groovy preprocessor adds a UUID email each iteration.
6. **Unsafe database replacement.** Replacing an open SQLite file was rejected. Each controlled run starts and later stops its own backend process; startup creates a clean seed database.
7. **Weak substring assertion.** Gemini’s revised answer suggested searching the GET response for quoted id/email substrings. The final assertion parses JSON and matches both fields on the same object.
8. **Unproven thresholds.** p95 <500 ms and error <1% are explicitly hypotheses, not measured facts. Final thresholds must be based on the raw JTL and resource evidence.

## Measurement verdict on the disputed predictions

- No `SQLITE_BUSY`, timeout or non-200 response occurred in 265,771 accepted endpoint samples across Load/Stress/Spike/Soak. The original “primary lock error” prediction is not supported by these runs.
- Stress shows queuing/diminishing return instead: from 30 to 40 users throughput rises only 0.86% while p95 rises 47.30%. Saturation onset is approximately 30 users, not an observed crash point.
- Whole-machine-normalized Node CPU remained low (Stress p95 3.568% across 16 logical processors), so “one-core CPU saturation dictates the ceiling” was not observed.
- Spike p95 rose to 120 ms and returned to 10 ms in the next 60-second window; recovery is empirically under 60 seconds.
- In the 15-minute Soak, five-minute trailing working-set slope was +0.030 MB/min and private-memory slope −0.025 MB/min. This supports a plateau in the measured interval, not a general proof of no leak.
- The duplicate-email mismatch was proven by two identical requests returning HTTP 200 with IDs 3 and 4.

## Human sign-off checklist

- [x] Confirm the paced account-lifecycle workload is appropriate for the selected localhost user-management workflow.
- [x] Confirm UUID test emails and correlated cleanup do not affect shared/production data; every controlled run targets only localhost and restarts the isolated SUT.
- [x] Inspect smoke sampler responses and exact assertions before the full CLI executions; the accepted smoke produced 182 successful iterations of each endpoint.
- [x] Verify timestamps, filename convention, student identity and MSSV against the committed plans/results.
- [x] Compare every reported aggregate/window metric against the committed raw JTL and deterministic `analysis/*.json` files.
