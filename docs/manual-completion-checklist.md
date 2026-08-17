# Manual completion checklist

These items require the student or final submission access. Do not mark them complete without seeing the evidence.

## Identity and group scope

- [x] Replace identity placeholders with **Nguyễn Đình Thái Hưng**.
- [x] Confirm MSSV `23127373`.
- [x] Student confirmed on **2026-08-18** that the account-lifecycle workflow is unique within the group.
- [x] Verify test-plan date `20260814`: the first samples in all four committed JTL files were recorded on 2026-08-14 (Asia/Ho_Chi_Minh).

## Manual screenshots still required (minimum four)

- [ ] `evidence/screenshots/manual/01-dxdiag-system.png`: open `dxdiag` → **System** tab and capture a readable frame containing Computer Name `ASUS`, OS, Processor and Memory.
- [ ] `evidence/screenshots/manual/02-load-jmeter-task-manager.png`: while the full **Load** rerun is active, show JMeter non-GUI output and Task Manager's backend `node.exe` row with **CPU** and **Memory** in one frame.
- [ ] `evidence/screenshots/manual/03-stress-jmeter-task-manager.png`: same evidence for the full **Stress** rerun.
- [ ] `evidence/screenshots/manual/04-spike-jmeter-task-manager.png`: same evidence for the full **Spike** rerun.
- [ ] Check that each scenario frame visibly identifies Load/Stress/Spike, was captured while its load was active, and contains no JWT, token, password or other secret.
- [ ] Reference all four manual images from `Main-Report.md`, rebuild `reports/pdf/Main-Report.pdf`, and visually inspect the rendered pages.

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
- [ ] Student reads the audit and signs off that every reported correction matches `analysis/*.json`; record the sign-off date in `AI-Audit-Report.md`.

## GitHub and video

- [x] Confirm the committed JTL files contain no JWT/password/secret fields before the attempted Gemini transfer.
- [x] Scan tracked files for high-confidence GitHub/OpenAI/Google keys, JWTs and private-key headers; no real credential pattern was found. Remaining password strings are synthetic test data or runtime placeholders.
- [x] Sign in to the `z3nz3nn` GitHub account in Chrome.
- [x] Publish [GitHub Issue #1](https://github.com/z3nz3nn/HW05-software-testing/issues/1) with the committed reproduction screenshot.
- [x] Change repository visibility from **Private** to **Public** after a tracked-file secret-pattern scan; preserve `evidence/screenshots/13-github-public-repository.jpg`.
- [ ] Record the 8–10 minute Vietnamese video using `docs/video-script-vi.md`.
- [ ] Ensure the video is at least 6 minutes, uses the student's own Vietnamese narration, demonstrates the complete Agent Skill workflow, and shows the tool/resource monitor in the same frame.
- [ ] Upload YouTube as **Unlisted**, test the link while signed out/incognito, and replace `[VIDEO_URL]` in `README.md` and `Main-Report.md`.

## Final package

- [ ] Preserve/export the Codex task transcript if the instructor requires low-level orchestration exchanges in addition to the structured AI Audit.
- [x] Check the Markdown and PDF visually; all three PDFs were rebuilt, text-extracted and inspected as rendered contact sheets with no clipped tables or blank trailing page.
- [x] Export `git-commit-log.txt` after the public-repository content/evidence commit (`da0b306`).
- [x] Confirm unauthenticated HTTP 200 for both the repository and Issue #1.
- [ ] Choose self-assessed grade after checking the lecturer's rubric clarification. The provided rows sum to 90 although the table says Total 100.
- [ ] Create `23127373_HW05_AI_Performance_<grade>.zip` only after the four screenshots, sign-off and working YouTube link are committed.
- [ ] Inspect the ZIP for the required Markdown/PDF/JMX/JTL/evidence/Skill/Git-log artifacts and confirm that ignored local runtimes/secrets are absent.
- [ ] Submit the ZIP to Moodle before the deadline shown there.
