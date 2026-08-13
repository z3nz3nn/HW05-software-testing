---
name: eshop-performance-testing
description: Design, review, execute, and analyze reproducible JMeter performance tests for the EShop Node.js/SQLite REST API. Use when creating Load, Stress, Spike, or Soak plans; correlating dynamic API data; validating raw JTL metrics; collecting backend resource evidence; or reviewing AI-generated performance-test claims.
---

# EShop performance testing

Build source-backed, data-driven performance evidence without fabricating execution artifacts.

## Workflow

1. Read the assignment and `references/eshop-api.md` completely.
2. Inspect the current backend source before assuming response codes, validation, authorization, database constraints, or reset behavior.
3. Separate every statement into:
   - source-proven fact;
   - pre-run hypothesis or starting SLO;
   - value requiring empirical measurement.
4. Select one non-duplicated end-to-end workflow containing auth-heavy, read-heavy, and transactional endpoint groups. Exercise the identical workflow in Load, Stress, and Spike plans.
5. Parameterize seed values with CSV. Generate volatile identifiers per iteration, correlate returned identifiers, and assert exact parsed values rather than ambiguous substrings.
6. Continue after assertion failure when cleanup is still safe. Never replace an open SQLite file. Start each controlled run with a fresh local backend process and stop only that owned process.
7. Run a short functional smoke test before load. Require equal successful sample counts for all mandatory workflow endpoints and confirm state cleanup.
8. Execute JMeter in non-GUI mode. Preserve the test plan, command, raw JTL, HTML dashboard, backend logs, and per-second process resource samples.
9. Use three different listener/view types across Load, Stress, and Spike. Treat the CLI JTL as the metric source of truth.
10. Run a 10–15 minute Soak test at an empirically selected sustained load. Report stable RPS, p95, errors, and resource ceilings with the calculation method.
11. Analyze CSV JTL with `scripts/summarize_jtl.py` or an equivalent deterministic script. Exclude transaction-controller rows from endpoint totals when they would double count.
12. Give raw artifacts to an AI for analysis, then verify every reported number directly. Record disagreements, source values, and feasible versus hallucinated recommendations.

## Evidence rules

- Never generate or edit JTL rows, resource measurements, screenshots, hardware identity, or video evidence to make results look better.
- Mark missing manual evidence explicitly.
- Record AI tool, local timestamp with timezone, exact prompt, exact output, review, and resulting decision.
- Keep credentials out of plans, reports, screenshots, and Git. Inject tokens at runtime.
- Test only an authorized local SUT.

## Quality gates

- All mandatory endpoints appear in every main plan.
- Dynamic IDs are extracted; generated email and ID are matched on the same returned object.
- A failed read assertion cannot suppress safe deletion when an ID exists.
- Load/Soak thresholds are hypotheses until the JTL proves them.
- Stress breaking point requires a throughput plateau/decline or an SLO/resource breach, not merely the highest configured thread count.
- Spike recovery compares post-spike windows with pre-spike baseline windows.
- Every report number can be traced to a committed raw row set and named percentile method.

