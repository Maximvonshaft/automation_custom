# Deployment Runbook

## Control Plane

1. Provision database.
2. Configure environment variables.
3. Generate Ed25519 signing key pair.
4. Store private key securely server-side.
5. Load Albania Pack server-side.
6. Start API service.
7. Run smoke test: health, license check, job compile, evidence upload.

## Local Agent

1. Install Agent on authorized workstation.
2. Register machine.
3. Confirm machine appears in Control Plane.
4. Fetch signed SafeBrake job.
5. Run in mock mode first.
6. Run controlled field test only under internal operator supervision.
