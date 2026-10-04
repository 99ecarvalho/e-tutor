# Tests for memory cards, spreadsheet exports, history replay and quotes.
#
# Copyright (c) 2025-2026 Eduardo Correia <ecorreia@apliant.com.br>
#
# This file is part of E-Tutor. It is free software, licensed under the GNU
# Lesser General Public License v3.0 or later. See COPYING.LESSER and COPYING
# for details.
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import csv
import io
import json
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch
from urllib.parse import parse_qs, urlparse

from coaching import LearningStore, normalize_result
from memory_tools import dictionary_links, make_card, read_history, replay_result, spreadsheet_text
from test_coaching import OPTS, notebook_path, sample
import test_coaching
from quotes import QUOTE_BANK, quote_for


class MemoryTests(unittest.TestCase):
    def test_links_encode_terms_as_data(self):
        term = "rain check & coffee / tea?"
        for url in dictionary_links(term).values():
            self.assertEqual(parse_qs(urlparse(url).query)["q"], [term])
            self.assertEqual(urlparse(url).scheme, "https")

    def test_export_preserves_columns_portuguese_and_quotes(self):
        card = make_card("idiom", "rain check", "outra ocasião", 'She said, "Later."\nNext line', "informal")
        rows = list(csv.reader(io.StringIO(spreadsheet_text([card])), delimiter="\t"))
        self.assertEqual(len(rows), 2)
        self.assertEqual(len(rows[0]), len(rows[1]))
        self.assertEqual(rows[1][2], "outra ocasião")
        self.assertEqual(rows[1][3], 'She said, "Later." Next line')
        self.assertIn("oxfordlearnersdictionaries.com", rows[1][rows[0].index("Oxford lookup")])
        csv_rows = list(csv.reader(io.StringIO(spreadsheet_text([card], delimiter=","))))
        self.assertEqual(csv_rows, rows)

    def test_export_treats_formula_like_content_as_text(self):
        for prefix in ("=", "+", "-", "@"):
            text = spreadsheet_text([make_card("vocabulary", "  " + prefix + "test", "word")])
            cells = list(csv.reader(io.StringIO(text), delimiter="\t"))
            self.assertEqual(cells[1][0], "'" + prefix + "test")

    def test_save_senses_and_edit_preserve_review_progress(self):
        with notebook_path() as path:
            store = LearningStore(path)
            one = make_card("vocabulary", "fine", "bom")
            two = make_card("vocabulary", "fine", "multa")
            self.assertEqual(store.add([one, two, dict(one, term=" FINE ")]), 2)
            store.rate(two, True)
            self.assertEqual([c["stage"] for c in store.cards], [0, 1])
            store.update_notes(two, "My own example", "fine noun")
            loaded = LearningStore(path)
            self.assertEqual(loaded.cards[1]["stage"], 1)
            self.assertEqual(loaded.cards[1]["personal_notes"], "My own example")

    def test_history_skips_broken_lines_and_replays_legacy_response(self):
        with notebook_path() as path:
            entry = {"query": "Original", "model": "example", "response": "```json\n" + json.dumps(sample()) + "\n```"}
            Path(path).write_text(json.dumps(entry) + "\ninvalid\n[]\n", encoding="utf-8")
            entries, skipped = read_history(path)
            self.assertEqual(skipped, 2)
            result = replay_result(entries[0])
            self.assertEqual(result["learning"]["items"][0]["term"], "take a rain check")
            self.assertEqual(len(result["versions"]), 3)
            self.assertEqual(result["request_id"], "legacy-1")

    def test_full_snapshot_replays_focus_and_corrections(self):
        data = normalize_result(sample(), OPTS)
        data["quote"] = quote_for(2)
        data["request_options"] = {"resolved_focus": "persuasion"}
        data["truncated"] = True
        entry = {"id": "abc", "query": "Original", "result": data, "timestamp": "2026-10-04"}
        result = replay_result(entry)
        self.assertEqual(result["versions"], data["versions"])
        self.assertEqual(result["learning"], data["learning"])
        self.assertEqual(result["quote"], data["quote"])
        self.assertTrue(result["truncated"])
        self.assertEqual(result["request_options"]["resolved_focus"], "persuasion")
        with self.assertRaises(ValueError):
            replay_result(dict(entry, status="error", error="Unavailable"))

    def test_quote_rotation_and_reference_export(self):
        self.assertEqual(quote_for(len(QUOTE_BANK)), quote_for(0))
        self.assertEqual(len({quote_for(i)["id"] for i in range(len(QUOTE_BANK))}), len(QUOTE_BANK))
        quote = quote_for(2)
        self.assertNotIn("translation_pt", quote)
        card = make_card("quote", quote["text"], quote["application_en"], quote_author=quote["author"],
                         quote_work=quote["work"], reference_url=quote["source_url"])
        rows = list(csv.reader(io.StringIO(spreadsheet_text([card])), delimiter="\t"))
        self.assertEqual(rows[1][rows[0].index("Reference URL")], quote["source_url"])


class IntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        test_coaching.AppTests.setUpClass()
        cls.module = test_coaching.AppTests.module

    def test_api_writes_snapshot_and_failure_without_extra_requests(self):
        m = self.module
        api = m.APIClient.__new__(m.APIClient)
        api.client = MagicMock()
        api.endpoint = "test"
        api.unsupported = {}
        api._create = MagicMock(return_value=SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content=json.dumps(sample())), finish_reason="stop")], usage=None))
        with notebook_path() as path, patch.object(m, "API_LOG_FILE", path):
            result = api.get_rewrites("A draft", "example", 0.4, "test prompt", OPTS)
            entries, _ = read_history(path)
            self.assertEqual(entries[0]["result"], result)
            self.assertEqual(result["quote"], quote_for(0))
            self.assertEqual(replay_result(entries[0])["versions"], result["versions"])
            no_quote = api.get_rewrites("No quote", "example", 0.4, "test prompt", dict(OPTS, quote=False))
            self.assertNotIn("quote", no_quote)
            api._create.side_effect = RuntimeError("Provider unavailable")
            with self.assertRaises(RuntimeError):
                api.get_rewrites("Another draft", "example", 0.4, "test prompt", OPTS)
            entries, _ = read_history(path)
            self.assertEqual(len(entries), 3)
            self.assertEqual(entries[0]["status"], "error")

    def test_history_display_has_no_clipboard_or_usage_side_effects(self):
        m = self.module
        app = MagicMock()
        app.busy = False
        entry = {"query": "A draft", "result": sample(), "id": "abc"}
        m.AppGUI.load_history_entry(app, entry)
        app.show_result.assert_called_once()
        app.copy_to_clipboard.assert_not_called()
        app.session.add.assert_not_called()
        app.input_text.delete.assert_not_called()
        app.client.get_rewrites.assert_not_called()


if __name__ == "__main__":
    unittest.main()
