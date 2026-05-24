# Release Runbook

Release note for this PR: v4.0 is a Controlled Runtime MVP. The Local Agent currently uses
`MockActionExecutor`; this PR does not implement the real Windows/ASYCUDA foreground GUI executor.
The verified field execution baseline remains `v3.1.1 SafeBrake` until GUI executor integration
lands.

1. Open a pull request to `main`.
2. Require the `SSS Quality Gate` workflow to pass.
3. Review security-sensitive diffs, especially signing, Agent execution, and country pack boundaries.
4. Build the Agent artifact from `agent/build_nuitka.ps1` only after approval.
5. Validate that the artifact excludes `control_plane/packs/**`.
6. Roll back by revoking affected licenses and redeploying the previous signed Agent artifact.
