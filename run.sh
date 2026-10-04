#!/bin/bash
# Runs E-Tutor, creating the .venv virtual environment on first use.
# (c) Eduardo Correia <ecorreia@apliant.com.br>
set -e
cd "$(dirname "$0")"
echo "Starting E-Tutor..."

VENV_PYTHON=".venv/bin/python"

if [ ! -x "$VENV_PYTHON" ]; then
    echo "Virtual environment not found. Creating .venv..."
    PYTHON=$(command -v python3 || command -v python)
    "$PYTHON" -m venv .venv
    echo "Virtual environment created."
fi

echo "Checking requirements..."
"$VENV_PYTHON" -m pip install -q --disable-pip-version-check -r requirements.txt

echo "Launching application..."
"$VENV_PYTHON" e-tutor.py
