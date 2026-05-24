# State Machine and Workflow Spec

## Agent execution states

- `INIT`
- `LOAD_JOB`
- `VERIFY_SIGNATURE`
- `VERIFY_LICENSE`
- `VERIFY_MACHINE`
- `VERIFY_MODE`
- `PREPARE_WINDOW`
- `EXECUTE_STEP`
- `CAPTURE_EVIDENCE`
- `HANDLE_EXPECTED_BLOCK`
- `PACKAGE_EVIDENCE`
- `UPLOAD_OR_EXPORT`
- `DONE`
- `ABORTED`

## Abort conditions

- invalid signature
- expired job
- wrong machine
- tenant revoked
- mode not allowed
- forbidden action encountered
- ASYCUDA window not found
- foreground window mismatch after recovery attempts
- evidence write failure

## Allowed action grammar v4.0

- `click(x, y)`
- `paste(value_token_or_plain_value)`
- `hotkey(keys)`
- `wait(ms)`
- `screenshot(label)`
- `store_line_safebrake()` only when mode is `safeBrakeStore`

Forbidden:

- `submit`
- `register`
- `payment`
- `read_password`
- `read_cookie`
- `backend_request`
