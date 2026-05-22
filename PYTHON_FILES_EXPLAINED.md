# 📁 Main Python Files Explained: What Each File Does

---

## 🗂️ The 6 Tables: Where They Are Located

### Table Storage Location

```
Unity Catalog Database (SQLite)
File: unity_catalog.db
Location: C:\Users\lokes\Downloads\databricks-agent-system\unity_catalog.db

Table Structure:
┌─────────────────────────────────────────────────────────────┐
│ ID │ CATALOG │ SCHEMA   │ NAME         │ OWNER        │ ...│
├────┼─────────┼──────────┼──────────────┼──────────────┼────┤
│ 1  │ main    │ analytics│ users        │ data_team    │    │
│ 2  │ main    │ analytics│ transactions │ finance_team │    │
│ 3  │ main    │ analytics│ events       │ product_team │    │
│ 4  │ main    │ analytics│ products     │ product_team │    │
│ 5  │ main    │ raw      │ web_logs     │ data_team    │    │
│ 6  │ main    │ raw      │ api_calls    │ platform_team│    │
└────┴─────────┴──────────┴──────────────┴──────────────┴────┘
```

### The 6 Tables (In Detail)

| # | Full Name | Type | Owner | Classification | Quality Score | Purpose |
|---|-----------|------|-------|-----------------|----------------|---------|
| 1 | `main.analytics.users` | PII | data_team | PII Data | 0.95 | Customer user profiles |
| 2 | `main.analytics.transactions` | Financial | finance_team | Financial Data | 0.85 | Payment transactions |
| 3 | `main.analytics.events` | Activity | product_team | Unclassified | 0.70 | User activity events |
| 4 | `main.analytics.products` | Reference | product_team | Public | 0.80 | Product catalog |
| 5 | `main.raw.web_logs` | Logs | data_team | Unclassified | 0.60 | Raw web server logs |
| 6 | `main.raw.api_calls` | Logs | platform_team | Unclassified | 0.50 | Raw API request logs |

### How to Access the Tables

**Option 1: Through Python Code**
```python
from databricks_mock import unity_catalog

# Get all tables
tables = unity_catalog.get_tables()
for table in tables:
    print(f"{table['name']} - Owner: {table['owner']} - Quality: {table['data_quality_score']}")
```

**Option 2: Through SQL (SQLite)**
```bash
sqlite3 unity_catalog.db
sqlite> SELECT * FROM tables;
```

**Option 3: Through Dashboard**
```
http://localhost:5000/api/catalog/tables
```

---

## 🐍 Main Python Files: What They Do

### 1. **demo.py** - Data Setup & Initialization

**Purpose**: Creates sample data and initializes the entire system

**What It Does**:
```
┌─────────────────────────────────────┐
│ demo.py                             │
├─────────────────────────────────────┤
│ 1. setup_sample_data()              │
│    └─ Registers 6 tables            │
│    └─ Sets quality scores           │
│    └─ Logs costs                    │
│                                     │
│ 2. setup_dlt_pipelines()            │
│    └─ Creates 3 DLT pipelines       │
│    └─ Bronze (raw data)             │
│    └─ Silver (cleaned)              │
│    └─ Gold (aggregated)             │
│                                     │
│ 3. setup_workflows()                │
│    └─ Creates 2 workflows           │
│    └─ Daily data ingestion          │
│    └─ Hourly analytics              │
│                                     │
│ 4. initialize_agents()              │
│    └─ Creates 8 AI agents           │
│    └─ Runs them once                │
│    └─ Displays results              │
└─────────────────────────────────────┘
```

**Key Functions**:
```python
setup_sample_data()      # Creates 6 Unity Catalog tables
setup_dlt_pipelines()    # Creates Bronze/Silver/Gold pipelines
setup_workflows()        # Creates scheduled workflows
setup_costs()            # Logs DBU costs
run_agents()             # Executes all 8 agents once
print_metrics()          # Displays final metrics
```

