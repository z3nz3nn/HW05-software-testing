# HW05 requirements traceability

> Student identity is confirmed as Nguyễn Đình Thái Hưng, MSSV `23127373`. The student confirmed the workflow's group uniqueness on 2026-08-18. The filename date `20260814` matches the first-sample date in every committed JTL file.

| Requirement | Planned artifact/evidence | Status |
| --- | --- | --- |
| One non-duplicated E2E workflow covering auth/read/transactional groups | `POST /api/register` → `GET /api/admin/users` → `DELETE /api/admin/users/:id` in every plan | Implemented; student confirmed group uniqueness on 2026-08-18 |
| Load, Stress, Spike test plans | `test-plans/23127373_{Load,Stress,Spike}_20260814.jmx` | Generated and validated locally |
| Same workflow in all three plans | Shared generator function `add_workflow` | Implemented |
| CSV data-driven input | `data/users.csv` plus UUID-derived email | Implemented |
| Dynamic correlation | JSON Extractor `$.id` → `registered_id` | Implemented |
| Strong assertions and cleanup | Exact parsed JSON match on id/email; delete continues after GET failure | Implemented |
| Three distinct listener/report views | Load: Summary Report; Stress: Aggregate Report; Spike: View Results Tree | Implemented; GUI screenshots pending human recording |
| CLI execution | `scripts/run-scenario.ps1` invokes JMeter `-n` | Implemented |
| Raw JTL and HTML reports | `results/*.jtl`, `reports/html/*` | Completed for Load/Stress/Spike/Soak |
| Resource evidence | Per-second Node process CSV; browser report screenshots; four original GUI captures | Completed; dxdiag plus Load/Stress/Spike same-frame screenshots visually reviewed |
| 10–15 minute endurance threshold | 15-minute Soak plan plus measured analysis | Completed: 10 users, 43.94 samples/s, p95 6 ms, 128.10 MB working-set ceiling |
| AI-first design and review | Gemini Pro multi-turn audit with screenshots and prompts/outputs | Completed: G-01/G-02 design review plus G-03/G-04/G-05 raw-data correction chain |
| AI analysis/misinterpretation hunt | Raw JTL metrics compared with Gemini interpretation | Completed: truncated estimates rejected, deterministic metrics matched, causal/leak overclaims retracted |
| Optimization feasibility critique | Source-backed classification | Completed in Main Report section 9 |
| Continuous performance model + flowchart | Main report section and CI proposal | Completed in `docs/continuous-performance-testing.md` |
| Agent Skill | `skills/eshop-performance-testing` | Completed and official validator passed |
| Demo video ≥6 minutes, same-frame tool/resource monitor, Vietnamese narration | <https://youtu.be/hz-N_-Y7VZY> | 15:05 and sampled visual requirements verified; still Private, must become Unlisted; student narration confirmation pending |
| AI Critique 200–300 words | `AI-Critique.md` | Completed: 279 words |
| AI Audit Report | `AI-Audit-Report.md` | Completed through G-05 with timestamps, prompts, outputs, screenshots and human decisions |
| Hardware screenshot/spec table | Hardware text evidence, report table and `evidence/screenshots/manual/01-dxdiag-system.png` | Completed; GUI screenshot shows hostname `ASUS`, OS, CPU and RAM |
| Genuine GitHub Issues | Duplicate email bug candidate, only after live reproduction | Issue #1 created with HTTP 200 IDs 3/4; repository and Issue are Public and unauthenticated HTTP 200 was verified |
| Git commit per procedure step | Logical commits and `git-commit-log.txt` | Completed through final content/evidence commit; log exported |
| Main report Markdown + PDF | `Main-Report.md`, `reports/pdf/Main-Report.pdf` | Completed; all three PDFs rendered and visually inspected |
| README self-assessment and summary | `README.md` | Completed with real metrics and video link; video visibility/narration confirmation remain |
