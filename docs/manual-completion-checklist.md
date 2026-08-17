# Manual completion checklist

These items require the student or access that Chrome currently does not provide. Do not mark them complete without seeing the evidence.

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

- [ ] In Chrome extension details, enable **Allow access to file URLs**, then restart/reconnect Chrome if the setting was changed. Two 2026-08-17 attempts still produced no file-chooser event.
- [ ] Upload all four raw JTL files to the existing Gemini Pro conversation.
- [ ] Verify G-03 and corrective G-04 timestamps, prompts, full outputs and screenshots are present in `AI-Audit-Report.md`.
- [ ] Read the output and sign off that every reported correction matches `analysis/*.json`.

## GitHub and video

- [x] Confirm the committed JTL files contain no JWT/password/secret fields before the attempted Gemini transfer.
- [x] Scan tracked files for high-confidence GitHub/OpenAI/Google keys, JWTs and private-key headers; no real credential pattern was found. Remaining password strings are synthetic test data or runtime placeholders.
- [x] Sign in to the `z3nz3nn` GitHub account in Chrome.
- [x] Publish [GitHub Issue #1](https://github.com/z3nz3nn/HW05-software-testing/issues/1) with the committed reproduction screenshot inside the Private repository.
- [ ] If the homework requires public access, explicitly change repository visibility from **Private** to **Public** after reviewing that no secret or unwanted personal data is committed.
- [ ] Record the 8–10 minute Vietnamese video using `docs/video-script-vi.md`.
- [ ] Upload YouTube as **Unlisted**, test in incognito, and replace `[VIDEO_URL]` everywhere.

## Final package

- [ ] Check the Markdown and PDF visually; no missing charts, clipped tables or placeholders except explicitly allowed audit notes.
- [ ] Export the final `git-commit-log.txt` after the last commit.
- [ ] Confirm the GitHub URL is accessible while logged out: `https://github.com/z3nz3nn/HW05-software-testing`.
- [ ] Choose self-assessed grade after checking the lecturer's rubric clarification. The provided rows sum to 90 although the table says Total 100.
- [ ] Create `<StudentID>_HW05_AI_Performance_<grade>.zip` only after all required documents exist.
- [ ] Inspect ZIP contents and submit it to Moodle before the deadline shown there.
