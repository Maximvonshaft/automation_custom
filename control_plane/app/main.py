from __future__ import annotations

from fastapi import FastAPI

from control_plane.app.api import admin, evidence, health, jobs, licenses, machines, manifests

app = FastAPI(title="CustomsOps Control Plane", version="4.0.0")
app.include_router(health.router)
app.include_router(machines.router)
app.include_router(licenses.router)
app.include_router(jobs.router)
app.include_router(evidence.router)
app.include_router(admin.router)
app.include_router(manifests.router)
