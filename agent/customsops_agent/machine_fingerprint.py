from __future__ import annotations

import hashlib
import platform
import uuid


def derive_machine_id(salt: str = "customsops-v4") -> str:
    raw = f"{platform.node()}|{platform.system()}|{uuid.getnode()}|{salt}".encode()
    return "machine_" + hashlib.sha256(raw).hexdigest()[:16]

