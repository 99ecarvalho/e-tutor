# Builds output\e-tutor.exe, a standalone Windows executable of E-Tutor.
#
# Copyright (c) 2025-2026 Eduardo Correia <ecorreia@apliant.com.br>
#
# This file is part of E-Tutor. It is free software, licensed under the GNU
# Lesser General Public License v3.0 or later. See COPYING.LESSER and COPYING
# for details.
#
# SPDX-License-Identifier: LGPL-3.0-or-later

Set-Location -Path $PSScriptRoot
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()

$appName = "e-tutor"
$iconPath = "icon.ico"  # optional; skipped if the file doesn't exist
$outputDir = "output"
$workDir = Join-Path $outputDir "build"
$venvPython = ".venv\Scripts\python.exe"

if (-Not (Test-Path $venvPython)) {
    Write-Host "Virtual environment not found. Creating .venv..."
    if (Get-Command py -ErrorAction SilentlyContinue) { py -3 -m venv .venv } else { python -m venv .venv }
    if ($LASTEXITCODE -ne 0) { throw "Failed to create virtual environment" }
}

# Python 3.10.0 has a bytecode bug that crashes PyInstaller (fixed in 3.10.1).
$pyVersion = & $venvPython -c "import sys; print('.'.join(map(str, sys.version_info[:3])))"
if ($pyVersion -eq "3.10.0") {
    throw "The .venv uses Python 3.10.0, which PyInstaller can't build with. Delete .venv and run this script again; it will be recreated with a newer Python."
}

Write-Host "Installing requirements and PyInstaller..."
& $venvPython -m pip install -q --disable-pip-version-check -r requirements.txt pyinstaller
if ($LASTEXITCODE -ne 0) { throw "Failed to install requirements" }

$pyinstallerArgs = @(
    "-m", "PyInstaller", "$appName.py",
    "--name", $appName,
    "--onefile",
    "--windowed",
    "--noconfirm",
    "--clean",
    "--log-level", "WARN",
    "--distpath", $outputDir,
    "--workpath", $workDir,
    "--specpath", $workDir,
    # pystray picks its OS backend at runtime, so PyInstaller can't see it.
    "--hidden-import", "pystray._win32"
)
if ($iconPath -and (Test-Path $iconPath)) {
    $pyinstallerArgs += @("--icon", (Resolve-Path $iconPath).Path)
}

Write-Host "Building $outputDir\$appName.exe..."
& $venvPython @pyinstallerArgs
if ($LASTEXITCODE -ne 0) { throw "PyInstaller failed" }

Remove-Item -Recurse -Force $workDir -ErrorAction SilentlyContinue

Write-Host "Build complete: $outputDir\$appName.exe" -ForegroundColor Green
Write-Host "The exe reads .env, user_prefs.json and log\ from its own folder. Copy your .env next to it, or set the key from Options > API Key & Endpoint."
