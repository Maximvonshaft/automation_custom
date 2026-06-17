# Sequence Flows

## Flow A — SafeBrake drag-and-drop

```text
Operator drags Excel
Agent computes SHA-256 and submits intake request
Control Plane classifies template
Control Plane parses Combine/Separate rows
Control Plane builds declaration_model
Operator selects target row/declaration
Control Plane compiles safeBrakeStore signed job
Agent downloads signed job
Agent validates signature, tenant, machine, mode, expiry
Agent executes Windows GUI actions
SafeBrake intentionally blocks Store final success
Agent packages evidence bundle
Control Plane records run metadata
```

## Flow B — fillOnly preview

Same as Flow A, but no `store_line_safebrake` action is appended.
