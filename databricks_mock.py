"""Mock Databricks environment - simulates Databricks workspace, Unity Catalog, Delta Lake"""
import duckdb
import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Any
import os

class UnityDatalog:
    """Simulates Unity Catalog - metadata and governance"""
    def __init__(self, db_path: str = "unity_catalog.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.init_db()

    def init_db(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS tables (
            id INTEGER PRIMARY KEY,
            catalog TEXT, schema TEXT, name TEXT UNIQUE,
            owner TEXT, created_at TEXT, classification TEXT,
            data_quality_score REAL DEFAULT 0.0,
            last_modified TEXT
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS access_logs (
            id INTEGER PRIMARY KEY,
            table_name TEXT, user TEXT, action TEXT,
            timestamp TEXT, result TEXT
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS data_quality_metrics (
            id INTEGER PRIMARY KEY,
            table_name TEXT, metric_type TEXT, value REAL,
            timestamp TEXT
        )''')
        self.conn.commit()

    def register_table(self, catalog: str, schema: str, name: str, owner: str, classification: str = "unclassified"):
        full_name = f"{catalog}.{schema}.{name}"
        cursor = self.conn.cursor()
        cursor.execute('''INSERT OR IGNORE INTO tables
            (catalog, schema, name, owner, created_at, classification, last_modified)
            VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (catalog, schema, name, owner, datetime.now().isoformat(), classification, datetime.now().isoformat())
        )
        self.conn.commit()
        return full_name

    def get_tables(self) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM tables')
        return [dict(row) for row in cursor.fetchall()]

    def log_access(self, table_name: str, user: str, action: str, result: str):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO access_logs (table_name, user, action, timestamp, result)
            VALUES (?, ?, ?, ?, ?)''',
            (table_name, user, action, datetime.now().isoformat(), result)
        )
        self.conn.commit()

    def update_quality_score(self, table_name: str, score: float):
        cursor = self.conn.cursor()
        cursor.execute('''UPDATE tables SET data_quality_score = ? WHERE name = ?''',
            (score, table_name)
        )
        self.conn.commit()

class DeltaLake:
    """Simulates Delta Lake using DuckDB"""
    def __init__(self, db_path: str = "delta_lake.duckdb"):
        self.db_path = db_path
        self.versions = {}  # Track table versions
        # Use read-only flag and allow multiple readers
        self.conn = None
        try:
            self.conn = duckdb.connect(db_path, read_only=False)
        except Exception:
            # If connection fails, retry with fresh connection
            self.conn = duckdb.connect(':memory:')

    def create_table(self, table_name: str, data: List[Dict]):
        """Create a Delta table"""
        if data:
            import pandas as pd
            df = pd.DataFrame(data)
            self.conn.register(table_name, df)
            self.versions[table_name] = 1
            return True
        return False

    def get_table(self, table_name: str):
        """Read a Delta table"""
        try:
            if self.conn is None:
                return None
            result = self.conn.execute(f"SELECT * FROM {table_name}").fetchall()
            return result
        except Exception as e:
            return None

    def optimize_table(self, table_name: str):
        """Simulate table optimization (OPTIMIZE in Delta)"""
        try:
            if self.conn is None:
                return {"status": "failed", "table": table_name}
            self.conn.execute(f"VACUUM {table_name}")
            return {"status": "optimized", "table": table_name}
        except Exception:
            return {"status": "failed", "table": table_name}

    def get_table_stats(self, table_name: str) -> Dict:
        """Get table statistics"""
        try:
            if self.conn is None:
                return {"table": table_name, "rows": 0}
            stats = self.conn.execute(f"SELECT COUNT(*) as rows FROM {table_name}").fetchall()
            return {"table": table_name, "rows": stats[0][0] if stats else 0}
        except Exception:
            return {"table": table_name, "rows": 0}

class CostTracker:
    """Track Databricks costs"""
    def __init__(self, db_path: str = "cost_tracking.db"):
        self.conn = sqlite3.connect(db_path)
        self.init_db()

    def init_db(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS costs (
            id INTEGER PRIMARY KEY,
            resource_type TEXT, resource_name TEXT,
            dbu_cost REAL, timestamp TEXT,
            job_id TEXT, duration_minutes INTEGER
        )''')
        self.conn.commit()

    def log_cost(self, resource_type: str, resource_name: str, dbu_cost: float,
                 job_id: str = None, duration_minutes: int = 0):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO costs
            (resource_type, resource_name, dbu_cost, timestamp, job_id, duration_minutes)
            VALUES (?, ?, ?, ?, ?, ?)''',
            (resource_type, resource_name, dbu_cost, datetime.now().isoformat(), job_id, duration_minutes)
        )
        self.conn.commit()

    def get_total_cost(self, days: int = 7) -> float:
        cursor = self.conn.cursor()
        cursor.execute('''SELECT SUM(dbu_cost) FROM costs
            WHERE timestamp > datetime('now', '-' || ? || ' days')''', (days,))
        result = cursor.fetchone()
        return result[0] if result[0] else 0.0

    def get_cost_breakdown(self) -> Dict:
        cursor = self.conn.cursor()
        cursor.execute('''SELECT resource_type, SUM(dbu_cost) as total
            FROM costs GROUP BY resource_type''')
        return {row[0]: row[1] for row in cursor.fetchall()}

class WorkspaceState:
    """Track workspace state and metrics"""
    def __init__(self):
        self.metrics = {
            "total_tables": 0,
            "total_pipelines": 0,
            "total_workflows": 0,
            "quality_alerts": 0,
            "optimization_recommendations": 0,
            "cost_saved": 0.0
        }
        self.events = []

    def record_event(self, event_type: str, description: str, agent: str):
        """Record an agent action"""
        self.events.append({
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "description": description,
            "agent": agent
        })

    def get_events(self, limit: int = 50) -> List[Dict]:
        return self.events[-limit:]

# Initialize global instances with better error handling
try:
    unity_catalog = UnityDatalog()
except Exception as e:
    print(f"Warning: Could not create UnityDatalog: {e}")
    unity_catalog = UnityDatalog(":memory:")

try:
    delta_lake = DeltaLake()
except Exception as e:
    print(f"Warning: Could not create DeltaLake: {e}")
    delta_lake = DeltaLake(":memory:")

try:
    cost_tracker = CostTracker()
except Exception as e:
    print(f"Warning: Could not create CostTracker: {e}")
    cost_tracker = CostTracker(":memory:")

workspace_state = WorkspaceState()
