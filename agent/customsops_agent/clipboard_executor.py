from __future__ import annotations


class ClipboardExecutor:
    def paste_value(self, value: str) -> str:
        if "\n" in value or "\r" in value:
            raise ValueError("Multiline clipboard values are not allowed")
        return value

