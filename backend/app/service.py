from __future__ import annotations

import csv
import io
import random
from datetime import datetime, timezone
from typing import Any

from backend.app.role_policy import is_allowed

STATE = {
    "students": {},
    "imports": {},
    "interventions": {},
    "seeded": False,
    "seed_version": "v1",
}

WEIGHTS = {
    "academic": 30.0,
    "attendance": 20.0,
    "lms": 15.0,
    "placement": 15.0,
    "skills": 10.0,
    "engagement": 10.0,
}


def deterministic_student_payload(index: int, seed: int = 20240621) -> dict[str, Any]:
    rng = random.Random(seed + index)
    departments = ["Computer Science", "Mechanical Engineering", "Business Analytics"]
    department = departments[index % len(departments)]
    study_year = 1 + (index % 4)
    academic_base = 58 + (index % 38)
    attendance_base = 60 + ((index * 7) % 33)
    lms_base = 50 + ((index * 11) % 44)
    placement_base = 45 + ((index * 5) % 45)
    skills_base = 52 + ((index * 13) % 42)
    engagement_base = 48 + ((index * 17) % 43)

    if index % 10 == 0:
        academic_base = 72
        attendance_base = 55
        placement_base = 35
    if index % 11 == 0:
        attendance_base = 78
        placement_base = 68
    if index % 7 == 0:
        lms_base = 42
        academic_base = 52
    if index % 13 == 0:
        engagement_base = 62

    periods = []
    for period_num in range(1, 7):
        periods.append({
            "period": f"2025-0{period_num}",
            "mark": max(35, min(98, academic_base + rng.randint(-12, 12))),
            "attendance": max(40, min(99, attendance_base + rng.randint(-18, 14))),
            "lms": max(35, min(100, lms_base + rng.randint(-15, 16))),
            "placement": max(1, min(100, placement_base + rng.randint(-20, 18))),
            "skills": max(30, min(100, skills_base + rng.randint(-16, 18))),
            "engagement": max(30, min(100, engagement_base + rng.randint(-14, 18))),
        })

    student = {
        "student_id": f"STU-{1000 + index}",
        "name": f"Student {index:03d}",
        "department": department,
        "study_year": study_year,
        "dataset_id": "demo",
        "cohort": "synthetic",
        "mentor_id": f"mentor-{(index % 10) + 1:03d}",
        "academic": {
            "result_summary": "synthetic academic record",
            "marks": periods,
            "backlogs": 0 if index % 5 else 1,
            "cgpa": round(2.4 + (academic_base / 100) * 2.0, 2),
        },
        "attendance": {
            "overall_percentage": attendance_base,
            "subjects": [
                {"subject": "Programming", "percentage": max(45, min(98, attendance_base + rng.randint(-15, 10)))},
                {"subject": "Mathematics", "percentage": max(45, min(98, attendance_base + rng.randint(-12, 10)))},
                {"subject": "Communication", "percentage": max(40, min(98, attendance_base + rng.randint(-18, 12)))},
            ],
            "trend": "stable" if index % 3 else "declining",
        },
        "lms": {
            "module_completion": max(30, min(100, lms_base + rng.randint(-10, 10))),
            "activity_count": 120 + rng.randint(40, 140),
            "submission_rate": max(30, min(100, lms_base + rng.randint(-5, 12))),
            "reporting_periods": periods,
        },
        "placement": {
            "aptitude": max(25, min(95, placement_base + rng.randint(-12, 12))),
            "coding": max(25, min(95, placement_base + rng.randint(-13, 14))),
            "interview": max(20, min(96, placement_base + rng.randint(-18, 12))),
            "readiness": max(10, min(100, placement_base + rng.randint(-8, 18))),
            "applicable": index % 4 != 0,
        },
        "skills": {
            "technical": max(25, min(100, skills_base + rng.randint(-10, 12))),
            "communication": max(25, min(100, skills_base + rng.randint(-12, 14))),
            "projects": max(30, min(100, skills_base + rng.randint(-10, 15))),
            "certifications": 1 if index % 2 else 0,
        },
        "engagement": {
            "clubs": 1 if index % 3 else 0,
            "events": 2 + rng.randint(0, 5),
            "projects": 1 if index % 4 else 0,
            "volunteering": 1 if index % 6 else 0,
            "participation_score": max(30, min(100, engagement_base + rng.randint(-15, 18))),
        },
        "feedback": [{
            "category": "motivation",
            "sentiment": "positive" if index % 4 else "neutral",
            "message": "Synthetic feedback from the student success sample dataset.",
            "period": periods[0]["period"],
        }],
        "interventions": [{
            "intervention_id": f"INT-{index:03d}",
            "student_id": f"STU-{1000 + index}",
            "suggested_action": "Academic support check-in",
            "supporting_evidence": "Synthetic intervention example",
            "owner": f"mentor-{(index % 10) + 1:03d}",
            "status": "Open",
            "due_date": "2025-06-15",
            "review_date": "2025-06-30",
        }],
        "risk_level": "low",
        "synthetic": True,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    return student


def is_missing(value: Any) -> bool:
    return value is None or value == "" or value == "N/A"


def clamp(value: float | None, minimum: float = 0.0, maximum: float = 100.0) -> float | None:
    if value is None:
        return None
    return max(minimum, min(maximum, value))


def normalise(value: float | None, low: float = 0.0, high: float = 100.0) -> float | None:
    if value is None:
        return None
    if high <= low:
        return 100.0
    return max(0.0, min(100.0, ((value - low) / (high - low)) * 100.0))


def calculate_score(student: dict[str, Any]) -> dict[str, Any]:
    component_values = {
        "academic": student.get("academic", {}).get("cgpa", None),
        "attendance": student.get("attendance", {}).get("overall_percentage", None),
        "lms": student.get("lms", {}).get("module_completion", None),
        "placement": student.get("placement", {}).get("readiness", None),
        "skills": ((student.get("skills", {}).get("technical", 0) or 0) + (student.get("skills", {}).get("communication", 0) or 0)) / 2 if student.get("skills") else None,
        "engagement": student.get("engagement", {}).get("participation_score", None),
    }

    covered_weight = 0.0
    contributions = {}
    component_scores = {}

    for key, weight in WEIGHTS.items():
        value = component_values.get(key)
        if is_missing(value):
            continue
        covered_weight += weight
        score = clamp(normalise(value, 0.0, 100.0), 0.0, 100.0)
        component_scores[key] = score
        contributions[key] = (score / 100.0) * weight

    total_weight = sum(WEIGHTS.values())
    coverage = covered_weight / total_weight if total_weight else 0.0
    final_score = sum(contributions.values()) if contributions else 0.0
    status = "Insufficient data" if coverage < 0.8 else ("Provisional" if coverage < 1.0 else "Ready")

    return {
        "component_values": component_scores,
        "weights": WEIGHTS,
        "weighted_contributions": contributions,
        "final_score": round(clamp(final_score, 0.0, 100.0), 2),
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
    if avg_mark < 55 or backlog_count > 1:
        level = "high"
    elif avg_mark < 66 or backlog_count > 0:
        level = "medium"
    else:
        level = "low"

    return {
        "level": level,
        "evidence": [
            {"observed": f"Average mark {round(avg_mark, 1)}%", "rule": "avg_mark < 66 => medium risk", "period": "latest"},
            {"observed": f"Backlogs: {backlog_count}", "rule": "backlog_count > 1 => high risk", "period": "latest"},
        ],
    }


def placement_risk(student: dict[str, Any]) -> dict[str, Any]:
    placement = student.get("placement", {})
    if not placement.get("applicable", False):
        return {"level": "Not applicable", "evidence": [{"observed": "Placement data not applicable for this cohort", "rule": "missing placement data does not imply poor readiness", "period": "latest"}]}

    readiness = placement.get("readiness")
    if readiness is None:
        return {"level": "Insufficient data", "evidence": [{"observed": "Placement readiness missing", "rule": "missing data is not treated as poor readiness", "period": "latest"}]}

    if readiness < 45:
        level = "high"
    elif readiness < 65:
        level = "medium"
    else:
        level = "low"
    return {"level": level, "evidence": [{"observed": f"Placement readiness {readiness}%", "rule": "readiness < 45 => high risk", "period": "latest"}]}


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


def seed_students() -> dict[str, Any]:
    if STATE["seeded"]:
        return {"student_count": len(STATE["students"]), "dataset_id": "demo", "seed_version": STATE["seed_version"], "status": "already_seeded"}

    for index in range(1, 151):
        student = deterministic_student_payload(index)
        STATE["students"][student["student_id"]] = student
    STATE["seeded"] = True
    return {"student_count": len(STATE["students"]), "dataset_id": "demo", "seed_version": STATE["seed_version"], "status": "seeded"}


def list_student_summaries() -> list[dict[str, Any]]:
    records = []
    for student in STATE["students"].values():
        score = calculate_score(student)
        student["score"] = score
        student["segment"] = segment_label(student, score)
        student["academic_risk"] = academic_risk(student)
        student["placement_risk"] = placement_risk(student)
        records.append({
            "student_id": student["student_id"],
            "name": student["name"],
            "department": student["department"],
            "study_year": student["study_year"],
            "dataset_id": student.get("dataset_id", "demo"),
            "score": score,
            "segment": student["segment"],
            "risk": student["academic_risk"]["level"],
        })
    return records


def get_student(student_id: str) -> dict[str, Any] | None:
    student = STATE["students"].get(student_id)
    if not student:
        return None
    score = calculate_score(student)
    student["score"] = score
    student["segment"] = segment_label(student, score)
    student["academic_risk"] = academic_risk(student)
    student["placement_risk"] = placement_risk(student)
    return student


def recompute_student(student_id: str) -> dict[str, Any]:
    student = get_student(student_id)
    if not student:
        raise KeyError(f"Student not found: {student_id}")
    student["score"] = calculate_score(student)
    student["segment"] = segment_label(student, student["score"])
    student["academic_risk"] = academic_risk(student)
    student["placement_risk"] = placement_risk(student)
    student["updated_at"] = student["score"]["calculated_at"]
    return student


def is_authorized(user: dict[str, Any], resource: str, action: str, student_id: str | None = None) -> bool:
    role = user.get("role")
    if not role or not is_allowed(role, resource, action):
        return False
    if student_id:
        student = STATE["students"].get(student_id)
        if not student:
            return False
        if role == "Student" and student["student_id"] != user.get("user_id"):
            return False
        if role == "Faculty or Mentor" and student.get("mentor_id") != user.get("user_id"):
            return False
    return True


def import_preview(csv_content: str, user: dict[str, Any]) -> dict[str, Any]:
    reader = csv.DictReader(io.StringIO(csv_content))
    accepted = []
    rejected = []
    for row in reader:
        student_id = (row.get("student_id") or "").strip()
        if not student_id:
            rejected.append({"row": row, "error": "Missing student_id"})
            continue
        if student_id not in STATE["students"]:
            rejected.append({"row": row, "error": "Unknown student_id"})
            continue
        accepted.append({**row, "student_id": student_id})

    import_id = f"IMP-{len(STATE['imports']) + 1:04d}"
    STATE["imports"][import_id] = {
        "import_id": import_id,
        "source": "csv",
        "status": "preview",
        "accepted": accepted,
        "rejected": rejected,
        "responsible_user": user.get("user_id"),
    }
    return {"import_id": import_id, "accepted": accepted, "rejected": rejected}


def submit_import(import_id: str, user: dict[str, Any]) -> dict[str, Any]:
    batch = STATE["imports"].get(import_id)
    if not batch:
        raise KeyError("Import not found")
    if not is_authorized(user, "student_master", "manage"):
        raise PermissionError("Not authorized")

    for item in batch["accepted"]:
        student_id = item["student_id"]
        student = STATE["students"].get(student_id)
        if not student:
            continue

        if "academic_mark" in item and item["academic_mark"] not in (None, ""):
            student["academic"]["cgpa"] = float(item["academic_mark"]) / 25.0
        if "attendance_percentage" in item and item["attendance_percentage"] not in (None, ""):
            student["attendance"]["overall_percentage"] = float(item["attendance_percentage"])
        if "lms_completion" in item and item["lms_completion"] not in (None, ""):
            student["lms"]["module_completion"] = float(item["lms_completion"])
        if "placement_readiness" in item and item["placement_readiness"] not in (None, ""):
            student["placement"]["readiness"] = float(item["placement_readiness"])
        if "skills_score" in item and item["skills_score"] not in (None, ""):
            student["skills"]["technical"] = float(item["skills_score"])
        if "engagement_score" in item and item["engagement_score"] not in (None, ""):
            student["engagement"]["participation_score"] = float(item["engagement_score"])

    batch["status"] = "processed"
    return {"import_id": import_id, "status": "processed", "accepted_count": len(batch["accepted"]), "rejected_count": len(batch["rejected"]) }


def create_intervention(payload: dict[str, Any], user: dict[str, Any]) -> dict[str, Any]:
    if not is_authorized(user, "intervention", "create_update", payload.get("student_id")):
        raise PermissionError("Faculty or mentor permissions required")

    intervention = {
        **payload,
        "intervention_id": payload.get("intervention_id", f"INT-{len(STATE['interventions']) + 1:04d}"),
        "status": payload.get("status", "Open"),
        "owner": payload.get("owner", user.get("user_id")),
        "updated_by": user.get("user_id"),
    }
    STATE["interventions"][intervention["intervention_id"]] = intervention
    return intervention


def list_interventions() -> list[dict[str, Any]]:
    return list(STATE["interventions"].values())


def get_dashboard_summary() -> dict[str, Any]:
    students = list_student_summaries()
    department_map: dict[str, int] = {}
    risk_map: dict[str, int] = {}
    for student in students:
        department_map[student["department"]] = department_map.get(student["department"], 0) + 1
        risk_map[student["risk"]] = risk_map.get(student["risk"], 0) + 1
    return {
        "department_counts": department_map,
        "risk_counts": risk_map,
        "students": students,
        "score_average": round(sum(s["score"]["final_score"] for s in students) / max(1, len(students)), 2),
    }


def audit_view() -> dict[str, Any]:
    return {"seed_version": STATE["seed_version"], "students": len(STATE["students"]), "current_imports": len(STATE["imports"]) }


def student_csv_template() -> str:
    lines = [
        "student_id,department,study_year,reporting_period,academic_mark,attendance_percentage,lms_completion,placement_readiness,skills_score,engagement_score",
        "STU-1001,Computer Science,2,2025-01,74,88,81,65,77,70",
        "STU-1002,Mechanical Engineering,3,2025-01,61,75,69,58,63,59",
    ]
    return "\n".join(lines) + "\n"


__all__ = [
    "STATE",
    "WEIGHTS",
    "deterministic_student_payload",
    "calculate_score",
    "academic_risk",
    "placement_risk",
    "segment_label",
    "seed_students",
    "list_student_summaries",
    "get_student",
    "recompute_student",
    "is_authorized",
    "import_preview",
    "submit_import",
    "create_intervention",
    "list_interventions",
    "get_dashboard_summary",
    "audit_view",
    "student_csv_template",
]
