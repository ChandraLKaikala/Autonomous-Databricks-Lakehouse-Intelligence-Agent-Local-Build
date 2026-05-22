# 🤖 Autonomous Databricks Lakehouse Intelligence Agent System

A production-grade multi-agent AI system that autonomously manages Databricks infrastructure, including Delta Lake, DLT Pipelines, Workflows, Unity Catalog, and cost optimization.

## 🎯 Project Overview

This is a  project built end-to-end in VS Code with:

- **8 Intelligent AI Agents** (using Claude API) that think and make decisions
- **Mock Databricks Environment** (Unity Catalog, Delta Lake, Workflows)
- **DLT Pipelines** with declarative definitions and lineage tracking
- **Workflow Orchestration** with scheduling and dependency management
- **Real-time Dashboard** to visualize agent decisions
- **Cloud-native Architecture** (cloud + data engineering + gen AI + agentic AI)

## 🏗️ Architecture

### Components

1. **Mock Databricks Environment** (`databricks_mock.py`)
   - Unity Catalog (metadata, governance, classification)
   - Delta Lake (using DuckDB)
   - Cost Tracking
   - Workspace State Management

2. **DLT Pipeline System** (`dlt_pipelines.py`)
   - Declarative pipeline definitions
   - Table lineage tracking
   - Quality assertions
   - Pipeline status monitoring

3. **Workflow Orchestration** (`workflows.py`)
   - Job scheduling (cron-like)
   - Task dependencies
   - Failure handling & retries
   - Performance metrics

4. **Multi-Agent System** (`agents.py`)
   - **GovernanceAgent**: Manages Unity Catalog, classification, compliance
   - **DeltaOptimizationAgent**: Optimizes Delta Lake tables
   - **SparkQueryOptimizer**: Optimizes Spark job performance
   - **CostManagementAgent**: Tracks & optimizes DBU costs
   - **DataQualityAgent**: Monitors data quality & anomalies
   - **DLTPipelineAgent**: Manages DLT pipelines
   - **WorkflowOrchestratorAgent**: Orchestrates workflows
   - **OrchestratorAgent**: Coordinates all agents strategically

5. **Dashboard** (`dashboard.html` + `dashboard_api.py`)
   - Real-time metrics visualization
   - Agent status and decisions
   - Pipeline lineage graphs
   - Cost analysis
   - Optimization recommendations
   - Event stream

## 📋 Features

### Data Governance
- ✅ Automatic table classification (PII, financial, etc.)
- ✅ Access logging and compliance tracking
- ✅ Data quality scoring
- ✅ Security alerts

### Pipeline Management
- ✅ DLT pipeline monitoring
- ✅ Automatic issue detection
- ✅ Data lineage tracking (Bronze → Silver → Gold)
- ✅ Quality assertions
- ✅ Freshness checks

### Cost Optimization
- ✅ DBU cost tracking
- ✅ Cost breakdown by resource
- ✅ Optimization recommendations
- ✅ Savings identification

### Workflow Orchestration
- ✅ Job scheduling
- ✅ Dependency management
- ✅ Failure detection & retry logic
- ✅ Performance optimization

### AI-Powered Intelligence
- ✅ Agentic reasoning using Claude API
- ✅ Multi-agent coordination
- ✅ Strategic decision making
- ✅ Continuous learning from actions

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Anthropic API key (for Claude)

### Installation

1. **Navigate to project directory**
```bash
cd C:\Users\lokes\Downloads\databricks-agent-system
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set API key**
```bash
$env:ANTHROPIC_API_KEY = "your-api-key-here"
```

### Running the Demo

```bash
python demo.py
```

This will:
- Set up realistic lakehouse data
- Create DLT pipelines (Bronze → Silver → Gold)
- Set up workflows
- Initialize all 8 AI agents
- Run agents through their decision loops
- Display metrics and recommendations

### Starting the Dashboard

```bash
python dashboard_api.py
```

Then open `dashboard.html` in your browser:
```
http://localhost:5000
```

## 📊 What You'll See

### In Terminal (Demo Output)
```
🚀 AUTONOMOUS DATABRICKS LAKEHOUSE INTELLIGENCE AGENT DEMO
============================================================

📊 Setting up sample data...
  ✓ Registered main.analytics.users
  ✓ Registered main.analytics.transactions
  ...

🔄 Setting up DLT pipelines...
  ✓ Created pipeline: bronze_ingestion
  ✓ Created pipeline: silver_transformation
  ✓ Created pipeline: gold_aggregation

