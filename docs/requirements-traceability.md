# HW05 requirements traceability

> **HUMAN REVIEW REQUIRED:** confirm student ID `23127373`, student name, final date, and that the account-lifecycle workflow is accepted as non-duplicated by the group.

| Requirement | Planned artifact/evidence | Status |
| --- | --- | --- |
| One non-duplicated E2E workflow covering auth/read/transactional groups | `POST /api/register` → `GET /api/admin/users` → `DELETE /api/admin/users/:id` in every plan | Implemented; group confirmation pending |
| Load, Stress, Spike test plans | `test-plans/23127373_{Load,Stress,Spike}_20260814.jmx` | Generated and validated locally |
| Same workflow in all three plans | Shared generator function `add_workflow` | Implemented |
| CSV data-driven input | `data/users.csv` plus UUID-derived email | Implemented |
| Dynamic correlation | JSON Extractor `$.id` → `registered_id` | Implemented |
| Strong assertions and cleanup | Exact parsed JSON match on id/email; delete continues after GET failure | Implemented |
| Three distinct listener/report views | Load: Summary Report; Stress: Aggregate Report; Spike: View Results Tree | Implemented; GUI screenshots pending human recording |
| CLI execution | `scripts/run-scenario.ps1` invokes JMeter `-n` | Implemented |
| Raw JTL and HTML reports | `results/*.jtl`, `reports/html/*` | Pending execution |
| Resource evidence | Per-second Node process CSV; browser report screenshots | Pending execution; Task Manager same-frame capture is manual |
| 10–15 minute endurance threshold | 15-minute Soak plan plus measured analysis | Pending execution |
| AI-first design and review | Gemini Pro multi-turn audit with screenshots and verbatim prompts/outputs | In progress |
| AI analysis/misinterpretation hunt | Raw JTL metrics compared with Gemini interpretation | Pending results |
| Optimization feasibility critique | Source-backed classification | Pending results |
| Continuous performance model + flowchart | Main report section and CI proposal | Pending |
| Agent Skill | `skills/eshop-performance-testing` | In progress |
| Demo video ≥6 minutes, same-frame tool/resource monitor, Vietnamese narration | `docs/video-script-vi.md` | Script pending; recording is manual-only |
| AI Critique 200–300 words | `AI-Critique.md` | Pending final Gemini interaction |
| AI Audit Report | `AI-Audit-Report.md` | In progress |
| Hardware screenshot/spec table | Hardware text evidence and report table | Text evidence pending; GUI screenshot manual-only |
| Genuine GitHub Issues | Duplicate email bug candidate, only after live reproduction | Pending reproduction |
| Git commit per procedure step | Logical commits and `git-commit-log.txt` | In progress |
| Main report Markdown + PDF | `Main-Report.md`, `reports/pdf/Main-Report.pdf` | Pending |
| README self-assessment and summary | `README.md` | Pending final metrics/video URL |

