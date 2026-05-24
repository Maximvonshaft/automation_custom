# Execution Brief

## Objective

Deliver v4.1 as a controlled extension of v4.0 `main`, not as a rewrite.

The implementation must join three things:

1. fixed Excel manifest intake;
2. server-side declaration-to-job compilation;
3. Windows-only ASYCUDA foreground GUI execution behind signed-plan validation.

## Starting Point

Use `main` commit `45fd4a9f5f95247432814293bced96badc80cd10` as the factual baseline.

Do not treat any unmerged v4.1 draft branch as production fact.

## Production Engineering Rules

- Work behind small PRs with GitHub Actions quality gates.
- Keep feature boundaries test-first where security or packaging risk exists.
- Preserve existing v4.0 tests.
- Add Windows GUI behavior behind adapters so Linux CI can test fail-closed and routing behavior.
- Put real Windows lab smoke evidence in the release report before production use.

## Implementation Sequence

1. Baseline audit and tests.
2. Manifest contract, schemas, and sanitized fixtures.
3. Server-side parser and declaration builder.
4. Job compiler extension.
5. Executor interface and Windows GUI adapter.
6. Operator intake shell.
7. Evidence compatibility and packaging inspection.
8. Release gate.

