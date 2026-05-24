# Codex Task 02 — Signed Job Plan

Implement Ed25519 signing and verification.

Requirements:

- server signs canonical job payload without `signature` field;
- agent verifies signature before any execution;
- invalid signature test;
- expired job test;
- wrong machine test;
- wrong tenant test;
- unauthorized mode test;
- forbidden Submit/Register/Payment action test.
