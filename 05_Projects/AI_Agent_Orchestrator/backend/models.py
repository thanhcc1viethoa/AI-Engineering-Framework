"""Pydantic models. Field names and enums match Requirement.md FR-003/FR-004."""

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    ASSIGNED = "ASSIGNED"
    RUNNING = "RUNNING"
    REVIEW = "REVIEW"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class Priority(str, Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    OPTIONAL = "Optional"


class AssignedAgent(str, Enum):
    ANTIGRAVITY = "antigravity"
    MUSE = "muse"
    PYTHON = "python"
    QA = "qa"
    PUBLISHER = "publisher"


class AgentStatus(str, Enum):
    IDLE = "IDLE"
    BUSY = "BUSY"
    OFFLINE = "OFFLINE"
    ERROR = "ERROR"


class TaskCreate(BaseModel):
    task_name: str
    description: Optional[str] = None
    assigned_agent: AssignedAgent
    priority: Priority = Priority.MEDIUM
    payload: dict[str, Any] = Field(default_factory=dict)
    workflow_id: Optional[str] = None


class Task(BaseModel):
    task_id: str
    task_name: str
    description: Optional[str] = None
    assigned_agent: str
    priority: str
    status: str
    payload: dict[str, Any] = Field(default_factory=dict)
    result: Optional[dict[str, Any]] = None
    error_message: Optional[str] = None
    output_path: Optional[str] = None
    workflow_id: Optional[str] = None
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


class Agent(BaseModel):
    agent_id: str
    name: str
    type: str
    status: str
    capabilities: list[str] = Field(default_factory=list)
    current_task: Optional[str] = None
    last_active: Optional[str] = None
    error_log: Optional[str] = None


class WorkflowCreate(BaseModel):
    workflow_name: str
    goal: str
    steps: Optional[list[TaskCreate]] = None


class Workflow(BaseModel):
    workflow_id: str
    workflow_name: str
    goal: str
    task_ids: list[str]
    status: str
    created_at: str
    completed_at: Optional[str] = None


class SystemStatus(BaseModel):
    agents_total: int
    agents_active: int
    tasks_running: int
    tasks_completed: int
    tasks_failed: int
    videos_created: int
    uptime_seconds: float
