# ========================================
# AUTONOMOUS DATABRICKS AGENT SYSTEM
# Final Working Solution
# ========================================

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "   DATABRICKS AGENT SYSTEM LAUNCHER" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Clean everything
Write-Host "[STEP 1/3] Cleaning up..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -Confirm:$false
Start-Sleep -Seconds 2
Remove-Item "C:\Users\lokes\Downloads\databricks-agent-system\*.db" -Force -ErrorAction SilentlyContinue
Remove-Item "C:\Users\lokes\Downloads\databricks-agent-system\*.duckdb" -Force -ErrorAction SilentlyContinue
Write-Host "[OK] Cleaned" -ForegroundColor Green

# Step 2: Run demo
Write-Host "[STEP 2/3] Running demo (populating data)..." -ForegroundColor Yellow
cd "C:\Users\lokes\Downloads\databricks-agent-system"
python demo.py
Write-Host "[OK] Demo complete" -ForegroundColor Green

# Step 3: Start dashboard
Write-Host "[STEP 3/3] Starting Dashboard..." -ForegroundColor Yellow
Write-Host ""
Write-Host "======================================" -ForegroundColor Green
Write-Host "      DASHBOARD IS READY!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""
Write-Host "[WEB] Open in browser: http://localhost:5000" -ForegroundColor Cyan
Write-Host "[FEATURES]" -ForegroundColor Cyan
Write-Host "   * Real-time metrics" -ForegroundColor Gray
Write-Host "   * Agent status cards" -ForegroundColor Gray
Write-Host "   * Cost analysis" -ForegroundColor Gray
Write-Host "   * Optimization recommendations" -ForegroundColor Gray
Write-Host ""
Write-Host "[ACTION] Click 'Run All Agents' to execute" -ForegroundColor Yellow
Write-Host ""

python dashboard_api.py