**When to Run**:
```bash
python demo.py
```

**Output Example**:
```
[DATA] Setting up sample data...
  OK Registered main.analytics.users
  OK Registered main.analytics.transactions
  OK Registered main.analytics.events
  OK Registered main.analytics.products
  OK Registered main.raw.web_logs
  OK Registered main.raw.api_calls

[PIPELINES] Setting up DLT pipelines...
  OK Created pipeline: bronze_ingestion
  OK Created pipeline: silver_transformation
  OK Created pipeline: gold_aggregation

[AGENTS] Running AI agents...
✓ GovernanceAgent: Reviewed 6 tables
✓ DataQualityAgent: Found 4 quality issues
...
```

---

### 2. **dashboard_api.py** - REST API Backend

**Purpose**: Serves the web dashboard and manages agent execution

**What It Does**:
```
┌─────────────────────────────────────┐
│ dashboard_api.py                    │
├─────────────────────────────────────┤
│ RESPONSIBILITIES:                   │
│ • Serve dashboard.html at root      │
│ • Expose 11 REST API endpoints      │
│ • Run agents in background          │
│ • Return results to dashboard       │
│ • Handle CORS for browser access    │
└─────────────────────────────────────┘

ENDPOINTS PROVIDED:
├── GET /                       (serve dashboard HTML)
├── GET /api/health             (server status)
├── GET /api/overview           (metrics overview)
├── GET /api/catalog/tables     (list tables)
├── GET /api/dlt/pipelines      (list pipelines)
├── GET /api/dlt/lineage        (data lineage)
├── GET /api/workflows          (list workflows)
├── GET /api/costs              (cost analysis)
├── GET /api/agents/status      (agent status)
├── POST /api/agents/run        (trigger agents)
├── GET /api/agents/results     (agent execution results)
├── GET /api/events             (event log)
├── GET /api/recommendations    (optimization tips)
└── GET /api/dashboard-data     (ALL data at once)
```

**Key Functionality**:

```python
# 1. Initialize agents at startup
try:
    governance, delta_opt, spark_opt, cost_mgmt, 
    data_quality, dlt_pipeline, workflow_orch, 
    orchestrator = initialize_agents()
except Exception as e:
    print(f"Warning: Agent initialization failed: {e}")

# 2. Serve dashboard HTML
@app.route('/', methods=['GET'])
def serve_dashboard():
    # Returns dashboard.html with all CSS/JS embedded

# 3. Run agents in background thread (non-blocking)
@app.route('/api/agents/run', methods=['POST'])
def run_agents():
    if agent_running:
        return {"status": "already_running"}, 202
    
    thread = threading.Thread(target=_run_agents_background, daemon=True)
    thread.start()
    return {"status": "started"}, 202  # Return immediately!

# 4. Provide data endpoints
@app.route('/api/dashboard-data', methods=['GET'])
def get_dashboard_data():
    return {
        "overview": {...},
        "costs": {...},
        "agents": [...],
        "recent_events": [...],
        "recommendations": [...]
    }

# 5. Start Flask server
if __name__ == '__main__':
    app.run(debug=False, port=5000, host='0.0.0.0', use_reloader=False)
```

**When to Run**:
```bash
python dashboard_api.py
# Then open: http://localhost:5000
```

**Key Features**:
- Non-blocking execution (202 Accepted)
- Per-agent error handling
- Thread-safe database access
- CORS enabled for browser
- Real-time metrics aggregation

---

### 3. **agents.py** - AI Agent Definitions

**Purpose**: Defines 8 specialized AI agents with agentic loops

