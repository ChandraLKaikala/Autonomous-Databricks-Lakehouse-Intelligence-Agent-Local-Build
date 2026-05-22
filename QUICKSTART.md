# Quick Start Guide

## ✅ System is Ready!

Your **Autonomous Databricks Lakehouse Intelligence Agent** system has been fully built and is ready to use.

## 📁 Project Location
```
C:\Users\lokes\Downloads\databricks-agent-system\
```

## 🚀 Run the Demo

Open PowerShell and run:

```powershell
cd C:\Users\lokes\Downloads\databricks-agent-system
python demo.py
```

This will:
- Set up a realistic lakehouse with 6 tables
- Create 3 DLT pipelines (Bronze → Silver → Gold)
- Set up 2 workflows with dependencies
- Run all 8 AI agents
- Display metrics and recommendations

## 🌐 View the Dashboard

1. Start the API server:
```powershell
python dashboard_api.py
```

2. Open the dashboard:
- **Web**: http://localhost:5000
- **File**: Open `dashboard.html` in your browser

3. Click "Run All Agents" to trigger agent execution

## 🔑 Enable Claude AI (Optional)

To use real Claude API instead of fallback mode:

1. Get your API key from: https://console.anthropic.com
2. Set environment variable:
```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-..."
python demo.py
```

## 📊 What You Get

### In the Terminal (Demo Output)
- Setup confirmation for 6 tables
- 3 DLT pipelines created
- 2 Workflows configured
- 8 Agents initialized
- Agent analysis and decisions
- Final metrics

### In the Dashboard
- Real-time system metrics
- Agent status cards
- Cost analysis and savings
- Data quality alerts
- Optimization recommendations
- Live event stream
- Pipeline lineage

## 🏗️ System Components

1. **databricks_mock.py** - Mock Databricks environment
2. **dlt_pipelines.py** - DLT pipeline system
3. **workflows.py** - Workflow orchestration
4. **agents.py** - 8 AI agents
5. **dashboard_api.py** - REST API backend
6. **dashboard.html** - Web dashboard

## 💡 What the Agents Do

| Agent | Role |
|-------|------|
| **Governance Agent** | Manages access, classification, compliance |
| **Delta Optimizer** | Optimizes table compression, partitioning |
| **Spark Optimizer** | Analyzes job performance, suggests optimizations |
| **Cost Manager** | Tracks costs, finds savings |
| **Quality Monitor** | Detects anomalies, quality issues |
| **DLT Pipeline Agent** | Monitors pipelines, detects issues |
| **Workflow Orchestrator** | Manages job scheduling, execution |
| **Orchestrator** | Coordinates all agents strategically |

## 📈 Architecture

```
┌─────────────────────────────────────┐
│   Mock Databricks Environment       │
│  - Unity Catalog                    │
│  - Delta Lake (DuckDB)              │
│  - Workflows & Jobs                 │
│  - Cost Tracking                    │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   DLT Pipelines                     │
│  - Bronze (Raw Data)                │
│  - Silver (Cleaned)                 │
│  - Gold (Aggregated)                │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   8 AI Agents (Using Claude API)    │
│  - Each agent has agentic loop      │
│  - Agents coordinate via Orchestrator
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   Dashboard & Metrics               │
│  - Flask REST API                   │
│  - Web Dashboard                    │
│  - Real-time Visualization          │
└─────────────────────────────────────┘
```

## 🎯 Try These Next Steps

### 1. Add More Data
Edit `demo.py` and add more sample tables, pipelines, or workflows.

### 2. Modify Agent Behavior
Edit `agents.py` and customize how agents analyze and decide.

### 3. Extend Workflows
Edit `workflows.py` to add more complex job dependencies.

### 4. Build Real Integrations
Connect to actual Databricks workspace using their API.

## 🐛 Troubleshooting

**Issue**: Demo fails to start
- **Solution**: Make sure all dependencies are installed: `pip install -r requirements.txt`

**Issue**: Dashboard won't load
- **Solution**: Make sure Flask API is running: `python dashboard_api.py`

**Issue**: Port 5000 already in use
- **Solution**: Change port in `dashboard_api.py` line: `app.run(port=5001)`

**Issue**: Unicode errors in output
- **Solution**: Already handled! Output uses ASCII-friendly text.

## 📚 Learn More

- See `README.md` for detailed architecture
- See `agents.py` for how agentic loops work
- See `dashboard_api.py` for API endpoints
- See `dlt_pipelines.py` for pipeline structure

## 💾 Files Created

```
databricks-agent-system/
├── databricks_mock.py          (Mock Databricks environment)
├── dlt_pipelines.py            (DLT Pipeline system)
├── workflows.py                (Workflow orchestration)
├── agents.py                   (8 AI agents)
├── dashboard_api.py            (Flask REST API)
├── dashboard.html              (Web dashboard)
├── demo.py                     (Demo script)
├── requirements.txt            (Dependencies)
├── README.md                   (Full documentation)
├── QUICKSTART.md              (This file)
├── unity_catalog.db           (Metadata database)
├── delta_lake.duckdb          (Data warehouse)
├── cost_tracking.db           (Cost tracking)
```

---

**Ready to see it in action?** 🚀

```powershell
cd C:\Users\lokes\Downloads\databricks-agent-system
python demo.py
```

Then start the dashboard:
```powershell
python dashboard_api.py
```

And open http://localhost:5000 in your browser!
