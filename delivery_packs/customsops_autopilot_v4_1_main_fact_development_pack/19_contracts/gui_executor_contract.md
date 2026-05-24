# GUI Executor Contract

The GUI executor accepts already validated job steps only.

Allowed actions remain constrained by Agent action policy:

- click
- paste
- click_paste
- hotkey
- wait
- screenshot
- store_line_safebrake

The executor must not know or load complete country pack files. It executes signed steps as generic foreground actions.

Non-Windows real execution must fail closed.
