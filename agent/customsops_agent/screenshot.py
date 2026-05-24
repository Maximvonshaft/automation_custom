from __future__ import annotations

from pathlib import Path

from shared.watermark import write_watermarked_text_artifact


def capture_mock_screenshot(path: Path, watermark: str) -> Path:
    return write_watermarked_text_artifact(path, "mock screenshot placeholder", watermark)

