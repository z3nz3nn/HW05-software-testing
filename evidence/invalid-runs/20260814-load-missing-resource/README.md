# Invalid run: Load without resource CSV

- Started: 2026-08-14 00:55:01 ICT
- Finished: 2026-08-14 01:00:01 ICT
- JMeter outcome: 18,989 endpoint samples, 0 errors
- Invalidating condition: the resource-monitor child process received unquoted paths containing spaces and exited before writing its CSV.
- Decision: exclude this run from every reported performance conclusion and rerun Load after adding quoted arguments, monitor stdout/stderr, a five-second fail-fast check, and a final row-count check.

The raw JTL, HTML dashboard, listener output, backend logs, and console log are retained here only as an audit trail. They are not the submitted final Load result.
