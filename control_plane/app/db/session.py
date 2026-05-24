from __future__ import annotations

from control_plane.app.db.models import License, Machine


class InMemoryRegistry:
    def __init__(self) -> None:
        self.machines: dict[tuple[str, str], Machine] = {}
        self.licenses: dict[tuple[str, str], License] = {}


registry = InMemoryRegistry()

