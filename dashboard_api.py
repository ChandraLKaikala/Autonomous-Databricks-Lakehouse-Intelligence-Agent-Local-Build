"""Flask API backend for the Databricks Agent System Dashboard"""
from flask import Flask, jsonify, request, send_from_directory, render_template_string
from flask_cors import CORS
from databricks_mock import unity_catalog, delta_lake, cost_tracker, workspace_state
from dlt_pipelines import pipeline_manager
from workflows import workflow_scheduler
from agents import initialize_agents
import json
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Initialize agents with error handling
try:
    governance, delta_opt, spark_opt, cost_mgmt, data_quality, dlt_pipeline, workflow_orch, orchestrator = initialize_agents()
except Exception as e:
    print(f"Warning: Agent initialization failed: {e}")
    governance = delta_opt = spark_opt = cost_mgmt = data_quality = dlt_pipeline = workflow_orch = orchestrator = None

# Store agent results
agent_results = {}

@app.route('/', methods=['GET'])
def serve_dashboard():
    """Serve the dashboard HTML"""
    try:
        # Get absolute path to dashboard.html
        dashboard_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dashboard.html')
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        return html_content, 200, {'Content-Type': 'text/html; charset=utf-8'}
    except Exception as e:
        return f"Error loading dashboard: {str(e)}", 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/api/overview', methods=['GET'])
