# Copyright (c) 2025-2026 Eduardo Correia <ecorreia@apliant.com.br>
#
# This file is part of E-Tutor. It is free software, licensed under the GNU
# Lesser General Public License v3.0 or later. See COPYING.LESSER and COPYING
# for details.
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Learning prompts, defensive response parsing, and local recall scheduling."""

import datetime as dt
import json
import os
import uuid

DEPTHS = [
    {"id": "quick", "label": "Daily bite"},
    {"id": "deep", "label": "Deep dive"},
    {"id": "off", "label": "Rewrites only"},
]
FOCUSES = [
    {"id": "mixed", "label": "Random mix"},
    {"id": "executive", "label": "Executive communication"},
    {"id": "persuasion", "label": "NLP-inspired persuasion"},
]
DOMAINS = ["everyday life", "arts and literature", "civic life", "relationships and social plans",
           "food and hospitality", "sports and popular expressions"]


def learning_prompt(opts):
    depth = opts.get("learning_depth", "quick")
    if depth == "off":
        return '\n4. learning: null. Do not add lessons or practice.'
    count = 3 if depth == "deep" else 1
    domain = DOMAINS[opts.get("lesson_index", 0) % len(DOMAINS)]
    recent = json.dumps(opts.get("recent_terms", [])[-40:], ensure_ascii=False)
    language = "Brazilian Portuguese" if opts.get("explain_language") == "pt" else "English"
    focus = opts.get("resolved_focus", "executive")
    focus_instruction = (
        "NLP-inspired persuasion practice: teach one transparent technique such as reframing a problem as a shared "
        "outcome, perspective-taking, matching the listener's terminology, or asking a clarifying question. "
        "Show how it applies to THIS message. Separate any proposed question from the rewrite. "
        "Respect the listener's freedom to disagree; avoid covert manipulation, invented motives, eye-accessing cues, "
        "claims about learning styles, or claims that NLP has established neurological effects."
        if focus == "persuasion" else
        "Executive communication practice: teach one habit such as conclusion first, recommendation plus rationale, "
        "separating facts from assumptions, a clear ask, or concise disagreement. Apply it to THIS message."
    )
    return f"""
4. learning: a short lesson for a self-taught Brazilian C2 professional planning US interviews and life in the US.
   Give exactly {count} vocabulary/idiom item(s) if vocabulary is enabled ({opts.get('vocabulary', True)}), otherwise none.
   Teach nuanced collocations, register, or nontechnical vocabulary; do not assume which words this individual knows.
   Prefer one useful stretch over rare words. Meaning_pt MUST be a Brazilian Portuguese translation even when explanations are in English.
   Examples must be NEW, generic English sentences without names, client details, or facts taken from the user's work.
   Usage explains register, a common trap, or when NOT to use the expression in {language}.
   Avoid recently taught terms: {recent}.
   Add one compact culture item if cultural notes are enabled ({opts.get('culture_notes', True)}), otherwise none.
   Rotate beyond tech: this request's domain is {domain}. Explain a stable, widely encountered US reference or convention,
   its meaning in Portuguese, a generic example, and where it varies. No claim that all educated Americans know it.
   No invented origins, quotes, stereotypes, current news, or unverified trivia. If unsure, omit the culture item.
   Communication: one concrete observation about THIS text, plus a reusable habit in {language} (max 45 words total).
   Focus for this request: {focus_instruction}
   Train bottom-line-first framing, audience awareness, calibrated certainty, clear asks, listening, and tactful disagreement.
   If discussing NLP, use transparent communication exercises; never claim mind control, brain reprogramming, or guaranteed persuasion.
   Spoken contexts: include a useful pause/stress or short spoken rehearsal cue, without pretending to diagnose pronunciation from text.
   Do not add drills, practice tasks, or quotations; the app supplies its own sourced quotation separately.
   Daily bite: keep the entire learning section under 180 words. Deep dive: under 330 words.
   JSON field to ADD to the object:
   "learning": {{"items": [{{"kind": "vocabulary|idiom|culture", "term": "...", "meaning_pt": "...", "example": "...", "usage": "..."}}],
                "communication": "..."}}
