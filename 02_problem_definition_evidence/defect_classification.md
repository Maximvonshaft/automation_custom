# Defect Classification

| Class | Description | Example |
|---|---|---|
| Functional | Feature does not work | Button click fails |
| UX Clarity | User cannot understand what to do | Technical labels, unclear empty state |
| Data Integrity | Incorrect or unsafe data mutation | Wrong status transition |
| Permission | Wrong user sees/does wrong thing | Agent sees admin config |
| Security | Secret/PII/auth risk | Token in localStorage |
| Reliability | Intermittent or fragile behavior | Missing retry/fallback |
| Observability | Failure cannot be diagnosed | No event/log/trace |
| Release | Change cannot be safely deployed or rolled back | No rollback path |
