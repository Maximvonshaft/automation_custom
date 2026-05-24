# Rollback Plan

If v4.1 introduces instability:

1. Stop external packaging.
2. Disable any v4.1 job issuance in Control Plane.
3. Keep v4.0 main as controlled-runtime architecture baseline.
4. Continue using v3.1.1 SafeBrake only for internal field validation.
5. Revoke affected test job plans and machine leases.
6. Preserve evidence bundles for incident review.
