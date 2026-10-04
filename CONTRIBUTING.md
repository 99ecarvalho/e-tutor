# Contributing to E-Tutor

Thanks for your interest in E-Tutor! Bug reports, documentation fixes, and code
are all welcome. This guide explains how to get a change merged with as little
back-and-forth as possible.

- [Ways to contribute](#ways-to-contribute)
- [Reporting bugs](#reporting-bugs)
- [Development setup](#development-setup)
- [Making a change](#making-a-change)
- [Coding style](#coding-style)
- [Commit messages](#commit-messages)
- [Pull requests](#pull-requests)
- [Licensing of contributions](#licensing-of-contributions)

## Ways to contribute

- **Report a bug** or unexpected behavior. See [Reporting bugs](#reporting-bugs).
- **Improve the documentation.** If something was unclear or wrong, a fix is
  welcome. The user guides are [README.md](README.md) and
  [QUICKSTART.md](QUICKSTART.md).
- **Improve the coaching.** Better prompts, clearer grammar notes, new
  situations or tones, and better review scheduling are all useful.
- **Test on your platform.** Reports from Windows, Linux, and macOS, and from
  different OpenAI-compatible endpoints, help a lot.

## Reporting bugs

Search the [existing issues](https://github.com/99ecarvalho/e-tutor/issues)
first. If your bug is new, [open an issue](https://github.com/99ecarvalho/e-tutor/issues/new)
and include:

- the commit hash or release you used, and whether you ran from source or the
  built `output\e-tutor.exe`;
- your OS and Python version;
- the provider (OpenAI, Azure AI Foundry, or another OpenAI-compatible server)
  and the model or deployment name;
- the options you selected (preset, situation, tone, coaching depth);
- what you expected to happen and what happened instead;
- any error shown in the console or in `log/e-tutor.log`.

Never paste your API key or other secrets into an issue. A minimal way to
reproduce the problem is the most valuable thing you can provide.

## Development setup

E-Tutor is a Python 3.8+ Tkinter application. The helper scripts create a
`.venv` and install the requirements; there is nothing else to set up.

```bash
git clone https://github.com/99ecarvalho/e-tutor.git
cd e-tutor
./run.sh                          # or .\run.ps1 on Windows
```

The source files are:

| File | Purpose |
| ---- | ------- |
| `e-tutor.py` | The Tkinter application: window, options, API client, logging, tray, and hotkeys |
| `coaching.py` | Coaching depths and focuses, the learning prompt, response normalization, and the learning store |
| `memory_tools.py` | Saved-memory cards, dictionary links, and replay of logged results |
| `tutor_library.py` | The Saved memory window: search, notes, and exports |
| `quotes.py` | The rotating, source-checked quotes |
| `test_coaching.py`, `test_memory.py` | `unittest` suites for the modules above |

### Testing your change

Before opening a pull request:

1. Run the tests and add one that fails without your change:

   ```bash
   .venv/bin/python -m unittest -v test_coaching test_memory
   ```

2. Launch the app, send a request with both `Grammar only` and a full
   coaching preset, and confirm the correction, rewrites, lesson, quote,
   saving, Review notebook, Saved memory, and History still work, with no
   errors in the console.
3. Try the edge cases your change could affect: a request that returns a
   malformed response, an unreadable notebook, replaying an old log entry, and
   switching providers (OpenAI vs. Azure).

Describe what you tested in the pull request.

## Making a change

1. For anything larger than a small fix, **open an issue first** to discuss
   the approach.
2. Fork the repository and create a branch from `main`:
   `git checkout -b fix/review-scheduling`.
3. Keep each pull request focused on one topic. Unrelated clean-ups belong in a
   separate pull request.
4. Update the documentation in the same pull request when you change behavior:
   the README, QUICKSTART, and the in-app hints.
5. Keep saved notebooks and logs backward compatible: existing
   `learning_notebook.json` cards and `log/api_log.jsonl` lines must still load.

## Coding style

Follow the style of the surrounding code:

- Plain, modern Python that runs on 3.8+, with the standard library plus the
  dependencies in `requirements.txt`.
- 4-space indentation, no tabs.
- `snake_case` for functions and variables, `PascalCase` for classes, and
  `UPPER_CASE` for module-level constants.
- Keep the Tkinter UI in `e-tutor.py`; keep coaching logic, memory, and quotes
  in their own modules so the tests can exercise them without a window.
- Long-running work (API calls) runs on a background thread so the window stays
  responsive; don't block the Tk main loop.
- Never log or print API keys. Keep secrets in `.env`, which is git-ignored.

New source files start with this header:

```python
# One-line description
#
# Copyright (c) 2026 Your Name <you@example.com>
#
# This file is part of E-Tutor. It is free software, licensed under the GNU
# Lesser General Public License v3.0 or later. See COPYING.LESSER and COPYING
# for details.
#
# SPDX-License-Identifier: LGPL-3.0-or-later
```

When you make a substantial change to an existing file, you may add your own
copyright line below the existing one.

## Commit messages

The project uses [Conventional Commits](https://www.conventionalcommits.org/):

```text
<type>(<optional scope>): <short summary in the imperative>

<optional body explaining what changed and why>
```

Common types are `feat`, `fix`, `docs`, `refactor`, `perf`, `test`, `build`,
and `chore`. For example:

```text
fix(review): return remembered cards after the correct interval

The scheduler advanced the due date before saving the stage, so a card
reappeared a day early after every review.
```

Keep the summary line under about 72 characters. Make each commit leave the
application working.

## Pull requests

Before you open a pull request, check that:

- [ ] `test_coaching` and `test_memory` pass;
- [ ] a full request and a `Grammar only` request both work, with no new
      console errors;
- [ ] saved notebooks and logs from older versions still load;
- [ ] documentation and in-app hints reflect any change in behavior;
- [ ] new files carry the copyright and SPDX header;
- [ ] commits follow the commit message convention.

A maintainer will review the pull request. You may be asked for changes, so
please don't take that as a rejection. It is how the code stays maintainable.

## Licensing of contributions

E-Tutor is licensed under the GNU Lesser General Public License v3.0 or later
(see [COPYING.LESSER](COPYING.LESSER) and [COPYING](COPYING)). By submitting a
contribution, you agree that it is licensed under the same terms, and you
confirm that you have the right to submit it.
