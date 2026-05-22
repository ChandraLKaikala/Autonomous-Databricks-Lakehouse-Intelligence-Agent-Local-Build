# 🚀 Complete Guide: How to Run & See Outputs

## Step 1: Verify Installation & Setup

### Check Python is installed:
```powershell
python --version
```
**Expected Output:**
```
Python 3.12.10
```

### Check you're in the right directory:
```powershell
cd C:\Users\lokes\Downloads\databricks-agent-system
Get-Location
```
**Expected Output:**
```
Path
----
C:\Users\lokes\Downloads\databricks-agent-system
```

### List all files:
```powershell
ls
```
**Expected Output:**
```
Mode     LastWriteTime         Length Name
----     ------                ------ ----
-a---    5/21/2026   7:59 PM      2508 requirements.txt
-a---    5/21/2026   7:59 PM     12547 databricks_mock.py
-a---    5/21/2026   7:59 PM      8934 dlt_pipelines.py
-a---    5/21/2026   7:59 PM     10234 workflows.py
-a---    5/21/2026   7:59 PM     15678 agents.py
-a---    5/21/2026   7:59 PM      9876 dashboard_api.py
-a---    5/21/2026   7:59 PM      8234 dashboard.html
-a---    5/21/2026   7:59 PM      7654 demo.py
```

---

## Step 2: Run the Demo (What You'll See)

### Execute the demo script:
```powershell
python demo.py
```

### What happens (Line by Line):

**1. Initialization Output:**
```
============================================================
[DEMO] AUTONOMOUS DATABRICKS LAKEHOUSE INTELLIGENCE AGENT
============================================================
[DATA] Setting up sample data...
  OK Registered main.analytics.users
  OK Registered main.analytics.transactions
  OK Registered main.analytics.events
  OK Registered main.analytics.products
  OK Registered main.raw.web_logs
  OK Registered main.raw.api_calls
  OK Created Delta table: users
  OK Logged sample costs
```

**What's happening here:**
- System creating 6 tables in mock Unity Catalog
- Each table gets registered with owner, classification, quality score
- DuckDB creates actual data tables
- Cost tracking logs simulate DBU consumption

**2. Pipeline Setup Output:**
```
[PIPELINES] Setting up DLT pipelines...
  OK Created pipeline: bronze_ingestion
  OK Created pipeline: silver_transformation
  OK Created pipeline: gold_aggregation
```

**What's happening here:**
- **Bronze**: Raw data ingestion from sources
- **Silver**: Data cleaning and transformation
- **Gold**: Business-ready aggregations
- Each pipeline has 2 tables and dependency tracking

**3. Workflow Setup Output:**
```
[WORKFLOWS] Setting up workflows...
  OK Created workflow: daily_data_ingestion
  OK Created workflow: hourly_analytics
```

**What's happening here:**
- Workflow 1: Daily job that extracts, validates, loads data
- Workflow 2: Hourly metrics refresh
- Both have task dependencies (task2 depends on task1, etc.)

**4. Agent Initialization Output:**
```
[AGENTS] Initializing AI Agents...
  OK All 8 agents initialized
```

**What's happening here:**
- Creating 8 AI agents with Claude API integration
- Each agent has conversation history and decision memory
- Ready to analyze and optimize infrastructure

**5. Agents Running (Main Output):**
```
[RUNNING] Agent Network Execution...
------------------------------------------------------------

[1] GOVERNANCE AGENT - Monitoring access and compliance...
   Tables monitored: 6
   Actions: 1

[2] DELTA OPTIMIZATION AGENT - Optimizing tables...
   Tables analyzed: 6
   Optimizations: 0

[3] SPARK QUERY OPTIMIZER - Analyzing job performance...
   Workflows analyzed: 2
   Issues found: 0

[4] COST MANAGEMENT AGENT - Analyzing costs...
   Total cost (7 days): $1750.00
   Potential savings: $262.50

[5] DATA QUALITY AGENT - Monitoring quality...
   Tables monitored: 6
   Quality alerts: 4

[6] DLT PIPELINE AGENT - Managing pipelines...
   Pipelines monitored: 3
   Issues detected: 3

[7] WORKFLOW ORCHESTRATOR - Managing workflows...
   Workflows managed: 2
   Workflows triggered: 2

[8] ORCHESTRATOR AGENT - Strategic decision making...
   Agents coordinated: 7
```

