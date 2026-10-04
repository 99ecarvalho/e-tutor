#!/bin/bash
# Runs E-Tutor, creating the .venv virtual environment on first use.
#
# Copyright (c) 2025-2026 Eduardo Correia <ecorreia@apliant.com.br>
#
# This file is part of E-Tutor. It is free software, licensed under the GNU
# Lesser General Public License v3.0 or later. See COPYING.LESSER and COPYING
# for details.
#
# SPDX-License-Identifier: LGPL-3.0-or-later
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
