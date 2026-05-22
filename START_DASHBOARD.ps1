# Start Dashboard API in PowerShell

cd "C:\Users\lokes\Downloads\databricks-agent-system"

# Kill any existing Python processes
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 1

# Clean up old database files
Remove-Item -Path delta_lake.duckdb, unity_catalog.db, cost_tracking.db -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1

Write-Host "Starting Dashboard API..." -ForegroundColor Green
Write-Host "================================================"
Write-Host ""

# Start the dashboard
python dashboard_api.py

Write-Host ""
Write-Host "================================================"
Write-Host "Dashboard started on http://localhost:5000" -ForegroundColor Green
Write-Host "Open in browser and click 'Run All Agents'" -ForegroundColor Cyan
