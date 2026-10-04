# Runs E-Tutor, creating the .venv virtual environment on first use.
# (c) Eduardo Correia <ecorreia@apliant.com.br>

Set-Location -Path $PSScriptRoot
Write-Host "Starting E-Tutor..."

$venvPython = ".venv\Scripts\python.exe"

if (-Not (Test-Path $venvPython)) {
    Write-Host "Virtual environment not found. Creating .venv..."
    if (Get-Command py -ErrorAction SilentlyContinue) { py -3 -m venv .venv } else { python -m venv .venv }
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
    Write-Host "Virtual environment created." -ForegroundColor Green
}

Write-Host "Checking requirements..."
& $venvPython -m pip install -q --disable-pip-version-check -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to install requirements" -ForegroundColor Red
    exit 1
}

Write-Host "Launching application..."
& $venvPython e-tutor.py
