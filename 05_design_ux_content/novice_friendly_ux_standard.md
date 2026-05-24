# Novice-friendly UX Standard

## Target

A non-expert user should understand:
1. where they are,
2. what the page is for,
3. what to do first,
4. what happens after action,
5. how to recover from failure,
6. when the task is complete.

## Standards

### Navigation
- Use business task language, not internal system language.
- Critical workflows must be top-level or one click away.
- Avoid exposing debug/configuration areas to normal operators.

### Layout
- One primary task per screen where possible.
- One obvious primary CTA.
- Secondary actions must not compete with primary action.
- Advanced actions should be progressively disclosed.

### Copy
- Prefer plain business language.
- Avoid raw enum names and technical errors.
- Explain consequences for risky actions.
- Provide examples for ambiguous fields.

### Feedback
- Loading state: tell user system is processing.
- Empty state: explain why empty and what to do next.
- Error state: explain next action.
- Success state: confirm completion and next step.
