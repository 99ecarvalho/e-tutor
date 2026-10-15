#!/bin/bash
# Runs E-Tutor, creating the platform-specific virtual environment on first use.
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

case "$(uname -s)" in
    Linux*) VENV_DIR=".venv-linux" ;;
    Darwin*) VENV_DIR=".venv-macos" ;;
    *)
        echo "Unsupported operating system: $(uname -s)" >&2
        exit 1
        ;;
esac

VENV_PYTHON="$VENV_DIR/bin/python"

if [ ! -x "$VENV_PYTHON" ]; then
    echo "Virtual environment not found. Creating $VENV_DIR..."
    PYTHON=$(command -v python3 || command -v python)
    "$PYTHON" -m venv "$VENV_DIR"
    echo "Virtual environment created."
fi

echo "Checking requirements..."
"$VENV_PYTHON" -m pip install -q --disable-pip-version-check -r requirements.txt

echo "Launching application..."
"$VENV_PYTHON" e-tutor.py
