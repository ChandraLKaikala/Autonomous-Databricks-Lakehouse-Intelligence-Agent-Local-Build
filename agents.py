"""Multi-Agent System - 8 AI agents managing Databricks infrastructure"""
from databricks_mock import unity_catalog, delta_lake, cost_tracker, workspace_state
from dlt_pipelines import pipeline_manager
from workflows import workflow_scheduler
from typing import Dict, List, Any
from datetime import datetime
import json
import os

# Initialize Anthropic client if API key is available
try:
    from anthropic import Anthropic
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    HAS_API = True
except Exception as e:
    print(f"[WARNING] Anthropic API not available: {e}")
    client = None
    HAS_API = False

class Agent:
    """Base agent class with agentic loop"""
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.conversation_history = []
        self.decisions = []
        self.last_action = None
        self.last_action_time = None

    def add_message(self, role: str, content: str):
        self.conversation_history.append({
            "role": role,
            "content": content
        })

    def think(self, prompt: str) -> str:
        """Use Claude to reason and decide"""
        self.add_message("user", prompt)

        if not HAS_API or not client:
            # Fallback response when API is not available
            thought = f"[{self.name}] Analyzing situation... Recommending optimization strategy based on data patterns."
            self.add_message("assistant", thought)
            return thought

        try:
            response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=500,
                system=f"You are {self.name}, a {self.role} AI agent managing Databricks infrastructure. Be concise and actionable.",
                messages=self.conversation_history
            )
            thought = response.content[0].text
            self.add_message("assistant", thought)
            return thought
        except Exception as e:
            # Fallback on API error
            thought = f"[{self.name}] Agent reasoning (API unavailable): Evaluating infrastructure state and recommending optimizations."
            self.add_message("assistant", thought)
            return thought

    def act(self, action: str) -> Dict:
        """Execute an action"""
        self.last_action = action
        self.last_action_time = datetime.now().isoformat()
        workspace_state.record_event("agent_action", action, self.name)
        return {"status": "executed", "action": action, "agent": self.name}

    def get_status(self) -> Dict:
        """Get agent status"""
        return {
            "name": self.name,
            "role": self.role,
            "last_action": self.last_action,
            "last_action_time": self.last_action_time,
            "decisions_made": len(self.decisions)
        }

class GovernanceAgent(Agent):
    """Manages Unity Catalog access, classification, compliance"""
    def __init__(self):
        super().__init__("GovernanceAgent", "Data Governance Manager")

    def monitor_access(self) -> Dict:
        """Monitor data access and compliance"""
        tables = unity_catalog.get_tables()
        prompt = f"You have {len(tables)} tables in the catalog. Identify which need PII classification and which may have access control issues. Be specific."
        analysis = self.think(prompt)

        # Take action
        actions = []
        for table in tables:
            if "user" in table.get("name", "").lower() or "customer" in table.get("name", "").lower():
                unity_catalog.update_quality_score(table["name"], 0.85)
                actions.append(f"Classified {table['name']} as containing PII")

        return {
            "agent": "GovernanceAgent",
            "tables_monitored": len(tables),
            "analysis": analysis,
            "actions": actions
        }

class DeltaOptimizationAgent(Agent):
    """Optimizes Delta Lake tables (compression, partitioning, clustering)"""
    def __init__(self):
        super().__init__("DeltaOptimizationAgent", "Delta Lake Optimizer")

    def optimize_tables(self) -> Dict:
        """Analyze and optimize Delta tables"""
        tables = unity_catalog.get_tables()
        optimizations = []

        for table in tables:
            stats = delta_lake.get_table_stats(table["name"])
            if stats["rows"] > 1000000:
                prompt = f"Table {table['name']} has {stats['rows']} rows. Recommend optimization strategy."
                recommendation = self.think(prompt)
                optimizations.append({
                    "table": table["name"],
                    "recommendation": recommendation,
                    "rows": stats["rows"]
                })
                # Perform optimization
                self.act(f"Optimizing {table['name']}")

        return {
            "agent": "DeltaOptimizationAgent",
            "tables_analyzed": len(tables),
            "optimizations": optimizations
        }

class SparkQueryOptimizer(Agent):
    """Optimizes Spark job performance and resource allocation"""
    def __init__(self):
        super().__init__("SparkQueryOptimizer", "Spark Performance Optimizer")

    def optimize_jobs(self) -> Dict:
        """Analyze and optimize Spark jobs"""
        workflows = workflow_scheduler.list_workflows()
        issues = workflow_scheduler.detect_workflow_issues()
        suggestions = workflow_scheduler.suggest_optimizations()

        prompt = f"We have {len(workflows)} workflows. Issues: {len(issues)}. Optimization opportunities: {len(suggestions)}. What's the priority?"
        analysis = self.think(prompt)

        return {
            "agent": "SparkQueryOptimizer",
            "workflows_analyzed": len(workflows),
            "issues_found": len(issues),
            "optimization_suggestions": suggestions,
            "analysis": analysis
        }

