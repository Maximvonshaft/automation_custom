# Sequence Flows

## Job compilation

```text
Ops Manager → Control Plane: upload/input declaration data
Control Plane → Pack Loader: load Albania ASYCUDA Pack
Control Plane → Compiler: compile minimal job steps
Compiler → Signer: sign job plan
Control Plane → Job Store: persist signed job
Operator Agent → Control Plane: fetch assigned job
```

## Local execution

```text
Agent starts
→ reads signed job plan
→ validates signature
→ validates machine/tenant/expiry/mode
→ locks ASYCUDA foreground window
→ executes allowed action grammar
→ captures screenshots and ledger
→ builds evidence bundle
→ uploads or stores evidence
```

## SafeBrake run

```text
Fill validated fields
→ intentionally omit configured SafeBrake required field
→ click line Store
→ ASYCUDA native validation blocks success
→ capture error screenshot
→ produce evidence bundle
```
