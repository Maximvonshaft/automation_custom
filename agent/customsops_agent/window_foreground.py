from __future__ import annotations


def assert_asycuda_foreground_window(window_title: str) -> None:
    normalized = window_title.upper()
    if "ASYCUDA" not in normalized:
        raise ValueError("ASYCUDA foreground window is not confirmed")

