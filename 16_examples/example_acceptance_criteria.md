# Example Acceptance Criteria

## AC-101 — Permission denied state

Given an agent without admin permission opens an admin-only action
When the UI renders the action area
Then the user must not see an active admin action button
And if the action is visible for context, it must be disabled with an explanation
And backend must still reject the forbidden action.

## AC-102 — Integration failure state

Given an external integration returns an error
When the UI displays the result
Then the user sees a business-safe message
And can retry or escalate
And raw provider details are not exposed to normal users.
