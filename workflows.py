"""Databricks Workflows/Jobs Orchestration Engine"""
from typing import Dict, List, Callable, Optional
from datetime import datetime, timedelta
from enum import Enum
import json

class JobStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Job:
    """Represents a single job/task"""
    def __init__(self, id: str, name: str, task_type: str, config: Dict):
        self.id = id
        self.name = name
        self.task_type = task_type  # "spark_python_task", "pipeline_task", "dbt_task", etc.
        self.config = config
        self.status = JobStatus.PENDING
        self.created_at = datetime.now().isoformat()
        self.started_at = None
        self.ended_at = None
        self.duration_minutes = 0
        self.error = None
        self.retry_count = 0
        self.max_retries = 3

    def run(self) -> bool:
        """Execute the job"""
        self.status = JobStatus.RUNNING
        self.started_at = datetime.now().isoformat()
        try:
            # Simulate job execution
            if "error_rate" in self.config and self.config["error_rate"] > 0:
                import random
                if random.random() < self.config["error_rate"]:
                    raise Exception(f"Job {self.name} failed (simulated error)")

            self.status = JobStatus.SUCCESS
            self.ended_at = datetime.now().isoformat()
            return True
        except Exception as e:
            self.error = str(e)
            if self.retry_count < self.max_retries:
                self.retry_count += 1
                self.status = JobStatus.PENDING
                return self.run()
            else:
                self.status = JobStatus.FAILED
                self.ended_at = datetime.now().isoformat()
                return False

    def get_status(self) -> Dict:
        """Get job status"""
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status.value,
            "task_type": self.task_type,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "duration_minutes": self.duration_minutes,
            "error": self.error,
            "retry_count": self.retry_count
        }

class WorkflowTask:
    """A task in a workflow (can have multiple jobs)"""
    def __init__(self, name: str, depends_on: List[str] = None):
        self.name = name
        self.depends_on = depends_on or []
        self.jobs = []
        self.status = JobStatus.PENDING
        self.completed_at = None

    def add_job(self, job: Job):
        self.jobs.append(job)

    def run(self) -> bool:
        """Run all jobs in task"""
        for job in self.jobs:
            if not job.run():
                self.status = JobStatus.FAILED
                return False
        self.status = JobStatus.SUCCESS
        self.completed_at = datetime.now().isoformat()
        return True

    def get_status(self) -> Dict:
        return {
            "name": self.name,
            "status": self.status.value,
            "jobs": [j.get_status() for j in self.jobs],
            "depends_on": self.depends_on
        }

class Workflow:
    """Databricks Workflow - orchestrates multiple tasks with dependencies"""
    def __init__(self, name: str, owner: str, schedule: str = None):
        self.name = name
        self.owner = owner
        self.schedule = schedule  # Cron expression
        self.tasks = {}
        self.status = JobStatus.PENDING
        self.created_at = datetime.now().isoformat()
        self.last_run = None
        self.run_history = []

    def add_task(self, task: WorkflowTask):
        """Add a task to workflow"""
        self.tasks[task.name] = task

    def get_execution_plan(self) -> List[str]:
        """Get topological order of task execution"""
        executed = set()
        plan = []

        def execute_task(task_name):
            if task_name in executed:
                return
            task = self.tasks.get(task_name)
            if task:
                for dep in task.depends_on:
                    execute_task(dep)
                plan.append(task_name)
                executed.add(task_name)

        for task_name in self.tasks:
            execute_task(task_name)
        return plan

    def run(self) -> Dict:
        """Execute the workflow"""
        self.status = JobStatus.RUNNING
        results = {
            "workflow": self.name,
            "status": "running",
            "timestamp": datetime.now().isoformat(),
            "tasks_executed": [],
            "tasks_failed": [],
            "duration_minutes": 0
        }

        start_time = datetime.now()
        execution_plan = self.get_execution_plan()

        for task_name in execution_plan:
            task = self.tasks[task_name]
            try:
                if task.run():
                    results["tasks_executed"].append(task_name)
                else:
                    results["tasks_failed"].append(task_name)
                    self.status = JobStatus.FAILED
                    break
            except Exception as e:
                results["tasks_failed"].append(task_name)
                self.status = JobStatus.FAILED

        if not results["tasks_failed"]:
            self.status = JobStatus.SUCCESS
            results["status"] = "success"

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds() / 60
        results["duration_minutes"] = round(duration, 2)

        self.last_run = datetime.now().isoformat()
        self.run_history.append(results)
        return results

    def get_status(self) -> Dict:
        """Get workflow status"""
        return {
            "name": self.name,
            "owner": self.owner,
            "status": self.status.value,
            "schedule": self.schedule,
            "created_at": self.created_at,
            "last_run": self.last_run,
            "tasks": [t.get_status() for t in self.tasks.values()],
            "execution_plan": self.get_execution_plan()
        }

class WorkflowScheduler:
    """Manages workflow scheduling and execution"""
    def __init__(self):
        self.workflows = {}
        self.scheduled_runs = {}

    def create_workflow(self, name: str, owner: str, schedule: str = None) -> Workflow:
        """Create a new workflow"""
        workflow = Workflow(name, owner, schedule)
        self.workflows[name] = workflow
        if schedule:
            self.scheduled_runs[name] = {
                "schedule": schedule,
                "last_triggered": None,
                "next_trigger": datetime.now() + timedelta(hours=1)
            }
        return workflow

    def get_workflow(self, name: str) -> Workflow:
        """Get workflow by name"""
        return self.workflows.get(name)

    def list_workflows(self) -> List[Dict]:
        """List all workflows"""
        return [w.get_status() for w in self.workflows.values()]

    def trigger_workflow(self, name: str) -> Dict:
        """Trigger a workflow manually"""
        workflow = self.workflows.get(name)
        if not workflow:
            return {"error": f"Workflow {name} not found"}
        return workflow.run()

    def run_all_workflows(self) -> Dict:
        """Run all workflows"""
        results = {
            "total": len(self.workflows),
            "succeeded": 0,
            "failed": 0,
            "workflows": {}
        }
        for name, workflow in self.workflows.items():
            result = workflow.run()
            results["workflows"][name] = result
            if workflow.status == JobStatus.SUCCESS:
                results["succeeded"] += 1
            else:
                results["failed"] += 1
        return results

    def detect_workflow_issues(self) -> List[Dict]:
        """Detect issues in workflows"""
        issues = []
        for name, workflow in self.workflows.items():
            if workflow.status == JobStatus.FAILED:
                issues.append({
                    "workflow": name,
                    "issue": "Workflow execution failed",
                    "severity": "high"
                })
            # Check for long-running tasks
            for task in workflow.tasks.values():
                if task.status == JobStatus.RUNNING:
                    issues.append({
                        "workflow": name,
                        "task": task.name,
                        "issue": "Task running longer than expected",
                        "severity": "medium"
                    })
        return issues

    def suggest_optimizations(self) -> List[Dict]:
        """Suggest workflow optimizations"""
        suggestions = []
        for name, workflow in self.workflows.items():
            if len(workflow.run_history) > 0:
                avg_duration = sum(r.get("duration_minutes", 0) for r in workflow.run_history) / len(workflow.run_history)
                if avg_duration > 60:
                    suggestions.append({
                        "workflow": name,
                        "suggestion": "Consider parallelizing tasks",
                        "potential_savings_minutes": avg_duration * 0.3,
                        "impact": "medium"
                    })
        return suggestions

# Global workflow scheduler
workflow_scheduler = WorkflowScheduler()
