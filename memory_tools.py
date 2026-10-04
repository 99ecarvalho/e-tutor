"""Portable learning cards, spreadsheet exports, and backward-compatible JSONL history."""

import csv
import datetime as dt
import io
import json
import re
from urllib.parse import urlencode

from coaching import dict_list, normalize_result
from quotes import saved_quote


def dictionary_links(term):
    """Search URLs, never invented entry URLs or AI-attributed dictionary definitions."""
    return {
        "Oxford": "https://www.oxfordlearnersdictionaries.com/search/english/?" + urlencode({"q": term}),
        "Cambridge": "https://dictionary.cambridge.org/search/direct/?" + urlencode({"dataset": "english", "q": term}),
    }


def make_card(kind, term, meaning="", example="", usage="", source="", result=None, **extra):
    result = result or {}
    return {"kind": kind, "term": term.strip(), "meaning_pt": meaning, "example": example, "usage": usage,
            "source_text": source, "request_id": result.get("request_id", ""),
            "request_timestamp": result.get("timestamp", ""), "saved_at": dt.datetime.now().isoformat(),
            "lookup_term": term.strip(), "personal_notes": "", **extra}


EXPORT_FIELDS = [
    ("term", "Term / correction"), ("kind", "Type"), ("meaning_pt", "Meaning / explanation"),
    ("example", "Example / corrected text"), ("usage", "Usage notes"), ("wrong", "Original wording"),
    ("personal_notes", "My notes"), ("source_text", "Source request"), ("saved_at", "Saved at"),
    ("request_timestamp", "Request date"), ("due", "Review due"), ("oxford", "Oxford lookup"),
    ("cambridge", "Cambridge lookup"),
    ("quote_author", "Quote author"), ("quote_work", "Quote source"), ("reference_url", "Reference URL"),
]


def spreadsheet_text(cards, delimiter="\t"):
    """One row per card; normalize cell newlines and neutralize spreadsheet formulas."""
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, delimiter=delimiter, lineterminator="\n")
    writer.writerow([label for _, label in EXPORT_FIELDS])
    for card in cards:
        links = dictionary_links(card.get("lookup_term") or card["term"])
        values = dict(card, oxford=links["Oxford"], cambridge=links["Cambridge"])
        row = []
        for key, _ in EXPORT_FIELDS:
            value = " ".join(str(values.get(key, "")).split())
            if value.startswith(("=", "+", "-", "@")):
                value = "'" + value
            row.append(value)
        writer.writerow(row)
    return stream.getvalue()


def read_history(path):
    """Skip broken records individually; never rewrite or discard the source log."""
    entries, skipped = [], 0
    try:
        with open(path, encoding="utf-8") as stream:
            for number, line in enumerate(stream, 1):
                if not line.strip():
                    continue
                try:
                    entry = json.loads(line)
                    if not isinstance(entry, dict) or not isinstance(entry.get("query"), str):
                        raise ValueError("Invalid history record")
                    if not isinstance(entry.get("id"), str) or not entry["id"]:
                        entry["id"] = f"legacy-{number}"
                    for key in ("timestamp", "model", "status"):
                        if not isinstance(entry.get(key, ""), str):
                            entry[key] = ""
                    entries.append(entry)
                except ValueError:
                    skipped += 1
    except FileNotFoundError:
        pass
    return list(reversed(entries)), skipped


def replay_result(entry):
    """Replay new snapshots and older raw-response records without a model call."""
    if entry.get("status") == "error":
        raise ValueError(entry.get("error") or "This request failed.")
    data = entry.get("result")
    if not isinstance(data, dict):
        content = entry.get("response", "")
        if not isinstance(content, str):
            raise ValueError("No saved response in this record.")
        candidates = [content]
        match = re.search(r"\{[\s\S]*\}", content)
        if match:
            candidates.append(match.group(0))
        data = None
        for candidate in candidates:
            try:
                decoded = json.loads(candidate)
                if isinstance(decoded, dict):
                    data = decoded
                    break
            except ValueError:
                pass
        if data is None:
            raise ValueError("This older response is not valid JSON. Its raw response is available below.")
    levels = list(dict.fromkeys(v["level"] for v in dict_list(data.get("versions")) if isinstance(v.get("level"), str)))
    counts = [sum(v.get("level") == level for v in dict_list(data.get("versions"))) for level in levels]
    # Restore what was returned, independently of today's controls.
    opts = {"levels": levels, "variations": max(counts, default=1), "grammar_notes": True,
            "vocabulary": True, "learning_depth": "deep", "culture_notes": True}
    result = normalize_result(data, opts)
    quote = saved_quote(data.get("quote"))
    if quote:
        result["quote"] = quote
    request_options = data.get("request_options", entry.get("options", entry))
    result.update(request_id=entry.get("id", ""), timestamp=entry.get("timestamp", ""),
                  request_options=request_options if isinstance(request_options, dict) else {},
                  truncated=bool(data.get("truncated")), usage=data.get("usage"))
    return result
