from __future__ import annotations

import csv
import io
import json
from copy import deepcopy
from typing import Any

from backend.app.config import APP_ENV
from backend.app.role_policy import is_allowed
from backend.app.scoring import WEIGHTS, academic_risk, calculate_score, placement_risk, segment_label
from backend.app.seed import deterministic_student_payload, student_csv_template

STATE = {
    "students": {},
    "imports": {},
    "interventions": {},
    "seeded": False,
    "seed_version": "v1",
}


def seed_students() -> dict[str, Any]:
    if STATE["seeded"]:
        return {"student_count": len(STATE["students"]), "dataset_id": "demo", "seed_version": STATE["seed_version"], "status": "already_seeded"}

    for index in range(1, 151):
        record = deterministic_student_payload(index)
        STATE["students"][record["student_id"]] = record

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


def ensure_authorized_user(user: dict[str, Any], resource: str, action: str, student_id: str | None = None) -> bool:
    role = user.get("role")
    if not role:
        return False
    if not is_allowed(role, resource, action):
        return False

    if student_id:
        student = STATE["students"].get(student_id)
        if not student:
            return False
        if role == "Student" and student["student_id"] != user.get("user_id"):
            return False
        if role == "Faculty or Mentor":
            if student.get("mentor_id") != user.get("user_id"):
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
    if not ensure_authorized_user(user, "student_master", "manage"):
        raise PermissionError("Not authorized")

    for item in batch["accepted"]:
        student_id = item["student_id"]
        if student_id in STATE["students"]:
            student = STATE["students"][student_id]
            for key in ["academic_mark", "attendance_percentage", "lms_completion", "placement_readiness", "skills_score", "engagement_score"]:
                if key in item and item[key] not in (None, ""):
                    if key == "academic_mark":
                        student["academic"]["cgpa"] = float(item[key]) / 25.0
                    elif key == "attendance_percentage":
                        student["attendance"]["overall_percentage"] = float(item[key])
                    elif key == "lms_completion":
                        student["lms"]["module_completion"] = float(item[key])
                    elif key == "placement_readiness":
                        student["placement"]["readiness"] = float(item[key])
                    elif key == "skills_score":
                        student["skills"]["technical"] = float(item[key])
                    elif key == "engagement_score":
                        student["engagement"]["participation_score"] = float(item[key])
    batch["status"] = "processed"
    return {"import_id": import_id, "status": "processed", "accepted_count": len(batch["accepted"]), "rejected_count": len(batch["rejected"])}


def create_intervention(payload: dict[str, Any], user: dict[str, Any]) -> dict[str, Any]:
    if not ensure_authorized_user(user, "intervention", "create_update", payload.get("student_id")):
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


def csv_template() -> str:
    return student_csv_template()


def audit_view() -> dict[str, Any]:
    return {"seed_version": STATE["seed_version"], "students": len(STATE["students"]), "current_imports": len(STATE["imports"])}
