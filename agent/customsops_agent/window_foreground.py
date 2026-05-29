from __future__ import annotations

from collections.abc import Callable


def get_active_window_title() -> str:
    try:
        import pygetwindow
    except ImportError as exc:
        raise RuntimeError("pygetwindow is required for real GUI foreground verification") from exc

    active_window = pygetwindow.getActiveWindow()
    if active_window is None:
        return ""
    return str(getattr(active_window, "title", "") or "")


def assert_asycuda_foreground_window(
    expected_window_title: str,
    *,
    active_window_title_provider: Callable[[], str] | None = None,
) -> str:
    expected = expected_window_title.upper()
    if "ASYCUDA" not in expected:
        raise ValueError("Foreground window title expectation must include ASYCUDA")

    provider = active_window_title_provider or get_active_window_title
    active_window_title = provider()
    normalized_active = active_window_title.upper()
    if "ASYCUDA" not in normalized_active:
        raise ValueError(
            "ASYCUDA foreground window is not confirmed; "
            f"active window title was: {active_window_title!r}"
        )
    return active_window_title