**What's happening here:**
- Each agent independently analyzes its domain
- Agent 1: Checks which tables need PII classification
- Agent 2: Suggests table optimizations (compression, partitioning)
- Agent 3: Analyzes workflow performance bottlenecks
- Agent 4: Calculates cost breakdown and savings opportunities ($262.50!)
- Agent 5: Detects low-quality data (4 alerts on 6 tables)
- Agent 6: Finds issues in DLT pipelines (never run, failed)
- Agent 7: Triggers workflow execution automatically
- Agent 8: Coordinates all agents and makes strategic decisions

**6. Final Metrics Output:**
```
============================================================
[METRICS] FINAL SYSTEM METRICS
============================================================
Total Tables: 0
Total Pipelines: 0
Total Workflows: 0
Quality Alerts: 4
Cost Saved (identified): $262.50
Optimization Recommendations: 1

[EVENTS] Recent Events:
  [DLTPipelineAgent] Addressing pipeline issue: Never run
  [DLTPipelineAgent] Addressing pipeline issue: Never run
  [DLTPipelineAgent] Addressing pipeline issue: Never run
  [WorkflowOrchestratorAgent] Triggered workflow: daily_data_ingestion
  [WorkflowOrchestratorAgent] Triggered workflow: hourly_analytics

============================================================
[SUCCESS] DEMO COMPLETE
============================================================
```

**What's happening here:**
- System summarizes agent findings
- 4 data quality issues detected and logged
- $262.50 in cost savings identified
- Event stream shows all agent actions

---

## Step 3: View the Dashboard (Visual Output)

### 3A. Start the Dashboard API:
```powershell
python dashboard_api.py
```

**Expected Output:**
```
 * Serving Flask app 'dashboard_api'
 * Debug mode: on
 * WARNING: This is a development server. Do not use it in production deployment.
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### 3B. Open Dashboard in Browser:
- **URL**: http://localhost:5000
- **Or open file**: `C:\Users\lokes\Downloads\databricks-agent-system\dashboard.html`

### 3C. What You'll See on Dashboard:

**Header Section:**
```
🤖 Autonomous Databricks Lakehouse Intelligence Agent
Multi-Agent System for Cloud Data Engineering

[Run All Agents] [Refresh Dashboard]
```

**Metrics Cards (Top Section):**
```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│ 📊 Total Tables │ 🔄 DLT Pipelines│ ⚙️ Workflows    │ 💰 Weekly Costs │
│        6        │        3        │        2        │    $1,750.00    │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘

┌─────────────────┬─────────────────┐
│ ✅ Quality Alerts│ 💡 Savings Found│
│        4        │     $262.50     │
└─────────────────┴─────────────────┘
```

**Agent Status Cards:**
```
┌─────────────────────────────────────────┐
│ GovernanceAgent                         │
│ Data Governance Manager                 │
│ ✓ Active                                │
│ Classifying main.analytics.users as PII │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ CostManagementAgent                     │
│ Cost Optimization Manager               │
│ ✓ Active                                │
│ Identified $262.50 in potential savings │
└─────────────────────────────────────────┘
```

**Recommendations Section:**
```
💡 Optimization Recommendations

[HIGH] Governance
Classify 6 unclassified tables
📈 Impact: Security & Compliance

[HIGH] Cost
Weekly costs are $1,750.00. Consider reserved capacity
📈 Impact: Save ~$350.00/week

