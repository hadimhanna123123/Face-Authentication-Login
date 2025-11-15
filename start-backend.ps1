# Backend Launcher
Write-Host "Starting Flask Backend Server..." -ForegroundColor Green
Write-Host "Port: 5000" -ForegroundColor Cyan
Write-Host ""

cd backend

# Check if virtual environment exists
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    .\venv\Scripts\Activate.ps1
}

# Run Flask app
python app.py
