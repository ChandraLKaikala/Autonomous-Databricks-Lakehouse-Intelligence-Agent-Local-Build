"""Demo script - Set up realistic lakehouse and run the agent system"""
from databricks_mock import unity_catalog, delta_lake, cost_tracker, workspace_state
from dlt_pipelines import pipeline_manager, PipelineTable, DLTPipeline
from workflows import workflow_scheduler, Workflow, WorkflowTask, Job
from agents import initialize_agents
import json
from datetime import datetime, timedelta

def setup_sample_data():
    """Create realistic lakehouse data"""
    print("[DATA] Setting up sample data...")

    # Register tables in Unity Catalog
    tables_to_create = [
        ("main", "analytics", "users", "data_team", "pii_data"),
        ("main", "analytics", "transactions", "finance_team", "financial_data"),
        ("main", "analytics", "events", "product_team", "unclassified"),
        ("main", "analytics", "products", "product_team", "public"),
        ("main", "raw", "web_logs", "data_team", "unclassified"),
        ("main", "raw", "api_calls", "platform_team", "unclassified"),
    ]

    for catalog, schema, name, owner, classification in tables_to_create:
        unity_catalog.register_table(catalog, schema, name, owner, classification)
        print(f"  OK Registered {catalog}.{schema}.{name}")

    # Create Delta Lake tables
    sample_data = [
        {"id": i, "name": f"user_{i}", "email": f"user{i}@example.com"}
        for i in range(100)
    ]
    delta_lake.create_table("users", sample_data)
    print("  OK Created Delta table: users")

    # Update quality scores
    unity_catalog.update_quality_score("users", 0.95)
    unity_catalog.update_quality_score("transactions", 0.85)
    unity_catalog.update_quality_score("events", 0.70)

    # Log some costs
    for i in range(7):
        cost_tracker.log_cost("compute", f"cluster_{i}", 50 + (i * 10))
        cost_tracker.log_cost("storage", f"warehouse_{i}", 30 + (i * 5))

    print("  OK Logged sample costs")

def setup_dlt_pipelines():
    """Create sample DLT pipelines"""
    print("\n[PIPELINES] Setting up DLT pipelines...")

    # Bronze pipeline
    bronze = pipeline_manager.create_pipeline("bronze_ingestion", "data_team")
    t1 = bronze.create_table("raw_users", source="s3://data/users")
    t2 = bronze.create_table("raw_transactions", source="s3://data/transactions")
    bronze.set_lineage("raw_transactions", ["raw_users"])
    pipeline_manager.pipelines["bronze_ingestion"] = bronze
    print("  OK Created pipeline: bronze_ingestion")

    # Silver pipeline
    silver = pipeline_manager.create_pipeline("silver_transformation", "analytics_team")
    t3 = silver.create_table("cleaned_users", source="raw_users")
    t4 = silver.create_table("cleaned_transactions", source="raw_transactions")
    silver.set_lineage("cleaned_transactions", ["cleaned_users"])
    pipeline_manager.pipelines["silver_transformation"] = silver
    print("  OK Created pipeline: silver_transformation")

    # Gold pipeline
    gold = pipeline_manager.create_pipeline("gold_aggregation", "business_team")
    t5 = gold.create_table("user_metrics", source="cleaned_users")
    t6 = gold.create_table("revenue_dashboard", source="cleaned_transactions")
    gold.set_lineage("revenue_dashboard", ["user_metrics"])
    pipeline_manager.pipelines["gold_aggregation"] = gold
    print("  OK Created pipeline: gold_aggregation")

def setup_workflows():
    """Create sample workflows"""
    print("\n[WORKFLOWS] Setting up workflows...")

    # Daily data ingestion workflow
    daily_ingest = workflow_scheduler.create_workflow(
        "daily_data_ingestion",
        "data_team",
        "0 1 * * *"  # 1 AM daily
    )

    # Add tasks
    task1 = WorkflowTask("extract_sources", depends_on=[])
    task1.add_job(Job("extract_1", "Extract Users", "spark_python_task", {}))
    task1.add_job(Job("extract_2", "Extract Transactions", "spark_python_task", {}))
    daily_ingest.add_task(task1)

    task2 = WorkflowTask("validate_data", depends_on=["extract_sources"])
    task2.add_job(Job("validate_1", "Validate Quality", "spark_python_task", {}))
    daily_ingest.add_task(task2)

    task3 = WorkflowTask("load_warehouse", depends_on=["validate_data"])
    task3.add_job(Job("load_1", "Load to DW", "spark_python_task", {}))
    daily_ingest.add_task(task3)

    workflow_scheduler.workflows["daily_data_ingestion"] = daily_ingest
    print("  OK Created workflow: daily_data_ingestion")

    # Hourly analytics update
    hourly_update = workflow_scheduler.create_workflow(
        "hourly_analytics",
        "analytics_team",
        "0 * * * *"  # Every hour
    )

    task4 = WorkflowTask("refresh_metrics", depends_on=[])
    task4.add_job(Job("metrics_1", "Recalculate Metrics", "spark_python_task", {}))
    hourly_update.add_task(task4)

    workflow_scheduler.workflows["hourly_analytics"] = hourly_update
    print("  OK Created workflow: hourly_analytics")