**What It Does**:
```
┌─────────────────────────────────────┐
│ agents.py                           │
├─────────────────────────────────────┤
│ Base Agent Class:                   │
│ ├─ think()          (Use Claude)    │
│ ├─ act()            (Record action) │
│ ├─ decide()         (Make decision) │
│ └─ get_status()     (Report status) │
│                                     │
│ 8 Specialized Agents:               │
│ ├─ GovernanceAgent      (PII, access)
│ ├─ DeltaOptimization    (Tables)    │
│ ├─ SparkQueryOptimizer  (Jobs)      │
│ ├─ CostManagement       (Costs)     │
│ ├─ DataQuality          (Quality)   │
│ ├─ DLTPipeline          (Pipelines) │
│ ├─ WorkflowOrchestrator (Workflows) │
│ └─ OrchestratorAgent    (Strategy)  │
└─────────────────────────────────────┘
```

**Agentic Loop Pattern**:

```python
class Agent:
    def think(self, prompt):
        # Step 1: Use Claude AI to reason
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=500,
            system=f"You are {self.name}, a {self.role}...",
            messages=self.conversation_history
        )
        return response.content[0].text
    
    def act(self, action):
        # Step 4: Execute the action
        self.last_action = action
        self.last_action_time = datetime.now().isoformat()
        workspace_state.record_event("agent_action", action, self.name)
        return {"status": "executed", "action": action}
    
    def get_status(self):
        # Report current status
        return {
            "name": self.name,
            "role": self.role,
            "last_action": self.last_action,
            "decisions_made": len(self.decisions)
        }
```

**Each Agent Executes This Loop**:

```
OBSERVE: Read current state
  ↓
THINK: "Claude, given state X, what should we do?"
  ↓
DECIDE: Claude recommends actions
  ↓
ACT: Execute the decisions
  ↓
LEARN: Store results for future reference
  ↓
REPEAT: Do it again every 5 minutes
```

**Example: CostManagementAgent**

```python
class CostManagementAgent(Agent):
    def analyze_costs(self):
        # 1. OBSERVE
        total_cost = cost_tracker.get_total_cost()
        breakdown = cost_tracker.get_cost_breakdown()
        
        # 2. THINK
        prompt = f"Total DBU cost this week: ${total_cost}. 
                   Breakdown: {breakdown}. 
                   What's costing the most?"
        analysis = self.think(prompt)  # <- Uses Claude AI
        
        # 3. DECIDE & ACT
        savings = total_cost * 0.15  # Suggest 15% savings
        self.act(f"Identified ${savings:.2f} in potential cost savings")
        
        # 4. LEARN & RETURN
        return {
            "agent": "CostManagementAgent",
            "total_cost_7days": f"${total_cost:.2f}",
            "potential_savings": f"${savings:.2f}",
            "analysis": analysis
        }
```

---

### 4. **databricks_mock.py** - Data Storage Layer

**Purpose**: Simulates Databricks environment with databases

**What It Does**:
```
┌─────────────────────────────────────┐
│ databricks_mock.py                  │
├─────────────────────────────────────┤
│ UnityDatalog (SQLite)               │
│ └─ Metadata storage                 │
│    ├─ Table registration            │
│    ├─ Classification (PII, etc)     │
│    ├─ Quality scores                │
│    └─ Access logs                   │
│                                     │
│ DeltaLake (DuckDB)                  │
│ └─ Analytics data storage           │
│    ├─ Table statistics              │
│    ├─ Row counts                    │
│    └─ Optimization simulation       │
│                                     │
│ CostTracker (SQLite)                │
│ └─ Cost tracking                    │
│    ├─ DBU cost logging              │
│    ├─ Cost breakdown                │
│    └─ Cost aggregation              │
│                                     │
│ WorkspaceState (In-Memory)          │
│ └─ Current system metrics           │
│    ├─ Table count                   │
│    ├─ Pipeline count                │
│    ├─ Workflow count                │
│    └─ Event log                     │
└─────────────────────────────────────┘
```

**Database Files Created**:

```
unity_catalog.db        ← 6 tables registered here
delta_lake.duckdb       ← Analytics queries run here
cost_tracking.db        ← Cost logs stored here
```

**Example Usage**:

