# Gesture & Face Recognition Authentication - Quick Start Script
# This script starts both the backend and frontend servers

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Gesture & Face Auth System Launcher  " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running from project root
if (-Not (Test-Path "backend") -or -Not (Test-Path "frontend")) {
    Write-Host "ERROR: Please run this script from the project root directory!" -ForegroundColor Red
    Write-Host "Current directory: $PWD" -ForegroundColor Yellow
    exit 1
}

# Start Backend
Write-Host "[1/2] Starting Backend (Flask)..." -ForegroundColor Green
Write-Host "      Port: 5000" -ForegroundColor Gray
Write-Host ""

$backendProcess = Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\backend'; python app.py" -PassThru
Start-Sleep -Seconds 3

# Start Frontend
Write-Host "[2/2] Starting Frontend (Express)..." -ForegroundColor Green
Write-Host "      Port: 3000" -ForegroundColor Gray
Write-Host ""

$frontendProcess = Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend'; npm start" -PassThru
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Both servers are starting...         " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend:  http://localhost:5000" -ForegroundColor Yellow
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Yellow
Write-Host ""
Write-Host "Open your browser and navigate to:" -ForegroundColor Green
Write-Host "  http://localhost:3000/login" -ForegroundColor Cyan -BackgroundColor Black
Write-Host ""
Write-Host "Press Ctrl+C in each terminal window to stop the servers" -ForegroundColor Gray
