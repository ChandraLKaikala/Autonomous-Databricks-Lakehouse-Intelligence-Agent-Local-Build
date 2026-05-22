# Safe Dashboard Startup Script

Write-Host "================================" -ForegroundColor Green
Write-Host "Dashboard Startup Script" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""

# Step 1: Kill any existing Python processes
Write-Host "[1/4] Stopping any existing Python processes..." -ForegroundColor Cyan
$processes = Get-Process python -ErrorAction SilentlyContinue
if ($processes) {
    $processes | Stop-Process -Force -Confirm:$false
    Write-Host "✓ Python processes stopped" -ForegroundColor Green
    Start-Sleep -Seconds 2
} else {
    Write-Host "✓ No Python processes running" -ForegroundColor Green
}

# Step 2: Clean up database files
Write-Host "[2/4] Cleaning up old database files..." -ForegroundColor Cyan
$dbFiles = @("delta_lake.duckdb", "unity_catalog.db", "cost_tracking.db")
foreach ($file in $dbFiles) {
    $filePath = Join-Path (Get-Location) $file
    if (Test-Path $filePath) {
        Remove-Item $filePath -Force -ErrorAction SilentlyContinue
        Write-Host "  ✓ Deleted $file" -ForegroundColor Green
    }
}
Start-Sleep -Seconds 1

# Step 3: Verify Flask can start
Write-Host "[3/4] Verifying environment..." -ForegroundColor Cyan
python -c "import flask; import duckdb; import anthropic" -ErrorAction SilentlyContinue
if ($?) {
    Write-Host "✓ All dependencies installed" -ForegroundColor Green
} else {
    Write-Host "✗ Missing dependencies - installing..." -ForegroundColor Yellow
    pip install -r requirements.txt -q
    Write-Host "✓ Dependencies installed" -ForegroundColor Green
}

# Step 4: Start dashboard
Write-Host "[4/4] Starting Dashboard API..." -ForegroundColor Cyan
Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "Dashboard Ready!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Open in browser:" -ForegroundColor Cyan
Write-Host "   http://localhost:5000" -ForegroundColor Yellow
Write-Host ""
Write-Host "📊 Features:" -ForegroundColor Cyan
Write-Host "   • Real-time metrics" -ForegroundColor Gray
Write-Host "   • Agent status" -ForegroundColor Gray
Write-Host "   • Cost analysis" -ForegroundColor Gray
Write-Host "   • Optimization recommendations" -ForegroundColor Gray
Write-Host "   • Event stream" -ForegroundColor Gray
Write-Host ""
Write-Host "💡 Click 'Run All Agents' button to trigger execution" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press CTRL+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the Flask app with no reload to avoid file lock issues
python -c "
import os
os.environ['FLASK_ENV'] = 'production'
from dashboard_api import app
app.run(debug=False, port=5000, host='0.0.0.0')
"
