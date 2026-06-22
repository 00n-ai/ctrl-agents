from __future__ import annotations

import re
from typing import Any


def parse_labeled_text(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in text.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip().lower().replace(" ", "_")
        value = value.strip()
        if key:
            out[key] = value
    return out


def extract_json_block(text: str) -> dict[str, Any] | None:
    match = re.search(r"```json\s*(\{.*?\})\s*```", text, re.S)
    if not match:
        return None
    import json

    return json.loads(match.group(1))