```python
from databricks_mock import unity_catalog, delta_lake, cost_tracker, workspace_state

# Get all tables
tables = unity_catalog.get_tables()  # Returns list of 6 tables

# Get table statistics
stats = delta_lake.get_table_stats("users")  # Returns {"table": "users", "rows": 100}

# Track costs
cost_tracker.log_cost("compute", "cluster_1", 50.0)
total = cost_tracker.get_total_cost()  # Returns total DBU cost for 7 days

# Record events
workspace_state.record_event("agent_action", "Optimized table X", "DeltaOptimizationAgent")
events = workspace_state.get_events(20)  # Get last 20 events
```

---

### 5. **dlt_pipelines.py** - Pipeline Management

**Purpose**: Simulates DLT (Delta Live Tables) pipelines

**What It Does**:
```
┌─────────────────────────────────────┐
│ dlt_pipelines.py                    │
├─────────────────────────────────────┤
│ PipelineManager:                    │
│ ├─ create_pipeline()    (new pipel) │
│ ├─ list_pipelines()     (all)       │
│ ├─ detect_issues()      (problems)  │
│ ├─ get_lineage()        (data flow) │
│ └─ suggest_optimizations()          │
│                                     │
│ DLTPipeline Class:                  │
│ ├─ Bronze tier (raw data)           │
│ ├─ Silver tier (clean data)         │
│ ├─ Gold tier (aggregated)           │
│ └─ Table lineage tracking           │
└─────────────────────────────────────┘
```

**3 Sample Pipelines Created** (by demo.py):

```
1. bronze_ingestion
   └─ raw_users → raw_transactions
   └─ Purpose: Ingest raw data

2. silver_transformation
   └─ cleaned_users → cleaned_transactions
   └─ Purpose: Clean and validate

3. gold_aggregation
   └─ user_metrics → revenue_dashboard
   └─ Purpose: Aggregate for business use
```

---

### 6. **workflows.py** - Job Orchestration

**Purpose**: Simulates Databricks Workflows (scheduled jobs)

**What It Does**:
```
┌─────────────────────────────────────┐
│ workflows.py                        │
├─────────────────────────────────────┤
│ WorkflowScheduler:                  │
│ ├─ create_workflow()    (new job)   │
│ ├─ trigger_workflow()   (run now)   │
│ ├─ list_workflows()     (all)       │
│ ├─ detect_issues()      (failures)  │
│ └─ suggest_optimizations()          │
│                                     │
│ Workflow Class:                     │
│ ├─ Tasks with dependencies          │
│ ├─ Cron scheduling                  │
│ ├─ Job execution tracking           │
│ └─ Failure and retry handling       │
└─────────────────────────────────────┘
```

**2 Sample Workflows Created** (by demo.py):

```
1. daily_data_ingestion (0 1 * * * = 1 AM daily)
   ├─ extract_sources
   ├─ validate_data (depends on extract)
   └─ load_warehouse (depends on validate)

2. hourly_analytics (0 * * * * = every hour)
   ├─ compute_metrics
   ├─ update_dashboards (depends on metrics)
   └─ alert_anomalies (depends on dashboards)
```

---

### 7. **dashboard.html** - Web Interface

**Purpose**: Serves the visual dashboard to users

**What It Does**:
```
┌─────────────────────────────────────┐
│ dashboard.html                      │
├─────────────────────────────────────┤
│ HTML Structure:                     │
│ ├─ Header with buttons              │
│ ├─ Metrics cards (6)                │
│ ├─ Agent status cards (8)           │
│ ├─ Recommendations section          │
│ ├─ Recent events feed               │
│ └─ Auto-refresh mechanism (10s)     │
│                                     │
│ JavaScript Functions:               │
│ ├─ runAgents()    (trigger run)     │
│ ├─ refreshDashboard() (load data)   │
│ └─ setInterval() (auto-refresh)     │
└─────────────────────────────────────┘
```

