# Example Filled Task — Novice-friendly Ticket Page

## Business Objective
Make the ticket page understandable for a new customer service agent without engineering context.

## Evidence
- Route: `/admin/tickets`
- Current issue: primary action says `Create Ticket`, empty state says `No data`.
- User risk: new agent may not know when to create a ticket or what kind of customer issue belongs here.

## Required Change
- Rename page title to `Customer Issues`.
- Rename CTA to `New Customer Issue`.
- Replace empty state with actionable copy:
  `No customer issues yet. When a customer reports a delivery problem, create a new issue to track the follow-up.`
- Preserve existing API and status enum.

## Acceptance Criteria
Given a new customer service agent opens the page,
When there are no tickets,
Then the page explains what the list is for and provides a clear next action.

## Tests
- typecheck
- component test for empty state
- manual QA screenshot