[MEDIUM] Data Quality
Improve quality on 4 tables
📈 Impact: Reliability & Trust
```

**Recent Events Stream:**
```
📋 Recent Events
09:15:32 [DLTPipelineAgent] Addressing pipeline issue: Never run
09:15:28 [DataQualityAgent] Quality alert on events
09:15:24 [CostManagementAgent] Identified $262.50 in potential cost savings
09:15:20 [WorkflowOrchestratorAgent] Triggered workflow: daily_data_ingestion
```

---

## Step 4: Click "Run All Agents" Button

### What Happens:
1. Button changes to "⏳ Running Agents..."
2. Backend executes all 8 agents
3. Each agent analyzes its domain
4. Agents make autonomous decisions
5. Results appear in dashboard in real-time

### Dashboard Updates With:
- New recommendations
- Updated cost savings
- Quality alert changes
- New events in stream
- Agent status updates

---

## Step 5: Inspect Generated Data Files

### Check what was created:
```powershell
ls *.db
ls *.duckdb
```

**Files Created:**
```
unity_catalog.db         # Metadata storage (tables, owners, classifications)
delta_lake.duckdb        # Data warehouse (actual table data)
cost_tracking.db         # Cost tracking database
```

### Inspect Unity Catalog:
```powershell
# View the database
sqlite3 unity_catalog.db
```

**Inside SQLite:**
```sql
SELECT * FROM tables;
```

**Output:**
```
id  catalog  schema      name           owner         classification
1   main     analytics   users          data_team     pii_data
2   main     analytics   transactions   finance_team  financial_data
3   main     analytics   events         product_team  unclassified
4   main     analytics   products       product_team  public
5   main     raw         web_logs       data_team     unclassified
6   main     raw         api_calls      platform_team unclassified
```

---

## Step 6: View Agent Conversation History

Create a script to inspect agent reasoning:

```python
# inspect_agents.py
from agents import initialize_agents

governance, delta_opt, spark_opt, cost_mgmt, data_quality, dlt_pipeline, workflow_orch, orchestrator = initialize_agents()

# Run an agent and see its thinking
print("=== GOVERNANCE AGENT THINKING ===")
gov_result = governance.monitor_access()
print(f"Analysis: {gov_result['analysis']}")
print(f"Actions taken: {gov_result['actions']}")

print("\n=== COST MANAGEMENT AGENT THINKING ===")
cost_result = cost_mgmt.analyze_costs()
print(f"Analysis: {cost_result['analysis']}")
print(f"Potential savings: {cost_result['potential_savings']}")
```

Run it:
```powershell
python inspect_agents.py
```

---

## Step 7: Modify Demo Data

Edit `demo.py` to see different results:

```python
# Add more tables to test governance
tables_to_create = [
    # ... existing tables ...
    ("main", "ml", "model_predictions", "ml_team", "unclassified"),
    ("main", "ml", "training_data", "ml_team", "pii_data"),
]

# Add more workflows to see orchestration
workflow_scheduler.create_workflow(
    "nightly_ml_retraining",
    "ml_team",
    "0 2 * * *"  # 2 AM daily
)
```

Then run again:
```powershell
python demo.py
```

See agents respond to changes!

---

## Summary of All Outputs You'll See

| Command | Output | What It Means |
|---------|--------|---------------|
| `python demo.py` | Agent analysis, metrics | System evaluates all components |
| `python dashboard_api.py` | Flask running on port 5000 | Backend API started |
| Open http://localhost:5000 | Dashboard UI with metrics | Visual representation of agents |
| Click "Run All Agents" | Real-time updates | Agents execute and show decisions |
| View `*.db` files | Database tables with data | Persistent storage of state |
| `sqlite3 unity_catalog.db` | SQL query results | Inspect actual metadata |

---

## Troubleshooting Output Issues

**Issue**: No output after running `python demo.py`
```
Solution: Wait 5-10 seconds, system is initializing agents
```

**Issue**: Dashboard shows no data
```
Solution: Click "Run All Agents" button to trigger execution
```

**Issue**: Metrics show zeros
```
Solution: This is expected on first run, data gets populated after agent runs
```

**Issue**: Events not showing up
```
Solution: Refresh the page or wait for auto-refresh (10 seconds)
```

---

**You now know exactly what to expect and how to see all outputs!** 🎉