def run_demo():
    """Run the complete demo"""
    print("\n" + "="*60)
    print("[DEMO] AUTONOMOUS DATABRICKS LAKEHOUSE INTELLIGENCE AGENT")
    print("="*60)

    # Setup
    setup_sample_data()
    setup_dlt_pipelines()
    setup_workflows()

    # Initialize and run agents
    print("\n[AGENTS] Initializing AI Agents...")
    governance, delta_opt, spark_opt, cost_mgmt, data_quality, dlt_pipeline, workflow_orch, orchestrator = initialize_agents()
    print("  OK All 8 agents initialized")

    # Run agents
    print("\n[RUNNING] Agent Network Execution...")
    print("-" * 60)

    print("\n[1] GOVERNANCE AGENT - Monitoring access and compliance...")
    gov_result = governance.monitor_access()
    print(f"   Tables monitored: {gov_result['tables_monitored']}")
    print(f"   Actions: {len(gov_result['actions'])}")

    print("\n[2] DELTA OPTIMIZATION AGENT - Optimizing tables...")
    delta_result = delta_opt.optimize_tables()
    print(f"   Tables analyzed: {delta_result['tables_analyzed']}")
    print(f"   Optimizations: {len(delta_result['optimizations'])}")

    print("\n[3] SPARK QUERY OPTIMIZER - Analyzing job performance...")
    spark_result = spark_opt.optimize_jobs()
    print(f"   Workflows analyzed: {spark_result['workflows_analyzed']}")
    print(f"   Issues found: {spark_result['issues_found']}")

    print("\n[4] COST MANAGEMENT AGENT - Analyzing costs...")
    cost_result = cost_mgmt.analyze_costs()
    print(f"   Total cost (7 days): {cost_result['total_cost_7days']}")
    print(f"   Potential savings: {cost_result['potential_savings']}")

    print("\n[5] DATA QUALITY AGENT - Monitoring quality...")
    quality_result = data_quality.monitor_quality()
    print(f"   Tables monitored: {quality_result['tables_monitored']}")
    print(f"   Quality alerts: {len(quality_result['quality_alerts'])}")

    print("\n[6] DLT PIPELINE AGENT - Managing pipelines...")
    dlt_result = dlt_pipeline.monitor_pipelines()
    print(f"   Pipelines monitored: {dlt_result['pipelines_monitored']}")
    print(f"   Issues detected: {dlt_result['issues_detected']}")

    print("\n[7] WORKFLOW ORCHESTRATOR - Managing workflows...")
    workflow_result = workflow_orch.orchestrate_workflows()
    print(f"   Workflows managed: {workflow_result['workflows_managed']}")
    print(f"   Workflows triggered: {workflow_result['workflows_triggered']}")

    print("\n[8] ORCHESTRATOR AGENT - Strategic decision making...")
    orchestrator_result = orchestrator.coordinate()
    print(f"   Agents coordinated: {orchestrator_result['agents_coordinated']}")
    print("\n   [ANALYSIS] Strategic Analysis:")
    for line in orchestrator_result['strategic_analysis'].split('\n')[:3]:
        print(f"      {line}")

    # Update final metrics
    workspace_state.metrics['total_tables'] = len(unity_catalog.get_tables())
    workspace_state.metrics['total_pipelines'] = len(pipeline_manager.list_pipelines())
    workspace_state.metrics['total_workflows'] = len(workflow_scheduler.list_workflows())

    # Show final metrics
    print("\n" + "="*60)
    print("[METRICS] FINAL SYSTEM METRICS")
    print("="*60)
    print(f"Total Tables: {workspace_state.metrics['total_tables']}")
    print(f"Total Pipelines: {workspace_state.metrics['total_pipelines']}")
    print(f"Total Workflows: {workspace_state.metrics['total_workflows']}")
    print(f"Quality Alerts: {workspace_state.metrics['quality_alerts']}")
    print(f"Cost Saved (identified): ${workspace_state.metrics['cost_saved']:.2f}")
    print(f"Optimization Recommendations: {workspace_state.metrics['optimization_recommendations']}")

    # Show recent events
    print("\n[EVENTS] Recent Events:")
    events = workspace_state.get_events(5)
    for event in events:
        print(f"  [{event['agent']}] {event['description']}")

    print("\n" + "="*60)
    print("[SUCCESS] DEMO COMPLETE")
    print("="*60)
    print("\n[WEB] Dashboard available at: http://localhost:5000")
    print("[FILES] Open: file:///C:/Users/lokes/Downloads/databricks-agent-system/dashboard.html")
    print("\nTo start the dashboard API:")
    print("  python dashboard_api.py")

if __name__ == "__main__":
    run_demo()
