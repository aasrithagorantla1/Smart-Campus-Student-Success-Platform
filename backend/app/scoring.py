import csv
import io
import json
import random
from datetime import datetime, timezone
from typing import Any


def _weight_map() -> dict[str, float]:
    return {
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
    raw_name = f"Student {index:03d}"
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

    periods = [
        {"period": f"2025-0{m}", "mark": max(35, min(98, academic_base + rng.randint(-12, 12)))} for m in range(1, 7)
    ]
    for p in periods:
        p["attendance"] = max(40, min(99, attendance_base + rng.randint(-18, 14)))
        p["lms"] = max(35, min(100, lms_base + rng.randint(-15, 16)))
        p["placement"] = max(1, min(100, placement_base + rng.randint(-20, 18)))
        p["skills"] = max(30, min(100, skills_base + rng.randint(-16, 18)))
        p["engagement"] = max(30, min(100, engagement_base + rng.randint(-14, 18)))

    risk_signal = "low"
    if index % 5 == 0:
        risk_signal = "medium"
    if index % 9 == 0:
        risk_signal = "high"

    student = {
        "student_id": f"STU-{1000 + index}",
        "name": raw_name,
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
        "feedback": [
            {
                "category": "motivation",
                "sentiment": "positive" if index % 4 else "neutral",
                "message": "Synthetic feedback from the student success sample dataset.",
                "period": periods[0]["period"],
            }
        ],
        "interventions": [
            {
                "intervention_id": f"INT-{index:03d}",
                "student_id": f"STU-{1000 + index}",
                "suggested_action": "Academic support check-in",
                "supporting_evidence": "Synthetic intervention example",
                "owner": f"mentor-{(index % 10) + 1:03d}",
                "status": "Open",
                "due_date": "2025-06-15",
                "review_date": "2025-06-30",
            }
        ],
        "score_history": [],
        "risk_history": [],
        "seed_version": "v1",
        "risk_level": risk_signal,
        "synthetic": True,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    return student


def csv_template_row() -> list[str]:
    return [
        "student_id",
        "department",
        "study_year",
        "reporting_period",
        "academic_mark",
        "attendance_percentage",
        "lms_completion",
        "placement_readiness",
        "skills_score",
        "engagement_score",
    ]


def student_csv_template() -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(csv_template_row())
    writer.writerow(["STU-1001", "Computer Science", "2", "2025-01", "74", "88", "81", "65", "77", "70"])
    writer.writerow(["STU-1002", "Mechanical Engineering", "3", "2025-01", "61", "75", "69", "58", "63", "59"])
    return buffer.getvalue()
