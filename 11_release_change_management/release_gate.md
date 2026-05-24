# Release Gate

A release cannot proceed unless:

- all required tests pass;
- Agent artifact contains no full Country Pack;
- invalid signature and forbidden action tests pass;
- private signing key is not in repository or client artifact;
- documentation states v4.0 does not support Submit/Register;
- rollback plan is approved;
- release owner signs off.