⚙️ Setting up workflows...
  ✓ Created workflow: daily_data_ingestion
  ✓ Created workflow: hourly_analytics

🤖 Initializing AI Agents...

⚡ Running Agent Network...
1️⃣ GOVERNANCE AGENT - Monitoring access and compliance...
2️⃣ DELTA OPTIMIZATION AGENT - Optimizing tables...
3️⃣ SPARK QUERY OPTIMIZER - Analyzing job performance...
...

📊 FINAL SYSTEM METRICS
Total Tables: 6
Total Pipelines: 3
Total Workflows: 2
Quality Alerts: 1
Cost Saved (identified): $152.50
```

### In Dashboard
- Real-time metrics (tables, pipelines, workflows, costs)
- Agent status cards showing what each agent is doing
- Optimization recommendations prioritized by impact
- Live event stream of agent actions
- Cost breakdown and potential savings
- Data lineage visualization

## 🧠 How Agents Work

Each agent uses an **agentic loop**:

1. **Observe**: Gather current state (tables, pipelines, workflows, metrics)
2. **Think**: Use Claude API to analyze and reason
3. **Decide**: Determine optimal actions
4. **Act**: Execute decisions and track outcomes
5. **Learn**: Store results for future decisions

### Example: Cost Management Agent

```python
# Observe: Current costs
total_cost = $1,250 (7 days)
breakdown = {"compute": $750, "storage": $500}

# Think: Ask Claude
"Total costs are $1,250/week. Compute is our biggest expense at $750.
What cost optimizations would save the most?"

# Claude Response:
"Right-size clusters (save 20%), use reserved capacity (save 15%),
enable intelligent caching (save 10%)"

# Decide: Prioritize actions
→ Implement cluster right-sizing (high impact, low risk)
→ Propose reserved capacity (medium impact, requires approval)

# Act: Execute optimization
✓ Updated cluster config
→ Identified $187.50 in savings
```

## 📁 Project Structure

```
databricks-agent-system/
├── databricks_mock.py          # Mock Databricks environment
├── dlt_pipelines.py            # DLT Pipeline system
├── workflows.py                # Workflow orchestration
├── agents.py                   # Multi-agent system
├── dashboard_api.py            # Flask API backend
├── dashboard.html              # Frontend dashboard
├── demo.py                     # Demo script
├── requirements.txt            # Dependencies
└── README.md                   # This file
```

## 🔧 API Endpoints

All endpoints available at `http://localhost:5000/api/`:

- `GET /health` - Health check
- `GET /overview` - System overview
- `GET /catalog/tables` - List all tables
- `GET /dlt/pipelines` - List DLT pipelines
- `GET /dlt/lineage` - Get data lineage graph
- `GET /workflows` - List workflows
- `GET /costs` - Cost analysis
- `GET /agents/status` - Agent statuses
- `POST /agents/run` - Run all agents
- `GET /events` - Recent events
- `GET /recommendations` - Optimization recommendations
- `GET /dashboard-data` - All data for dashboard

## 🎓 Learning Outcomes

This project demonstrates:

1. **Cloud Data Engineering**: Lakehouse architecture, DLT, Workflows
2. **Generative AI**: Claude API, agentic reasoning, multi-turn conversations
3. **Agentic AI**: Agent loops, decision making, coordination
4. **System Design**: Multi-component architecture, real-time dashboards
5. **Enterprise Patterns**: Governance, cost optimization, quality monitoring

## 🚀 Extensibility

To add new capabilities:

1. **Add a new agent**: Extend `Agent` class in `agents.py`
2. **Add a new pipeline**: Use `pipeline_manager.create_pipeline()`
3. **Add a new workflow**: Use `workflow_scheduler.create_workflow()`
4. **Add a new metric**: Extend `workspace_state.metrics`
5. **Update dashboard**: Add new API endpoint and UI component

## 💡 Future Enhancements

- [ ] Real Databricks API integration
- [ ] Machine learning model drift detection
- [ ] Advanced cost forecasting
- [ ] Automated remediation workflows
- [ ] Multi-workspace management
- [ ] Custom alert webhooks
- [ ] Historical trend analysis
- [ ] Predictive optimization



## 🤝 Support

For issues or questions, review the agent logic in `agents.py` or dashboard API in `dashboard_api.py`.

---

**Built with**: Python, Claude API, DuckDB, Flask, Agentic AI

**Status**: Production-grade MVP ready for deployment

**Scale**: Designed for enterprise-scale data infrastructure with 1000+ tables and 100+ pipelines
