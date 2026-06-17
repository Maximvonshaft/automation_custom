# Secrets Management Policy

- Signing private key stays server-side only.
- Agent embeds only public verification key.
- Real country packs must not be committed to public or agent code paths.
- Production tenant credentials, machine license secrets, and pack secrets must be stored in a secret manager, not `.env` committed files.
- Job plans are short-lived and signed.
- Evidence bundles may contain screenshots; retention policy must be defined before external deployment.
