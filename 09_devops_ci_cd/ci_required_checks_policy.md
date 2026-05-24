# CI Required Checks Policy

Required before merge:

- pytest
- ruff or equivalent lint
- schema validation tests
- forbidden action tests
- signed job negative tests
- pack-not-in-agent artifact test
- evidence watermark test
- dependency vulnerability scan when available

No PR may merge if tests for signature rejection or forbidden actions fail.
