# Manual completion checklist

These items require the student or final submission access. Do not mark them complete without seeing the evidence.

## Identity and group scope

- [x] Replace identity placeholders with **Nguyễn Đình Thái Hưng**.
- [x] Confirm MSSV `23127373`.
- [x] Student confirmed on **2026-08-18** that the account-lifecycle workflow is unique within the group.
- [x] Verify test-plan date `20260814`: the first samples in all four committed JTL files were recorded on 2026-08-14 (Asia/Ho_Chi_Minh).

## Manual screenshots still required (minimum four)

- [x] `evidence/screenshots/manual/01-dxdiag-system.png`: open `dxdiag` → **System** tab and capture a readable frame containing Computer Name `ASUS`, OS, Processor and Memory.
- [x] `evidence/screenshots/manual/02-load-jmeter-task-manager.png`: while the full **Load** rerun is active, show JMeter non-GUI output and Task Manager's backend `node.exe` row with **CPU** and the working-set resource column in one frame.
- [x] `evidence/screenshots/manual/03-stress-jmeter-task-manager.png`: same evidence for the full **Stress** rerun.
- [x] `evidence/screenshots/manual/04-spike-jmeter-task-manager.png`: same evidence for the full **Spike** rerun.
- [x] Check that each scenario frame visibly identifies Load/Stress/Spike, was captured while its load was active, and contains no JWT, token, password or other secret.
- [x] Reference all four manual images from `Main-Report.md`, rebuild `reports/pdf/Main-Report.pdf`, and visually inspect the rendered pages.

Use **PowerShell in the VS Code terminal**, one command at a time. Arrange the terminal and Task Manager → Details side-by-side before taking each screenshot:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\run-scenario.ps1 -Scenario Load -ArtifactSuffix manual-evidence
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\run-scenario.ps1 -Scenario Stress -ArtifactSuffix manual-evidence
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\run-scenario.ps1 -Scenario Spike -ArtifactSuffix manual-evidence
```

The suffix protects the accepted result files from overwrite. These are full evidence reruns (approximately 5, 8 and 7 minutes), not shortened smoke tests. If a suffixed result already exists, use a new suffix such as `manual-evidence-2`; the wrapper intentionally refuses overwrites.

## Gemini raw-JTL analysis

- [x] Enable Chrome file access; the initial U-01 failure is retained in the audit and the later chooser succeeded.
- [x] Upload all four raw JTL files to the existing Gemini Pro conversation.
- [x] Record G-03, corrective G-04 and interpretation-boundary G-05 timestamps, prompts, outputs, screenshots and human decisions in `AI-Audit-Report.md`.
- [x] Cross-check the reported G-04/G-05 corrections against `analysis/*.json`; the final human decisions and accepted/rejected claims are recorded in `AI-Audit-Report.md`.

## GitHub and video

- [x] Confirm the committed JTL files contain no JWT/password/secret fields before the attempted Gemini transfer.
- [x] Scan tracked files for high-confidence GitHub/OpenAI/Google keys, JWTs and private-key headers; no real credential pattern was found. Remaining password strings are synthetic test data or runtime placeholders.
- [x] Sign in to the `z3nz3nn` GitHub account in Chrome.
- [x] Publish [GitHub Issue #1](https://github.com/z3nz3nn/HW05-software-testing/issues/1) with the committed reproduction screenshot.
- [x] Change repository visibility from **Private** to **Public** after a tracked-file secret-pattern scan; preserve `evidence/screenshots/13-github-public-repository.jpg`.
- [x] Record and upload the video. Chrome verified a duration of **15:05** and sampled frames show JMeter/VS Code plus Task Manager in one frame, the Agent Skill, audit/bug evidence and the continuous model.
- [ ] Student confirms that the recording uses their own audible Vietnamese narration; Chrome exposed no captions/audio transcript for independent verification.
- [ ] Change YouTube visibility from **Private** to **Unlisted** and test the link while signed out/incognito.
- [x] Insert `https://youtu.be/hz-N_-Y7VZY` in `README.md` and `Main-Report.md`; the video-link placeholder is removed.

## Final package

- Optional only if requested by the instructor: preserve/export the Codex task transcript in addition to the structured AI Audit.
- [x] Check the Markdown and PDF visually; all three PDFs were rebuilt, text-extracted and inspected as rendered contact sheets with no clipped tables or blank trailing page.
- [x] Export `git-commit-log.txt` after the manual screenshots/video-link update (`b191a89`).
- [x] Confirm unauthenticated HTTP 200 for both the repository and Issue #1.
- [x] Use self-assessed grade `090`, matching the six published rubric rows (which sum to 90 even though the table prints Total 100).
- [ ] Create `23127373_HW05_AI_Performance_<grade>.zip` only after the four screenshots, sign-off and working YouTube link are committed.
- [ ] Inspect the ZIP for the required Markdown/PDF/JMX/JTL/evidence/Skill/Git-log artifacts and confirm that ignored local runtimes/secrets are absent.
- [ ] Submit the ZIP to Moodle before the deadline shown there.
