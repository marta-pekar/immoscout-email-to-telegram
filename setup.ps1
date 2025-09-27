# PowerShell setup script for Windows

# Create virtual environment if it doesn't exist
if (!(Test-Path ".venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Green
    python -m venv .venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Green
& .\.venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Green
pip install -r requirements.txt

Write-Host "Setup complete! Virtual environment is activated." -ForegroundColor Green
Write-Host "To run the script: python main.py" -ForegroundColor Yellow
Write-Host "To deactivate: deactivate" -ForegroundColor Yellow