# Admin Guide

The HQ Control Plane owns country packs, machine registration, licensing, job compilation, signing,
evidence intake, and revocation.

Production deployment requirements:

- Keep `CUSTOMSOPS_SIGNING_PRIVATE_KEY_PEM` only in the Control Plane secret store.
- Distribute only the Ed25519 public key to Agent builds.
- Never ship `control_plane/packs/**` inside the Agent artifact.
- Rotate signing keys through a managed release and revocation window.

