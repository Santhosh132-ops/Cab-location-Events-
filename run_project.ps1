$ErrorActionPreference = "Stop"

Write-Host "Starting Real-Time Cab Location Tracker..." -ForegroundColor Cyan

# 1. Check Virtual Environment
if (-not (Test-Path "venv")) {
    Write-Host "Virtual environment not found. Creating..." -ForegroundColor Yellow
    python -m venv venv
}

# Always install/update dependencies
Write-Host "Installing dependencies..." -ForegroundColor Cyan
.\venv\Scripts\python.exe -m pip uninstall -y kafka-python
.\venv\Scripts\python.exe -m pip install -r producer\requirements.txt -r consumer\requirements.txt -r backend\requirements.txt

# 2. Start Docker if not running (Simple check)
Write-Host "Ensuring Docker containers are up..." -ForegroundColor Cyan
docker-compose up -d

# 3. Start Backend
Write-Host "Launching Backend API..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& { .\venv\Scripts\python.exe -m uvicorn backend.main:app --reload }"

# 4. Start Consumer
Write-Host "Launching Consumer..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& { .\venv\Scripts\python.exe consumer\main.py }"

# 5. Start Producer
Write-Host "Launching Producer (Driver Simulation)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& { .\venv\Scripts\python.exe producer\main.py }"

# 6. Open Frontend
Write-Host "Opening Frontend Map..." -ForegroundColor Green
Start-Process "frontend\index.html"

Write-Host "Project is running! Check the opened windows." -ForegroundColor Cyan
