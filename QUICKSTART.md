# 🚀 Quick Start Guide

Copyright (c) 2025-2026 Eduardo Correia <ecorreia@apliant.com.br>

- [Getting it running](#getting-it-running)
- [Connecting to an API](#connecting-to-an-api)
- [Your first request](#your-first-request)
- [Running the tests](#running-the-tests)
- [Building the Windows executable](#building-the-windows-executable)
- [A daily routine](#a-daily-routine)

## Getting it running

E-Tutor is a desktop Tkinter application. You need Python 3.8 or newer. The
helper scripts create a `.venv` virtual environment on first run, install the
requirements, and start the app; they work from any folder.

### 1. Get the code

```bash
git clone https://github.com/99ecarvalho/e-tutor.git
cd e-tutor
```

### 2. Start it

**Windows (PowerShell):**

```powershell
.\run.ps1
```

**Linux/Mac:**

```sh
./run.sh
```

On Windows, `.venv` is created with the newest Python known to the `py`
launcher. On Linux, the `keyboard` library needs root to register the global
hotkey; without it, the app still works through the window.

**Manual setup**, if you prefer:

```sh
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt   # Windows
.venv/bin/python -m pip install -r requirements.txt       # Linux/Mac
.venv\Scripts\python e-tutor.py                           # or .venv/bin/python e-tutor.py
```

## Connecting to an API

E-Tutor works with OpenAI, Azure AI Foundry / Azure OpenAI, or any
OpenAI-compatible server. Open `Options` > `API Key & Endpoint` in the app, or
create a `.env` file next to `e-tutor.py`:

```ini
# Required: the key for OpenAI or for your custom endpoint
OPENAI_API_KEY=sk-...

# Optional: any OpenAI-compatible endpoint. Leave out for api.openai.com.
# Azure AI Foundry / Azure OpenAI (v1 API):
# OPENAI_BASE_URL=https://<resource>.openai.azure.com/openai/v1/

# Optional: only for the classic Azure deployments API.
# AZURE_OPENAI_API_VERSION=2024-10-21
```

Values in `.env` take priority over environment variables of the same name. On
Azure, requests use your **deployment name** as the model; add it with
`Options` > `Select Model` > `Add Custom Model / Azure Deployment`.

## Your first request

1. Pick a **preset** (start with `Daily coach`) and a **Situation** such as a
   meeting, Slack/Teams, email, or a job interview.
2. Type your English draft in the box and press **Enter** (Shift+Enter adds a
   new line), or copy text anywhere and press **Ctrl+Shift+R**.
3. Read the **Corrected** line first, then the **Grammar notes** and the
   rewrite versions.
4. Click `Copy first rewrite`, or double-click the version you want.
5. Click **Save** beside anything worth keeping, then open the **Review
   notebook** later to practice it.

## Running the tests

```bash
.venv\Scripts\python -m unittest -v test_coaching test_memory   # Windows
.venv/bin/python -m unittest -v test_coaching test_memory       # Linux/Mac
```

The tests cover response validation, teaching controls, review persistence and
scheduling, spreadsheet exports, history logging, and backward-compatible
replay. They do not call a live API or change your real preferences or
notebook.

## Building the Windows executable

```powershell
.\build.ps1
```

This installs PyInstaller into `.venv` and produces `output\e-tutor.exe`
(git-ignored). Python 3.10.0 can't be used because of a bug that crashes
PyInstaller. To use a custom icon, put an `icon.ico` in the project folder.

## A daily routine

1. Select **Daily coach** and **Random mix**, and choose the real situation.
2. Send your draft; read the correction and compare the Native and Executive
   versions.
3. Read the short lesson and optional **Quote**; click **Source** or **Save**.
4. Open the **Review notebook** for a few minutes each morning: explain each
   expression and use it in a new sentence before revealing its meaning.
5. Use **Deep dive** when you have time, or **Rewrites only** during a busy
   meeting. Use the **Interview** preset for concise, evidence-based answers.

See [README.md](README.md) for the full feature list.
