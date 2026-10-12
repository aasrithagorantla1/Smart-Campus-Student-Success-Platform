from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any


WEIGHTS = {
    "academic": 30.0,
    "attendance": 20.0,
    "lms": 15.0,
    "placement": 15.0,
    "skills": 10.0,
    "engagement": 10.0,
}


def is_missing(value: Any) -> bool:
    return value is None or value == "" or value == "N/A"


def clamp(value: float | None, min_value: float = 0.0, max_value: float = 100.0) -> float | None:
    if value is None:
        return None
    return max(min_value, min(max_value, value))


def normalise(value: float | None, low: float = 0.0, high: float = 100.0) -> float | None:
    if value is None:
        return None
    if high <= low:
        return 100.0
    return max(0.0, min(100.0, ((value - low) / (high - low)) * 100.0))


def student_component_values(student: dict[str, Any]) -> dict[str, Any]:
    academic = student.get("academic", {})
    attendance = student.get("attendance", {})
    lms = student.get("lms", {})
    placement = student.get("placement", {})
    skills = student.get("skills", {})
    engagement = student.get("engagement", {})

    return {
        "academic": academic.get("cgpa", None),
        "attendance": attendance.get("overall_percentage", None),
        "lms": lms.get("module_completion", None),
        "placement": placement.get("readiness", None),
        "skills": (skills.get("technical", 0) + skills.get("communication", 0)) / 2 if skills else None,
        "engagement": engagement.get("participation_score", None),
    }


def calculate_score(student: dict[str, Any]) -> dict[str, Any]:
    component_values = student_component_values(student)
    total_weight = 0.0
    covered_weight = 0.0
    contributions = {}
    component_scores = {}

    for key, weight in WEIGHTS.items():
        value = component_values.get(key)
        if is_missing(value):
            continue
        total_weight += weight
        covered_weight += weight
        normalised = clamp(normalise(value, 0.0, 100.0), 0.0, 100.0)
        component_scores[key] = normalised
        contributions[key] = (normalised / 100.0) * weight

    total_applicable = sum(WEIGHTS.values())
    coverage = covered_weight / total_applicable if total_applicable else 0.0

    final_score = sum(contributions.values()) if contributions else 0.0
    final_score = clamp(final_score, 0.0, 100.0)

    if coverage < 0.8:
        status = "Insufficient data"
    elif coverage < 1.0:
        status = "Provisional"
    else:
        status = "Ready"

    return {
        "component_values": component_scores,
        "weights": WEIGHTS,
        "weighted_contributions": contributions,
        "final_score": round(final_score, 2),
        "coverage": round(coverage, 4),
        "status": status,
        "scoring_version": "v1",
        "calculated_at": datetime.now(timezone.utc).isoformat(),
    }


def academic_risk(student: dict[str, Any]) -> dict[str, Any]:
    academic = student.get("academic", {})
    marks = [m.get("mark", 0) for m in academic.get("marks", [])]
    if not marks:
        return {"level": "Insufficient data", "evidence": []}
    avg_mark = sum(marks) / len(marks)
    backlog_count = academic.get("backlogs", 0)
    risk_level = "low"
    if avg_mark < 55 or backlog_count > 1:
        risk_level = "high"
    elif avg_mark < 66 or backlog_count > 0:
        risk_level = "medium"
    evidence = [
        {"observed": f"Average mark {round(avg_mark, 1)}%", "rule": "avg_mark < 66 => medium risk", "period": "latest"},
        {"observed": f"Backlogs: {backlog_count}", "rule": "backlog_count > 1 => high risk", "period": "latest"},
    ]
    return {"level": risk_level, "evidence": evidence}


def placement_risk(student: dict[str, Any]) -> dict[str, Any]:
    placement = student.get("placement", {})
    if not placement.get("applicable", False):
        return {"level": "Not applicable", "evidence": [{"observed": "Placement data not applicable for this cohort", "rule": "missing placement data does not imply poor readiness", "period": "latest"}]}

    readiness = placement.get("readiness")
    if readiness is None:
        return {"level": "Insufficient data", "evidence": [{"observed": "Placement readiness missing", "rule": "missing data is not treated as poor readiness", "period": "latest"}]}
    if readiness < 45:
        risk_level = "high"
    elif readiness < 65:
        risk_level = "medium"
    else:
        risk_level = "low"
    return {
        "level": risk_level,
        "evidence": [{"observed": f"Placement readiness {readiness}%", "rule": "readiness < 45 => high risk", "period": "latest"}],
    }


def segment_label(student: dict[str, Any], score: dict[str, Any]) -> str:
    academic = student.get("academic", {})
    placement = student.get("placement", {})
    attendance = student.get("attendance", {}).get("overall_percentage")
    if score.get("status") == "Insufficient data":
        return "Insufficient data"
    if academic.get("cgpa", 0) >= 3.5 and placement.get("readiness", 0) < 60:
        return "Strong academics, low placement readiness"
    if attendance is not None and attendance < 70 and academic.get("cgpa", 0) < 3.2:
        return "Declining attendance and results"
    if student.get("skills", {}).get("technical", 0) >= 75 and academic.get("cgpa", 0) < 3.0:
        return "Strong skills, academic support required"
    if score.get("final_score", 0) > 65 and student.get("risk_level") == "medium":
        return "Improving after intervention"
    if score.get("final_score", 0) >= 75:
        return "Consistently performing well"
    return "Insufficient data"
