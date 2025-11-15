# Frontend Launcher
Write-Host "Starting Express Frontend Server..." -ForegroundColor Green
Write-Host "Port: 3000" -ForegroundColor Cyan
Write-Host ""

cd frontend

# Check if node_modules exists
if (-Not (Test-Path "node_modules")) {
    Write-Host "node_modules not found. Running npm install..." -ForegroundColor Yellow
    npm install
    Write-Host ""
}

# Run Express server
npm start
