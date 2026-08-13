# Manual completion checklist

These items require the student or access that Chrome currently does not provide. Do not mark them complete without seeing the evidence.

## Identity and group scope

- [ ] Replace `[HỌ TÊN]` / `[FULL NAME]` with the student's official full name.
- [ ] Confirm MSSV `23127373`; regenerate filenames if it is wrong.
- [ ] Send `docs/group-selection-message.md` and save the group's confirmation that the workflow is unique.
- [ ] Confirm test date `20260814` is acceptable as the filename date.

## Screenshots and hardware

- [ ] Open `dxdiag` GUI, verify hostname `ASUS`, and capture a readable screenshot.
- [ ] For Load, Stress and Spike, capture JMeter/tool output and Task Manager's `node.exe` CPU/Memory in the **same frame**. The existing HTML/report screenshots are supporting evidence, not a substitute for this requirement.
- [ ] Verify every screenshot shows the correct scenario and no secret/JWT.
- [ ] Add the manual images to `evidence/screenshots/manual/` and reference them from `Main-Report.md`.

## Gemini raw-JTL analysis

- [ ] In Chrome extension details, enable **Allow access to file URLs**.
- [ ] Upload all four raw JTL files to the existing Gemini Pro conversation.
- [ ] Verify G-03 and corrective G-04 timestamps, prompts, full outputs and screenshots are present in `AI-Audit-Report.md`.
- [ ] Read the output and sign off that every reported correction matches `analysis/*.json`.

## GitHub and video

- [ ] Confirm the public repository contains no secret or personal data.
- [ ] Publish the duplicate-email issue on this repository's GitHub Issues page and attach `evidence/screenshots/04-duplicate-email-reproduction.png`.
- [ ] Record the 8–10 minute Vietnamese video using `docs/video-script-vi.md`.
- [ ] Upload YouTube as **Unlisted**, test in incognito, and replace `[VIDEO_URL]` everywhere.

## Final package

- [ ] Check the Markdown and PDF visually; no missing charts, clipped tables or placeholders except explicitly allowed audit notes.
- [ ] Export the final `git-commit-log.txt` after the last commit.
- [ ] Confirm public GitHub URL: `https://github.com/z3nz3nn/HW05-software-testing`.
- [ ] Choose self-assessed grade after checking the lecturer's rubric clarification. The provided rows sum to 90 although the table says Total 100.
- [ ] Create `<StudentID>_HW05_AI_Performance_<grade>.zip` only after all required documents exist.
- [ ] Inspect ZIP contents and submit it to Moodle before the deadline shown there.
