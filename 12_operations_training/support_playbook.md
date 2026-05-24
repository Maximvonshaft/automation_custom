# Support Playbook

## Common failures

| Symptom | Likely cause | Action |
|---|---|---|
| Invalid signature | job edited or corrupt | regenerate job |
| Wrong machine | job issued to another machine | register correct machine |
| Expired job | operator waited too long | reissue job |
| Forbidden action rejected | pack/compiler bug | escalate to engineering |
| Evidence upload failed | network issue | export local bundle and retry |
| ASYCUDA foreground mismatch | operator changed window | restart run from clean state |
