# License and Kill Switch Policy

License dimensions:

- tenant
- machine
- country pack
- allowed modes
- expiry
- daily run limit
- offline lease limit

Kill switch can revoke:

- tenant
- machine
- pack version
- agent version
- individual job

Agent must check license at startup and before executing jobs when online. Offline jobs must be short-lived and signed.