"""


def clean_string(value, limit=12000):
    return value[:limit].strip() if isinstance(value, str) else ""


def dict_list(value):
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def normalize_result(data, opts):
    """Never let nulls, wrong types, or unsolicited styles reach the GUI/clipboard."""
    if not isinstance(data, dict):
        raise ValueError("The response was not a JSON object. Please try again.")
    result = {"corrected": clean_string(data.get("corrected")), "notes": [], "versions": []}
    if opts.get("grammar_notes"):
        result["notes"] = [{key: clean_string(n.get(key)) for key in ("wrong", "right", "why")}
                           for n in dict_list(data.get("notes"))[:6]]
    versions = dict_list(data.get("versions"))
    for level in opts.get("levels", []):
        matching = [v for v in versions if v.get("level") == level and clean_string(v.get("text"))]
        for v in matching[:opts.get("variations", 1)]:
            result["versions"].append({"level": level, "text": clean_string(v.get("text")),
                "vocabulary": [{"term": clean_string(i.get("term")), "meaning": clean_string(i.get("meaning"))}
                               for i in dict_list(v.get("vocabulary"))[:2]] if opts.get("vocabulary") else []})
    lesson = data.get("learning")
    if opts.get("learning_depth", "quick") != "off" and isinstance(lesson, dict):
        items, vocab_count, culture_count = [], 0, 0
        for item in dict_list(lesson.get("items")):
            kind = item.get("kind")
            if kind in ("vocabulary", "idiom"):
                if not opts.get("vocabulary", True) or vocab_count >= (3 if opts.get("learning_depth") == "deep" else 1):
                    continue
                vocab_count += 1
            elif kind == "culture":
                if not opts.get("culture_notes", True) or culture_count >= 1:
                    continue
                culture_count += 1
            else:
                continue
            card = {k: clean_string(item.get(k), 1500) for k in ("term", "meaning_pt", "example", "usage")}
            if all(card[k] for k in ("term", "meaning_pt", "example")):
                items.append(dict(card, kind=kind))
        result["learning"] = {"items": items, "communication": clean_string(lesson.get("communication"), 2500)}
    if not result["corrected"] and not result["versions"]:
        raise ValueError("The response contained no usable correction or rewrite. Please try again.")
    return result


class LearningStore:
    """Manual lesson collection; atomic writes and explicit self-rated retrieval."""

    def __init__(self, path):
        self.path = path
        self.cards = []
        self.load_error = None
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list) or any(not self.valid_card(c) for c in data):
                raise ValueError("Invalid learning notebook format")
            self.cards = data
        except FileNotFoundError:
            pass
        except (OSError, ValueError) as error:
            # Preserve damaged/unreadable files rather than silently overwriting them.
            self.load_error = str(error)

    @staticmethod
    def valid_card(card):
        if not isinstance(card, dict) or not all(isinstance(card.get(k), str) for k in
                ("term", "meaning_pt", "example", "usage", "kind", "due")):
            return False
        try:
            dt.date.fromisoformat(card["due"])
        except ValueError:
            return False
        return type(card.get("stage")) is int and 0 <= card["stage"] <= 4

    def _save(self, cards):
        if self.load_error:
            raise OSError("Notebook could not be read; preserved original file: " + self.load_error)
        temp = self.path + ".tmp"
        with open(temp, "w", encoding="utf-8") as f:
            json.dump(cards, f, ensure_ascii=False, indent=2)
        os.replace(temp, self.path)
        self.cards = cards

    def add(self, items, today=None):
        today = today or dt.date.today()
        cards = [dict(c) for c in self.cards]
        known = {self.identity(c) for c in cards}
        for item in items:
            if self.identity(item) not in known:
                cards.append(dict(item, id=uuid.uuid4().hex, stage=0, due=today.isoformat()))
                known.add(self.identity(item))
        added = len(cards) - len(self.cards)
        self._save(cards)
        return added

    @staticmethod
    def identity(card):
        # Keep different senses or item types while ignoring case/spacing differences.
        return tuple(" ".join(str(card.get(k, "")).casefold().split()) for k in ("kind", "term", "meaning_pt"))

    def contains(self, item):
        return any(self.identity(c) == self.identity(item) for c in self.cards)

    def update_notes(self, item, notes, lookup_term):
        cards = [dict(c) for c in self.cards]
        card = next(c for c in cards if self.identity(c) == self.identity(item))
        card.update(personal_notes=notes, lookup_term=lookup_term.strip() or card["term"])
        self._save(cards)

    def due(self, today=None):
        today = (today or dt.date.today()).isoformat()
        return sorted((c for c in self.cards if c["due"] <= today), key=lambda c: c["due"])

    def rate(self, term, remembered, today=None):
        today = today or dt.date.today()
        cards = [dict(c) for c in self.cards]
        card = next(c for c in cards if (self.identity(c) == self.identity(term) if isinstance(term, dict) else c["term"] == term))
        intervals = (1, 3, 7, 14, 30)
        days = intervals[card["stage"]] if remembered else 1
        card["stage"] = min(card["stage"] + 1, 4) if remembered else 0
        card["due"] = (today + dt.timedelta(days=days)).isoformat()
        self._save(cards)
