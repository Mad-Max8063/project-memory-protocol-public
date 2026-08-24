"""Dependency-free slug normalization for the PMP handoff demo."""

from __future__ import annotations

import re
import unicodedata


def slugify(value: str) -> str:
    """Return an ASCII slug using the demo's NFKD-decomposable scope."""
    normalized = unicodedata.normalize("NFKD", value.strip().lower())
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", ascii_value).strip("-")
