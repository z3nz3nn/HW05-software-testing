# HW05 — AI-assisted Performance Testing

| Field | Value |
| --- | --- |
| Student | **Nguyễn Đình Thái Hưng** |
| Student ID | **23127373** |
| Repository | <https://github.com/z3nz3nn/HW05-software-testing> — **Private; make Public before submission if required** |
| Demo video | **[VIDEO_URL — HUMAN REVIEW REQUIRED]** |

This repository contains real JMeter 5.6.3 non-GUI runs against the local EShop Node.js/Express/SQLite backend. The unique account-lifecycle workflow is used unchanged in Load, Stress and Spike:

`POST /api/register` → `GET /api/admin/users` → `DELETE /api/admin/users/:id`

The three endpoint groups are auth-heavy registration, read-heavy user lookup, and transactional user deletion/cleanup. CSV provides seed fields, a Groovy preprocessor generates a UUID email per iteration, the registered ID is correlated, and exact JSON assertions verify that GET returns the same ID/email before deletion.

## Test summary

| Scenario | Workload | Samples | Error % | p95 ms | Throughput samples/s | Main result |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| Load | 15 users; ramp 30s; 300s | 19,311 | 0.00 | 8 | 64.58 | Starting p95/error SLO passed |
| Stress | 10→20→30→40; 120s/step | 139,140 | 0.00 | 95 overall | 290.48 overall | Capacity knee around 30 users; 30→40 adds ~0.9% throughput while p95 rises ~47% |
| Spike | baseline 10; +40 from 120–180s; 420s total | 67,818 | 0.00 | 104 overall | 161.87 overall | Burst p95 120 ms; next 60s window p95 10 ms, recovery <60s |
| Soak | 10 users; ramp 60s; 900s | 39,502 | 0.00 | 6 | 43.94 | 15-minute threshold verified; working-set ceiling 128.10 MB and five-minute trailing slope +0.03 MB/min |

Endurance threshold on this hardware is therefore **10 concurrent users at about 43.94 endpoint samples/s, p95 6 ms, 0% errors, and observed Node working-set ceiling 128.10 MB for 15 minutes**. This is a localhost/co-located test limit, not a production SLA or proof of the maximum possible stable concurrency.

Genuine bugs found: **1** — FR-01 duplicate email accepted twice (both HTTP 200, IDs 3 and 4). See [GitHub Issue #1](https://github.com/z3nz3nn/HW05-software-testing/issues/1), `docs/issues/duplicate-email-registration.md`, and `evidence/issues/duplicate-email/`. The repository remains Private, so Issue visibility is not yet public.

## Deliverables

- Main report: [`Main-Report.md`](Main-Report.md) and `reports/pdf/Main-Report.pdf`
- AI Audit: [`AI-Audit-Report.md`](AI-Audit-Report.md) and `reports/pdf/AI-Audit-Report.pdf`
- AI Critique: [`AI-Critique.md`](AI-Critique.md)
- JMX: [`test-plans/`](test-plans/)
- Full raw JTL: [`results/`](results/)
- JMeter HTML reports: [`reports/html/`](reports/html/)
- Deterministic analyses: [`analysis/`](analysis/)
- Resource/hardware/issue/screenshots: [`evidence/`](evidence/)
- Reusable Agent Skill: [`skills/eshop-performance-testing/`](skills/eshop-performance-testing/)
- Continuous model: [`docs/continuous-performance-testing.md`](docs/continuous-performance-testing.md)
- Vietnamese video script: [`docs/video-script-vi.md`](docs/video-script-vi.md)
- Remaining student actions: [`docs/manual-completion-checklist.md`](docs/manual-completion-checklist.md)

## Reproduce locally

Install Node.js, Java 17 and Apache JMeter 5.6.3. Place the official EShop SUT at `runtime/eshop-sut` and JMeter at `.tools/apache-jmeter-5.6.3`, then install backend dependencies. These two local runtime folders are intentionally ignored.

From **PowerShell in the VS Code terminal**:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\run-scenario.ps1 -Scenario Load
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\run-scenario.ps1 -Scenario Stress
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\run-scenario.ps1 -Scenario Spike
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\run-scenario.ps1 -Scenario Soak
```

The wrapper refuses to overwrite existing results and fails fast when the resource monitor does not produce CSV evidence.

## Self-assessment

| No. | Criteria | Available | Self-assessed | Evidence |
| ---: | --- | ---: | ---: | --- |
| 1 | Task 1 — Load testing | 20 | 20 | JMX, 5-minute raw JTL/HTML/resource analysis |
| 2 | Task 1 — Stress testing | 20 | 20 | Staircase JMX, time-window capacity analysis |
| 3 | Task 1 — Spike testing | 20 | 20 | Baseline/burst/recovery JMX and recovery evidence |
| 4 | Task 2 — AI analysis + misinterpretation hunt | 10 | 10* | Gemini design/review logged; raw-JTL upload G-03/G-04 must be completed |
| 5 | Task 3 — Continuous Performance Testing | 10 | 10 | Flowchart, gates and cost/false-alarm trade-offs |
| 6 | Agent Skills | 10 | 10* | Validated reusable Skill; student must publish demo video |
|  | **Rows total** | **90** | **90*** | Provided rubric rows sum to 90 although the file prints Total 100 |

\* **HUMAN REVIEW REQUIRED:** `090` is only defensible after completing the raw-JTL Gemini upload, same-frame screenshots, required repository visibility and unlisted video. Identity, PDF generation and Issue creation are complete, but the repository is still Private. If any required item remains missing, reduce the self-assessment rather than claim unearned completion.

## Human-review status

The raw JTL, local hardware text report, resource CSVs, duplicate-email API responses and Issue are real. The student still must provide their own dxdiag GUI screenshot, same-frame JMeter/Task Manager evidence, Vietnamese narration/video, working Gemini file-upload permission, group confirmation, required repository visibility, YouTube link and Moodle submission. See the checklist before packaging.
