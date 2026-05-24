# Security Review Checklist

- [ ] Private signing key is server-side only.
- [ ] Agent embeds only public key.
- [ ] Agent rejects unsigned jobs.
- [ ] Agent rejects expired jobs.
- [ ] Agent rejects wrong-machine jobs.
- [ ] Agent rejects forbidden actions.
- [ ] Country Pack is not bundled into Agent.
- [ ] Evidence includes watermarks.
- [ ] Logs do not contain ASYCUDA passwords or credentials.
- [ ] Submit/Register/Payment actions are blocked in v4.0.
- [ ] License revoke path is tested.
- [ ] CI includes tests for negative security cases.
