# Abuse / Misuse Cases

| Case | Control |
|---|---|
| Agent copied to another PC | machine binding rejects job |
| Job reused after expiry | expiry check rejects job |
| Local IT edits job plan | signature check rejects job |
| Operator tries Submit action | forbidden action policy rejects job |
| Tenant stops paying | license revoke / kill switch |
| Agent reverse-engineered | no complete Country Pack in binary |
| Evidence tampering | watermark + hashes + server upload |
