from __future__ import annotations

import re

from .models import NetworkGraph


IDENT = r"[A-Za-z][A-Za-z0-9_-]*"
NUMBER = r"\d+(?:[.,]\d+)?"
PATTERNS = {
    "bus": re.compile(rf"Szyna (?P<id>{IDENT}) ma napięcie (?P<vn_kv>{NUMBER}) kV", re.I),
    "line": re.compile(
        rf"Szyna (?P<from_bus>{IDENT}) jest połączona linią (?P<id>{IDENT}) "
        rf"z szyną (?P<to_bus>{IDENT})(?: o długości (?P<length_km>{NUMBER}) km)?",
        re.I,
    ),
    "load": re.compile(
        rf"Do szyny (?P<bus>{IDENT}) podłączono odbiór (?P<id>{IDENT}) "
        rf"o mocy (?P<p_mw>{NUMBER}) MW",
        re.I,
    ),
}


def parse_description(text: str) -> NetworkGraph:
    """Odczytuje trzy jawnie zdefiniowane wzorce zdań; nie interpretuje swobodnego tekstu."""
    sentences = [part.strip().rstrip(".!?").strip() for part in re.split(r"(?<=[.!?])\s+|\n+", text.strip())]
    sentences = [part for part in sentences if part]
    if not sentences:
        raise ValueError("Opis jest pusty.")

    data: dict[str, list[dict]] = {"buses": [], "lines": [], "loads": []}
    destinations = {"bus": "buses", "line": "lines", "load": "loads"}
    for sentence in sentences:
        for kind, pattern in PATTERNS.items():
            match = pattern.fullmatch(sentence)
            if match:
                record = {key: value.replace(",", ".") if key in {"vn_kv", "length_km", "p_mw"} and value else value
                          for key, value in match.groupdict().items() if value is not None}
                data[destinations[kind]].append(record)
                break
        else:
            raise ValueError(f"Nie rozpoznano zdania: {sentence}")
    return NetworkGraph.model_validate(data)
