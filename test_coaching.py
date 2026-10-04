import datetime as dt
import importlib.util
import json
from pathlib import Path
from contextlib import contextmanager
import unittest
from unittest.mock import MagicMock, patch
import uuid

from coaching import LearningStore, learning_prompt, normalize_result
from quotes import quote_for


@contextmanager
def notebook_path():
    # Individual files inherit workspace permissions (Windows temp directories may not).
    path = Path(__file__).resolve().parent / (".test-notebook-" + uuid.uuid4().hex + ".json")
    try:
        yield str(path)
    finally:
        for candidate in (path, Path(str(path) + ".tmp")):
            if candidate.exists():
                candidate.unlink()


def sample():
    return {"corrected": "I might need another day.", "notes": None,
            "versions": [{"level": "executive", "text": "I may need one more day.", "vocabulary": None},
                         {"level": "native", "text": "I might need another day."},
                         {"level": "unknown", "text": "Ignore this."}],
            "learning": {"items": [
                {"kind": "idiom", "term": "take a rain check", "meaning_pt": "deixar para outra ocasião",
                 "example": "Can I take a rain check on dinner?", "usage": "Informal; declining an invitation for now."}],
                "communication": "Keep uncertainty when the timing is not confirmed.",
                "drill": {"prompt": "Decline an invitation while leaving the door open.",
                          "answer": "Could I take a rain check?"}}}


OPTS = {"levels": ["native", "executive"], "variations": 1, "vocabulary": True,
        "grammar_notes": True, "learning_depth": "quick", "culture_notes": True}


class ResponseTests(unittest.TestCase):
    def test_types_and_requested_order(self):
        result = normalize_result(sample(), OPTS)
        self.assertEqual([v["level"] for v in result["versions"]], OPTS["levels"])
        self.assertEqual(result["notes"], [])
        self.assertEqual(result["versions"][1]["vocabulary"], [])

    def test_invalid_response_never_becomes_copyable(self):
        for data in (None, [], {"corrected": ["bad"], "versions": None}, {"versions": "bad"}):
            with self.assertRaises(ValueError):
                normalize_result(data, OPTS)

    def test_controls_enforced_locally(self):
        result = normalize_result(sample(), dict(OPTS, learning_depth="off", levels=[], grammar_notes=False))
        self.assertNotIn("learning", result)
        self.assertEqual(result["versions"], [])
        result = normalize_result(sample(), dict(OPTS, vocabulary=False))
        self.assertEqual(result["learning"]["items"], [])

    def test_bad_lesson_fields_and_item_budget(self):
        data = sample()
        data["learning"]["items"] *= 5
        data["learning"]["drill"] = "bad"
        result = normalize_result(data, OPTS)
        self.assertEqual(len(result["learning"]["items"]), 1)
        self.assertNotIn("drill", result["learning"])

    def test_focus_translation_and_recall_in_prompt(self):
        prompt = learning_prompt(dict(OPTS, explain_language="en", resolved_focus="persuasion"))
        self.assertIn("NLP-inspired persuasion practice", prompt)
        self.assertIn("Brazilian Portuguese translation even when explanations are in English", prompt)
        self.assertNotIn('"drill"', prompt)
        self.assertNotIn("15-second", prompt)
        self.assertIn("Executive communication practice", learning_prompt(dict(OPTS, resolved_focus="executive")))


class NotebookTests(unittest.TestCase):
    def setUp(self):
        context = notebook_path()
        self.path = context.__enter__()
        self.addCleanup(context.__exit__, None, None, None)
        self.store = LearningStore(self.path)
        self.today = dt.date(2026, 10, 4)
        self.items = sample()["learning"]["items"]

    def test_roundtrip_dedup_and_due_dates(self):
        self.assertEqual(self.store.add(self.items, self.today), 1)
        self.assertEqual(self.store.add([dict(self.items[0], term="TAKE A RAIN CHECK")], self.today), 0)
        store = LearningStore(self.path)
        self.assertEqual(len(store.due(self.today)), 1)
        store.rate(self.items[0]["term"], True, self.today)
        self.assertEqual(store.due(self.today), [])
        self.assertEqual(store.cards[0]["due"], "2026-10-05")
        store.rate(self.items[0]["term"], True, self.today + dt.timedelta(days=1))
        self.assertEqual(store.cards[0]["due"], "2026-10-08")
        store.rate(self.items[0]["term"], False, self.today + dt.timedelta(days=4))
        self.assertEqual(store.cards[0]["stage"], 0)
        self.assertEqual(store.cards[0]["due"], "2026-10-09")

    def test_damaged_file_is_preserved(self):
        Path(self.path).write_text('{"broken":true}', encoding="utf-8")
        store = LearningStore(self.path)
        self.assertIsNotNone(store.load_error)
        with self.assertRaises(OSError):
            store.add(self.items)
        self.assertEqual(Path(self.path).read_text(encoding="utf-8"), '{"broken":true}')

    def test_failed_write_does_not_change_memory(self):
        with patch("coaching.os.replace", side_effect=OSError("disk error")):
            with self.assertRaises(OSError):
                self.store.add(self.items)
        self.assertEqual(self.store.cards, [])


class AppTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("tutor", Path(__file__).with_name("e-tutor.py"))
        cls.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.module)

    def test_new_draft_survives_response_and_copy_is_opt_in(self):
        app = MagicMock()
        app.current_model = "test"
        app.recent_terms = []
        app.lesson_index = 0
        app.popup_enabled = False
        app.input_text.get.return_value = "My next draft"
        result = normalize_result(sample(), OPTS)
        result["usage"] = {"known": False, "rewrites": 2}
        result["request_options"] = {"auto_copy": False}
        self.module.AppGUI._on_rewrites_ready(app, "I might need another day.", result, True)
        app.input_text.delete.assert_not_called()
        app.copy_to_clipboard.assert_not_called()
        self.assertEqual(app.latest_copy, "I might need another day.")

    def test_parser_rejects_prose_but_accepts_fenced_json(self):
        self.assertEqual(self.module.extract_json('```json\n{"corrected":"OK"}\n```'), {"corrected": "OK"})
        with self.assertRaises(ValueError):
            self.module.extract_json("Sorry, cannot answer.")

    def test_gui_build_render_and_presets(self):
        m = self.module
        app = m.AppGUI.__new__(m.AppGUI)
        app.prefs = dict(m.ConfigManager.DEFAULTS)
        app.current_model = m.DEFAULT_MODEL
        app.current_temperature = 0.4
        app.custom_models = []
        app.popup_enabled = True
        app.theme = "dark"
        app.session = m.SessionUsage()
        app.copy_tag_count = 0
        app.last_lesson = None
        app.review_window = None
        app.busy = False
        with notebook_path() as path:
            app.notebook = LearningStore(path)
            with patch.object(m.ConfigManager, "save"), patch.object(m.messagebox, "showerror", side_effect=AssertionError("Unexpected error dialog")):
                app._build_gui()
                app.root.withdraw()
                try:
                    app.apply_theme("dark")
                    app.apply_theme("light")
                    app.apply_preset(m.PRESETS[0][1])
                    self.assertEqual(app.get_options()["levels"], ["native", "executive"])
                    self.assertTrue(app.get_options()["quote"])
                    app.quote_var.set(False)
                    app._on_options_changed()
                    self.assertFalse(app.get_options()["quote"])
                    app.quote_var.set(True)
                    result = normalize_result(sample(), OPTS)
                    result["quote"] = quote_for(0)
                    result["notes"] = [{"wrong": "depends of", "right": "depends on", "why": "Use on after depend."}]
                    app.show_result("I might need another day.", result, result["versions"])
                    self.assertIn("Make it yours", app.output_text.get("1.0", "end"))
                    self.assertIn("[Oxford]", app.output_text.get("1.0", "end"))
                    self.assertIn("[Source]", app.output_text.get("1.0", "end"))
                    self.assertNotIn("15-second", app.output_text.get("1.0", "end"))
                    self.assertFalse(hasattr(app, "practice_button"))
                    def check_link_spaces():
                        positions = app.output_text.tag_ranges("action")
                        for start, end in zip(positions[::2], positions[1::2]):
                            label = app.output_text.get(start, end)
                            self.assertEqual(label, label.strip())
                            self.assertNotIn("action", app.output_text.tag_names(f"{start}-1c"))
                    check_link_spaces()
                    grammar_card = next(card for _, card in app.save_actions if card["kind"] == "correction")
                    app.save_memory_item(grammar_card)
                    app.save_memory_item(grammar_card)
                    self.assertEqual(len(app.notebook.cards), 1)
                    self.assertEqual(app.notebook.cards[0]["source_text"], "I might need another day.")
                    app.last_lesson = result["learning"]
                    app.save_lesson()
                    self.assertIn("[Saved]", app.output_text.get("1.0", "end"))
                    check_link_spaces()
                    app.open_memory()
                    library = app.library_windows["memory"]
                    library.window.withdraw()
                    library.rows.selection_set(0)
                    library.select()
                    with patch.object(app, "copy_to_clipboard") as copy:
                        library.copy_selected()
                        self.assertIn("take a rain check", copy.call_args.args[0])
                    library.notes.insert("1.0", "A useful expression")
                    library.save_notes()
                    self.assertEqual(app.notebook.cards[1]["personal_notes"], "A useful expression")
                    app.load_history_entry({"query": "Earlier draft", "result": result, "id": "earlier"})
                    self.assertEqual(app.current_source, "Earlier draft")
                    with notebook_path() as history_path, patch.object(m, "API_LOG_FILE", history_path):
                        Path(history_path).write_text(json.dumps({"query": "From history list", "result": result}) + "\n", encoding="utf-8")
                        app.open_history()
                        history = app.library_windows["history"]
                        history.window.withdraw()
                        history.rows.selection_set(0)
                        history.select()
                        self.assertEqual(app.current_source, "From history list")
                    app.open_review()
                    app.review_window.withdraw()
                    app.root.update_idletasks()
                    self.assertEqual(len(app.notebook.due()), 2)
                    quote_card = next(card for _, card in app.save_actions if card["kind"] == "quote")
                    app.save_memory_item(quote_card)
                    self.assertEqual(app.notebook.cards[-1]["reference_url"], result["quote"]["source_url"])
                    app.apply_preset(m.PRESETS[-1][1])
                    self.assertEqual(app.get_options()["learning_depth"], "off")
                    app.clear_output()
                    self.assertEqual(app.latest_copy, "")
                finally:
                    app.root.destroy()


if __name__ == "__main__":
    unittest.main()