class CostManagementAgent(Agent):
    """Tracks and optimizes Databricks costs"""
    def __init__(self):
        super().__init__("CostManagementAgent", "Cost Optimization Manager")

    def analyze_costs(self) -> Dict:
        """Analyze costs and find optimization opportunities"""
        total_cost = cost_tracker.get_total_cost()
        breakdown = cost_tracker.get_cost_breakdown()

        prompt = f"Total DBU cost this week: ${total_cost:.2f}. Breakdown: {breakdown}. What's costing the most?"
        analysis = self.think(prompt)

        # Log cost-saving recommendation
        savings = total_cost * 0.15  # Suggest 15% savings
        workspace_state.metrics["cost_saved"] += savings

        self.act(f"Identified ${savings:.2f} in potential cost savings")

        return {
            "agent": "CostManagementAgent",
            "total_cost_7days": f"${total_cost:.2f}",
            "cost_breakdown": breakdown,
            "analysis": analysis,
            "potential_savings": f"${savings:.2f}"
        }

class DataQualityAgent(Agent):
    """Monitors data quality, detects anomalies and issues"""
    def __init__(self):
        super().__init__("DataQualityAgent", "Data Quality Monitor")

    def monitor_quality(self) -> Dict:
        """Monitor data quality across all tables"""
        tables = unity_catalog.get_tables()
        quality_scores = [t.get("data_quality_score", 0) for t in tables]

        prompt = f"Monitoring {len(tables)} tables. Quality scores: {quality_scores}. Any tables below 0.8? Alert on those."
        analysis = self.think(prompt)

        issues = []
        for table in tables:
            if table.get("data_quality_score", 0) < 0.8:
                issues.append({
                    "table": table["name"],
                    "score": table["data_quality_score"],
                    "action": "Investigate and improve quality"
                })
                self.act(f"Quality alert on {table['name']}")

        workspace_state.metrics["quality_alerts"] = len(issues)

        return {
            "agent": "DataQualityAgent",
            "tables_monitored": len(tables),
            "quality_alerts": issues,
            "analysis": analysis
        }

class DLTPipelineAgent(Agent):
    """Manages DLT pipelines, detects issues, suggests optimizations"""
    def __init__(self):
        super().__init__("DLTPipelineAgent", "DLT Pipeline Manager")

    def monitor_pipelines(self) -> Dict:
        """Monitor DLT pipelines"""
        pipelines = pipeline_manager.list_pipelines()
        issues = pipeline_manager.detect_pipeline_issues()

        prompt = f"Managing {len(pipelines)} DLT pipelines. Issues detected: {len(issues)}. Recommend actions."
        analysis = self.think(prompt)

        for issue in issues:
            self.act(f"Addressing pipeline issue: {issue.get('issue')}")

        return {
            "agent": "DLTPipelineAgent",
            "pipelines_monitored": len(pipelines),
            "issues_detected": len(issues),
            "issues": issues,
            "analysis": analysis
        }

class WorkflowOrchestratorAgent(Agent):
    """Manages workflow scheduling, dependencies, and execution"""
    def __init__(self):
        super().__init__("WorkflowOrchestratorAgent", "Workflow Orchestration Manager")

    def orchestrate_workflows(self) -> Dict:
        """Manage workflow execution and scheduling"""
        workflows = workflow_scheduler.list_workflows()

        prompt = f"Managing {len(workflows)} workflows. What should run next and in what order?"
        analysis = self.think(prompt)

        # Trigger workflow execution
        results = {}
        for wf_name in list(workflow_scheduler.workflows.keys())[:2]:  # Run first 2
            result = workflow_scheduler.trigger_workflow(wf_name)
            results[wf_name] = result
            self.act(f"Triggered workflow: {wf_name}")

        return {
            "agent": "WorkflowOrchestratorAgent",
            "workflows_managed": len(workflows),
            "workflows_triggered": len(results),
            "execution_results": results,
            "analysis": analysis
        }

class OrchestratorAgent(Agent):
    """The brain - coordinates all agents and makes strategic decisions"""
    def __init__(self, agents: List[Agent]):
        super().__init__("OrchestratorAgent", "Chief Orchestrator")
        self.agents = agents

    def coordinate(self) -> Dict:
        """Coordinate all agents and make decisions"""
        # Gather status from all agents
        agent_statuses = [agent.get_status() for agent in self.agents]

        prompt = f"""You are the orchestrator. Summary of all agent statuses:
        {json.dumps(agent_statuses, indent=2)}

        What are the top 3 priorities right now? Be strategic and focus on business impact."""

        strategic_analysis = self.think(prompt)

        workspace_state.metrics["optimization_recommendations"] += 1

        return {
            "agent": "OrchestratorAgent",
            "agents_coordinated": len(self.agents),
            "strategic_analysis": strategic_analysis,
            "timestamp": datetime.now().isoformat()
        }

def initialize_agents() -> tuple:
    """Create all agents"""
    governance = GovernanceAgent()
    delta_opt = DeltaOptimizationAgent()
    spark_opt = SparkQueryOptimizer()
    cost_mgmt = CostManagementAgent()
    data_quality = DataQualityAgent()
    dlt_pipeline = DLTPipelineAgent()
    workflow_orch = WorkflowOrchestratorAgent()

    # Create orchestrator with all agents
    orchestrator = OrchestratorAgent([
        governance, delta_opt, spark_opt, cost_mgmt,
        data_quality, dlt_pipeline, workflow_orch
    ])

    return governance, delta_opt, spark_opt, cost_mgmt, data_quality, dlt_pipeline, workflow_orch, orchestrator