**Dashboard Features**:
- Real-time metrics
- Agent status cards
- Optimization recommendations
- Event log
- Cost breakdown
- Non-blocking "Run All Agents" button

---

## 🔄 How Files Work Together

### Startup Sequence

```
1. User runs: python demo.py
   ├─ Calls: setup_sample_data()
   │  └─ Creates 6 tables in unity_catalog.db
   ├─ Calls: setup_dlt_pipelines()
   │  └─ Creates 3 pipelines
   ├─ Calls: setup_workflows()
   │  └─ Creates 2 workflows
   └─ Calls: run_agents()
      └─ All 8 agents execute once

2. User runs: python dashboard_api.py
   ├─ Imports demo data (already created)
   ├─ Initializes 8 agents
   ├─ Starts Flask server
   └─ Waits for HTTP requests

3. User opens: http://localhost:5000
   ├─ dashboard.html loads
   ├─ JavaScript calls /api/dashboard-data
   ├─ Gets all metrics, agents, events
   └─ Displays in real-time dashboard

4. User clicks: "Run All Agents"
   ├─ Calls: POST /api/agents/run
   ├─ dashboard_api.py starts background thread
   ├─ Thread calls: _run_agents_background()
   │  ├─ Calls: governance.monitor_access()
   │  ├─ Calls: delta_opt.optimize_tables()
   │  ├─ Calls: spark_opt.optimize_jobs()
   │  ├─ ... (all 8 agents)
   │  └─ Each agent:
   │     ├─ Observes state (from databases)
   │     ├─ Thinks (uses Claude AI)
   │     ├─ Decides
   │     ├─ Acts (records in workspace_state)
   │     └─ Learns (stores decisions)
   │
   └─ Dashboard auto-refreshes after 5 seconds
      └─ Shows results
```

---

## 📊 Data Flow Diagram

```
demo.py
  ↓
  ├─→ databricks_mock.py
  │   ├─ Creates unity_catalog.db (6 tables)
  │   ├─ Creates delta_lake.duckdb (analytics)
  │   ├─ Creates cost_tracking.db (costs)
  │   └─ Creates WorkspaceState (in-memory)
  │
  ├─→ dlt_pipelines.py
  │   └─ Creates 3 pipelines (stored in memory)
  │
  ├─→ workflows.py
  │   └─ Creates 2 workflows (stored in memory)
  │
  └─→ agents.py
      ├─ Reads from databases
      ├─ Calls Claude AI
      └─ Writes to WorkspaceState


dashboard_api.py
  ↓
  ├─ Reads from databases (via databricks_mock.py)
  │
  ├─ Serves dashboard.html
  │
  └─ Provides REST API (/api/*)
      ↓
      dashboard.html
      ├─ JavaScript calls /api/dashboard-data
      ├─ Gets:
      │  ├─ Tables (from unity_catalog.db)
      │  ├─ Pipelines (from memory)
      │  ├─ Workflows (from memory)
      │  ├─ Costs (from cost_tracking.db)
      │  ├─ Events (from WorkspaceState)
      │  └─ Agents status
      │
      └─ Displays in browser
```

---

## 🎯 Quick Reference: What Each File Does

| File | Purpose | Creates | Reads | Writes |
|------|---------|---------|-------|--------|
| **demo.py** | Setup | 6 tables, 3 pipelines, 2 workflows | Nothing | Everything |
| **dashboard_api.py** | REST API | REST endpoints | All databases | Logs only |
| **agents.py** | AI Logic | 8 agents | Databases | Events, decisions |
| **databricks_mock.py** | Data Storage | SQLite/DuckDB files | Databases | Databases |
| **dlt_pipelines.py** | Pipelines | Pipeline objects | Databases | Pipeline state |
| **workflows.py** | Jobs | Workflow objects | Databases | Workflow state |
| **dashboard.html** | UI | HTML/CSS/JS | /api/* endpoints | Nothing (read-only) |

---

**Last Updated**: May 21, 2026
