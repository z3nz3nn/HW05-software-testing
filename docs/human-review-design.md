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

## Human sign-off checklist

- [ ] Confirm the workload resembles expected local-user behavior.
- [ ] Confirm test emails and user cleanup do not affect shared/production data (tests run only on localhost).
- [ ] Inspect at least one sampler response in GUI before full CLI execution.
- [ ] Verify timestamps, filenames, and student identity.
- [ ] Compare all reported metrics against the committed raw JTL.

