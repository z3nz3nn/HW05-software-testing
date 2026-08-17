# Manual screenshot drop folder

Place exactly named, original screenshots here. Do not crop away the scenario identity, process name, CPU/Memory columns or dxdiag field labels.

## Required files

1. `01-dxdiag-system.png`
   - dxdiag **System** tab is visible.
   - Computer Name `ASUS`, Operating System, Processor and Memory are readable.
2. `02-load-jmeter-task-manager.png`
   - One frame shows the active Load JMeter non-GUI terminal and Task Manager → Details.
   - Backend `node.exe`, CPU and Memory are readable.
3. `03-stress-jmeter-task-manager.png`
   - Same requirements while the Stress run is active.
4. `04-spike-jmeter-task-manager.png`
   - Same requirements while the Spike run is active.

## Reject and retake when

- JMeter and Task Manager are in separate images.
- The frame does not identify Load, Stress or Spike.
- `node.exe` is hidden, idle after the run, or its CPU/Memory columns are missing.
- Text is unreadable or a window covers the required evidence.
- A JWT, token, password or other secret is visible.

After adding all four files, update the four checkboxes in `docs/manual-completion-checklist.md`, embed the images in `Main-Report.md`, rebuild its PDF and visually inspect the rendered pages.
