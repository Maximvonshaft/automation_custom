# Secrets Management Policy

## Server-side secrets

- Ed25519 private signing key
- database credentials
- API signing secrets if used

Store in environment variables or a secret manager. Do not commit.

## Client-side allowed material

- Ed25519 public key
- tenant-neutral agent config
- machine installation ID

## Forbidden on client

- private signing key
- complete Country Pack
- business mapping rules
- credential material
