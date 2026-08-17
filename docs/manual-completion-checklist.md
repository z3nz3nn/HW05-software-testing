# Manual completion checklist

These items require the student or final submission access. Do not mark them complete without seeing the evidence.

## Identity and group scope

- [x] Replace identity placeholders with **Nguyễn Đình Thái Hưng**.
- [x] Confirm MSSV `23127373`.
- [ ] Send `docs/group-selection-message.md` and save the group's confirmation that the workflow is unique.
- [ ] Confirm test date `20260814` is acceptable as the filename date.

## Screenshots and hardware

- [ ] Open `dxdiag` GUI, verify hostname `ASUS`, and capture a readable screenshot.
- [ ] For Load, Stress and Spike, capture JMeter/tool output and Task Manager's `node.exe` CPU/Memory in the **same frame**. The existing HTML/report screenshots are supporting evidence, not a substitute for this requirement.
- [ ] Verify every screenshot shows the correct scenario and no secret/JWT.
- [ ] Add the manual images to `evidence/screenshots/manual/` and reference them from `Main-Report.md`.

## Gemini raw-JTL analysis

- [x] Enable Chrome file access; the initial U-01 failure is retained in the audit and the later chooser succeeded.
- [x] Upload all four raw JTL files to the existing Gemini Pro conversation.
- [x] Record G-03, corrective G-04 and interpretation-boundary G-05 timestamps, prompts, outputs, screenshots and human decisions in `AI-Audit-Report.md`.
- [ ] Read the output and sign off that every reported correction matches `analysis/*.json`.

## GitHub and video

- [x] Confirm the committed JTL files contain no JWT/password/secret fields before the attempted Gemini transfer.
- [x] Scan tracked files for high-confidence GitHub/OpenAI/Google keys, JWTs and private-key headers; no real credential pattern was found. Remaining password strings are synthetic test data or runtime placeholders.
- [x] Sign in to the `z3nz3nn` GitHub account in Chrome.
- [x] Publish [GitHub Issue #1](https://github.com/z3nz3nn/HW05-software-testing/issues/1) with the committed reproduction screenshot.
- [x] Change repository visibility from **Private** to **Public** after a tracked-file secret-pattern scan; preserve `evidence/screenshots/13-github-public-repository.jpg`.
- [ ] Record the 8–10 minute Vietnamese video using `docs/video-script-vi.md`.
- [ ] Upload YouTube as **Unlisted**, test in incognito, and replace `[VIDEO_URL]` everywhere.

## Final package

- [ ] Preserve/export the Codex task transcript if the instructor requires low-level orchestration exchanges in addition to the structured AI Audit.
- [x] Check the Markdown and PDF visually; all three PDFs were rebuilt, text-extracted and inspected as rendered contact sheets with no clipped tables or blank trailing page.
- [x] Export `git-commit-log.txt` after the final content/evidence commit (`a6adf69`).
- [x] Confirm unauthenticated HTTP 200 for both the repository and Issue #1.
- [ ] Choose self-assessed grade after checking the lecturer's rubric clarification. The provided rows sum to 90 although the table says Total 100.
- [ ] Create `<StudentID>_HW05_AI_Performance_<grade>.zip` only after all required documents exist.
- [ ] Inspect ZIP contents and submit it to Moodle before the deadline shown there.
