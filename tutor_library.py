# Copyright (c) 2025-2026 Eduardo Correia <ecorreia@apliant.com.br>
#
# This file is part of E-Tutor. It is free software, licensed under the GNU
# Lesser General Public License v3.0 or later. See COPYING.LESSER and COPYING
# for details.
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Memory and request-history windows. Browsing and export never call the model."""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import webbrowser

from memory_tools import dictionary_links, read_history, spreadsheet_text


class LibraryWindow:
    def __init__(self, app, history_path, palette, mode="memory"):
        self.app, self.history_path, self.mode = app, history_path, mode
        self.entries, self.visible = [], []
        self.window = win = tk.Toplevel(app.root)
        win.title("Saved memory · browse and export" if mode == "memory" else "Request history · click to restore")
        win.geometry("1000x720")
        win.minsize(780, 560)
        win.configure(bg=palette["bg"])
        self.palette = palette
        top = self.frame(win)
        top.pack(fill=tk.X, padx=12, pady=10)
        self.label(top, "Search:").pack(side=tk.LEFT)
        self.search = tk.StringVar()
        search = tk.Entry(top, textvariable=self.search, bg=palette["field_bg"], fg=palette["fg"],
                          insertbackground=palette["fg"])
        search.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=8)
        self.button(top, "Refresh", self.refresh).pack(side=tk.LEFT)
        self.search.trace_add("write", lambda *_: self.filter())

        listing = self.frame(win)
        listing.pack(fill=tk.BOTH, expand=True, padx=12)
        self.rows = tk.Listbox(listing, selectmode=tk.EXTENDED if mode == "memory" else tk.BROWSE,
                               exportselection=False, height=10, font=("Segoe UI", 11),
                               bg=palette["field_bg"], fg=palette["fg"], selectbackground=palette["select_bg"])
        scroll = tk.Scrollbar(listing, command=self.rows.yview)
        self.rows.config(yscrollcommand=scroll.set)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.rows.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.rows.bind("<<ListboxSelect>>", self.select)
        self.details = scrolledtext.ScrolledText(win, height=9, wrap=tk.WORD, font=("Segoe UI", 10),
                                                bg=palette["field_bg"], fg=palette["fg"])
        self.details.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)
        self.details.config(state=tk.DISABLED)
        self.lookup = tk.StringVar()
        if mode == "memory":
            references = self.frame(win)
            references.pack(fill=tk.X, padx=12)
            self.label(references, "Dictionary lookup:").pack(side=tk.LEFT)
            tk.Entry(references, textvariable=self.lookup, bg=palette["field_bg"], fg=palette["fg"],
                     insertbackground=palette["fg"]).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=8)
            for provider in ("Oxford", "Cambridge"):
                self.button(references, provider, lambda p=provider: self.open_dictionary(p)).pack(side=tk.LEFT, padx=3)
            self.reference_button = self.button(references, "Quote source", self.open_reference)
            self.reference_button.pack(side=tk.LEFT, padx=3)
            self.reference_button.config(state=tk.DISABLED)
            notes_row = self.frame(win)
            notes_row.pack(fill=tk.X, padx=12, pady=6)
            self.label(notes_row, "My notes:").pack(side=tk.LEFT)
            self.notes = tk.Text(notes_row, height=2, wrap=tk.WORD, bg=palette["field_bg"], fg=palette["fg"],
                                 insertbackground=palette["fg"])
            self.notes.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=8)
            self.button(notes_row, "Save notes", self.save_notes).pack(side=tk.LEFT)
        actions = self.frame(win)
        actions.pack(fill=tk.X, padx=12, pady=6)
        if mode == "memory":
            for label, callback in (("Copy selected rows", self.copy_selected), ("Copy filtered list", self.copy_filtered),
                                    ("Export CSV…", self.export_csv), ("Open source request", self.open_source),
                                    ("Practice due cards", app.open_review)):
                self.button(actions, label, callback).pack(side=tk.LEFT, padx=(0, 6))
        else:
            self.label(actions, "Selecting a request restores its result in the main window. No API call or clipboard change.").pack(anchor="w")
        self.status = self.label(win, "")
        self.status.pack(fill=tk.X, padx=12, pady=(0, 10))
        self.refresh()

    def frame(self, parent):
        return tk.Frame(parent, bg=self.palette["bg"])

    def label(self, parent, text):
        return tk.Label(parent, text=text, anchor="w", bg=self.palette["bg"], fg=self.palette["fg"])

    def button(self, parent, text, command):
        return tk.Button(parent, text=text, command=command, bg=self.palette["button_bg"], fg=self.palette["fg"])

    def display(self, text):
        self.details.config(state=tk.NORMAL)
        self.details.delete("1.0", tk.END)
        self.details.insert(tk.END, text)
        self.details.config(state=tk.DISABLED)

    def refresh(self):
        try:
            if self.mode == "memory":
                self.entries = list(reversed(self.app.notebook.cards))
                self.notice = ("Notebook unreadable: " + self.app.notebook.load_error if self.app.notebook.load_error else
                               "Ctrl/Shift-click to select several cards. Copy includes column headers for your spreadsheet.")
            else:
                self.entries, skipped = read_history(self.history_path)
                self.notice = f"{skipped} unreadable log lines skipped." if skipped else "Newest requests first. Search by text, date, or model."
        except OSError as error:
            self.entries = []
            self.notice = f"Could not read history: {error}"
        self.filter()

    def filter(self):
        query = self.search.get().casefold().strip()
        self.visible = [entry for entry in self.entries if query in " ".join(str(v) for v in entry.values()).casefold()]
        self.rows.delete(0, tk.END)
        for entry in self.visible:
            if self.mode == "memory":
                text = f"{entry['kind']}  |  {entry['term']}  —  {entry['meaning_pt']}"
            else:
                text = f"{entry.get('timestamp', '')[:19]}  |  {entry.get('model', '')}  |  {entry.get('status', 'ok')}  |  {entry['query']}"
            self.rows.insert(tk.END, " ".join(text.split())[:240])
        self.display("Select an item to see its full details." if self.visible else "No items found.")
        if self.mode == "memory":
            self.notes.delete("1.0", tk.END)
            self.lookup.set("")
            self.reference_button.config(state=tk.DISABLED)
        self.status.config(text=f"{len(self.visible)} of {len(self.entries)} items. {self.notice}")

    def selected(self):
        return [self.visible[index] for index in self.rows.curselection()]

    def select(self, event=None):
        items = self.selected()
        if not items:
            return
        item = items[0]
        if self.mode == "memory":
            self.display(f"{item['term']}  ·  {item['kind']}\n\nMeaning / explanation: {item['meaning_pt']}\n\n"
                         f"Example: {item['example']}\nUsage: {item['usage']}\n\n"
                         f"Original wording: {item.get('wrong', '')}\nSource request: {item.get('source_text', '')}\n"
                         f"Saved: {item.get('saved_at', 'Earlier version')}  ·  Next review: {item['due']}\n\n"
                         f"Reference: {item.get('quote_author', '')} {item.get('quote_work', '')}\n{item.get('reference_url', '')}\n\n"
                         "Oxford / Cambridge open the publisher's reference site. Edit the lookup term if no exact entry matches. "
                         "Tutor explanations are AI-generated.")
            self.lookup.set(item.get("lookup_term") or item["term"])
            self.notes.delete("1.0", tk.END)
            self.notes.insert(tk.END, item.get("personal_notes", ""))
            self.reference_button.config(state=tk.NORMAL if str(item.get("reference_url", "")).startswith("https://") else tk.DISABLED)
        else:
            self.display(f"{item.get('timestamp', '')} · {item.get('model', '')}\n"
                         f"Tokens: {item.get('input_tokens', '?')} in / {item.get('output_tokens', '?')} out\n"
                         f"Estimated USD: {item.get('cost_usd', 'unknown')}\n\n{item['query']}")
            self.app.load_history_entry(item)
            if not self.app.busy:
                self.app.root.lift()

    def open_dictionary(self, provider):
        term = self.lookup.get().strip()
        if term:
            webbrowser.open(dictionary_links(term)[provider])

    def save_notes(self):
        items = self.selected()
        if len(items) != 1:
            self.status.config(text="Select one card to edit its notes.")
            return
        try:
            self.app.notebook.update_notes(items[0], self.notes.get("1.0", "end-1c"), self.lookup.get())
        except OSError as error:
            messagebox.showerror("Could not save notes", str(error), parent=self.window)
            return
        self.refresh()
        self.status.config(text="Notes and dictionary lookup saved.")

    def open_reference(self):
        items = self.selected()
        url = items[0].get("reference_url", "") if items else ""
        if isinstance(url, str) and url.startswith("https://"):
            webbrowser.open(url)

    def copy(self, items):
        if not items:
            self.status.config(text="No cards selected to copy.")
            return
        self.app.copy_to_clipboard(spreadsheet_text(items))
        self.status.config(text=f"Copied {len(items)} rows plus headers. Paste directly into your spreadsheet.")

    def copy_selected(self):
        self.copy(self.selected())

    def copy_filtered(self):
        self.copy(self.visible)

    def export_csv(self):
        items = self.selected() or self.visible
        if not items:
            self.status.config(text="No cards to export.")
            return
        path = filedialog.asksaveasfilename(parent=self.window, title="Export selected cards (or filtered list)",
                                          defaultextension=".csv", initialfile="english-memory.csv",
                                          filetypes=[("CSV spreadsheet", "*.csv")])
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8-sig", newline="") as stream:
                stream.write(spreadsheet_text(items, delimiter=","))
        except OSError as error:
            messagebox.showerror("Could not export", str(error), parent=self.window)
            return
        self.status.config(text=f"Exported {len(items)} cards to {path}")

    def open_source(self):
        items = self.selected()
        if not items:
            return
        try:
            entries, _ = read_history(self.history_path)
        except OSError as error:
            self.status.config(text=str(error))
            return
        item = items[0]
        match = next((e for e in entries if item.get("request_id") and e["id"] == item["request_id"]), None)
        if match is None and item.get("source_text"):
            match = next((e for e in entries if e["query"] == item["source_text"]), None)
        if match:
            self.app.load_history_entry(match)
            self.app.root.lift()
        else:
            self.status.config(text="The source request is not in this installation's history log.")