def overview():
    """Get system overview"""
    tables = unity_catalog.get_tables()
    pipelines = pipeline_manager.list_pipelines()
    workflows = workflow_scheduler.list_workflows()

    return jsonify({
        "workspace_metrics": workspace_state.metrics,
        "total_tables": len(tables),
        "total_pipelines": len(pipelines),
        "total_workflows": len(workflows),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/catalog/tables', methods=['GET'])
def get_tables():
    """Get all tables in Unity Catalog"""
    tables = unity_catalog.get_tables()
    return jsonify({"tables": tables, "count": len(tables)})

@app.route('/api/dlt/pipelines', methods=['GET'])
def get_pipelines():
    """Get all DLT pipelines"""
    pipelines = pipeline_manager.list_pipelines()
    return jsonify({"pipelines": pipelines, "count": len(pipelines)})

@app.route('/api/dlt/lineage', methods=['GET'])
def get_lineage():
    """Get data lineage graph"""
    lineage = pipeline_manager.get_all_lineage()
    return jsonify(lineage)

@app.route('/api/workflows', methods=['GET'])
def get_workflows():
    """Get all workflows"""
    workflows = workflow_scheduler.list_workflows()
    return jsonify({"workflows": workflows, "count": len(workflows)})

@app.route('/api/costs', methods=['GET'])
def get_costs():
    """Get cost information"""
    total_cost = cost_tracker.get_total_cost()
    breakdown = cost_tracker.get_cost_breakdown()
    return jsonify({
        "total_cost_7days": f"${total_cost:.2f}",
        "breakdown": breakdown,
        "potential_savings": f"${workspace_state.metrics['cost_saved']:.2f}"
    })

@app.route('/api/agents/status', methods=['GET'])
def get_agents_status():
    """Get all agents status"""
    agents = [
        governance.get_status(),
        delta_opt.get_status(),
        spark_opt.get_status(),
        cost_mgmt.get_status(),
        data_quality.get_status(),
        dlt_pipeline.get_status(),
        workflow_orch.get_status(),
        orchestrator.get_status()
    ]
    return jsonify({"agents": agents, "count": len(agents)})

@app.route('/api/agents/run', methods=['POST'])
def run_agents():
    """Run all agents and get results"""
    global agent_results

    results = {
        "timestamp": datetime.now().isoformat(),
        "agents": {}
    }

    # Run each agent
    results["agents"]["governance"] = governance.monitor_access()
    results["agents"]["delta_optimization"] = delta_opt.optimize_tables()
    results["agents"]["spark_optimization"] = spark_opt.optimize_jobs()
    results["agents"]["cost_management"] = cost_mgmt.analyze_costs()
    results["agents"]["data_quality"] = data_quality.monitor_quality()
    results["agents"]["dlt_pipelines"] = dlt_pipeline.monitor_pipelines()
    results["agents"]["workflow_orchestration"] = workflow_orch.orchestrate_workflows()
    results["agents"]["orchestrator"] = orchestrator.coordinate()

    agent_results = results
    workspace_state.metrics["total_tables"] = len(unity_catalog.get_tables())
    workspace_state.metrics["total_pipelines"] = len(pipeline_manager.list_pipelines())
    workspace_state.metrics["total_workflows"] = len(workflow_scheduler.list_workflows())

    return jsonify(results)

@app.route('/api/agents/results', methods=['GET'])
def get_agent_results():
    """Get last agent run results"""
    return jsonify(agent_results)

@app.route('/api/events', methods=['GET'])
def get_events():
    """Get workspace events"""
    limit = request.args.get('limit', 50, type=int)
    events = workspace_state.get_events(limit)
    return jsonify({"events": events, "count": len(events)})

@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    """Get optimization recommendations"""
    recommendations = []

    # Governance recommendations
    tables = unity_catalog.get_tables()
    unclassified = [t for t in tables if t.get("classification") == "unclassified"]
    if unclassified:
        recommendations.append({
            "category": "Governance",
            "priority": "high",
            "recommendation": f"Classify {len(unclassified)} unclassified tables",
            "impact": "Security & Compliance"
        })

    # Cost recommendations
    total_cost = cost_tracker.get_total_cost()
    if total_cost > 1000:
        recommendations.append({
            "category": "Cost",
            "priority": "high",
            "recommendation": f"Weekly costs are ${total_cost:.2f}. Consider reserved capacity",
            "impact": f"Save ~${total_cost * 0.2:.2f}/week"
        })

    # Quality recommendations
    low_quality = [t for t in tables if t.get("data_quality_score", 1) < 0.8]
    if low_quality:
        recommendations.append({
            "category": "Data Quality",
            "priority": "medium",
            "recommendation": f"Improve quality on {len(low_quality)} tables",
            "impact": "Reliability & Trust"
        })

    # Pipeline recommendations
    pipelines = pipeline_manager.list_pipelines()
    failing = [p for p in pipelines if p["status"] == "failed"]
    if failing:
        recommendations.append({
            "category": "Pipelines",
            "priority": "high",
            "recommendation": f"Fix {len(failing)} failing pipelines",
            "impact": "Data Availability"
        })

    return jsonify({"recommendations": recommendations, "count": len(recommendations)})

@app.route('/api/dashboard-data', methods=['GET'])
def get_dashboard_data():
    """Get all data needed for dashboard"""
    try:
        tables = unity_catalog.get_tables() if unity_catalog else []
        pipelines = pipeline_manager.list_pipelines() if pipeline_manager else []
        workflows = workflow_scheduler.list_workflows() if workflow_scheduler else []

        return jsonify({
            "overview": {
                "workspace_metrics": workspace_state.metrics,
                "total_tables": len(tables),
                "total_pipelines": len(pipelines),
                "total_workflows": len(workflows)
            },
            "costs": {
                "total_7days": f"${cost_tracker.get_total_cost():.2f}" if cost_tracker else "$0.00",
                "breakdown": cost_tracker.get_cost_breakdown() if cost_tracker else {}
            },
            "agents": [
                governance.get_status() if governance else {},
                delta_opt.get_status() if delta_opt else {},
                spark_opt.get_status() if spark_opt else {},
                cost_mgmt.get_status() if cost_mgmt else {},
                data_quality.get_status() if data_quality else {},
                dlt_pipeline.get_status() if dlt_pipeline else {},
                workflow_orch.get_status() if workflow_orch else {}
            ],
            "recent_events": workspace_state.get_events(20),
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e), "timestamp": datetime.now().isoformat()}), 200

if __name__ == '__main__':
    # Disable auto-reload to prevent file lock issues with DuckDB
    app.run(debug=False, port=5000, host='0.0.0.0', use_reloader=False)
