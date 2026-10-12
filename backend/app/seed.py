from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class StudentRecord:
    student_id: str
    name: str
    department: str
    study_year: int
    dataset_id: str = "demo"
    cohort: str = "default"
    mentor_id: str | None = None
    attendance: dict[str, Any] = field(default_factory=dict)
    academic: dict[str, Any] = field(default_factory=dict)
    lms: dict[str, Any] = field(default_factory=dict)
    placement: dict[str, Any] = field(default_factory=dict)
    skills: dict[str, Any] = field(default_factory=dict)
    engagement: dict[str, Any] = field(default_factory=dict)
    feedback: list[dict[str, Any]] = field(default_factory=list)
    interventions: list[dict[str, Any]] = field(default_factory=list)
    score_history: list[dict[str, Any]] = field(default_factory=list)
    risk_history: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ImportBatch:
    import_id: str
    source: str
    status: str
    accepted: list[dict[str, Any]] = field(default_factory=list)
    rejected: list[dict[str, Any]] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
