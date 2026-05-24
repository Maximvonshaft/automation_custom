# Empty / Error / Loading / Disabled State Standard

## Empty State

Must include:
- what is empty,
- why it may be empty,
- what to do next,
- primary action if applicable.

## Error State

Must include:
- user-safe explanation,
- actionable next step,
- retry/contact/admin path where applicable,
- no raw stack trace or secret.

## Loading State

Must include:
- visible progress or clear processing message,
- disabled duplicate submission where needed,
- timeout/failure handling for long operations.

## Disabled State

Must include:
- reason for disabled action,
- how to become eligible if relevant.
