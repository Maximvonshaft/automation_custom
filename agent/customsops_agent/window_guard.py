from __future__ import annotations


def assert_operator_confirmed_foreground_window(window_title: str) -> None:
    if "ASYCUDA" not in window_title.upper():
        raise ValueError("Foreground window is not an operator-confirmed ASYCUDA window")

