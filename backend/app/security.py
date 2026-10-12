from __future__ import annotations

from typing import Annotated, Any

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.app.config import APP_TITLE, LOCAL_DEMO_AUTH_BYPASS, APP_ENV
from backend.app.role_policy import get_policy_summary
from backend.app.role_policy import get_user_claims_from_request
from backend.app.security import build_demo_user_map, generate_demo_token
from backend.app.seed import student_csv_template
from backend.app.service import (
    audit_view,
    create_intervention,
    csv_template,
    get_dashboard_summary,
    get_student,
    import_preview,
    list_interventions,
    list_student_summaries,
    recompute_student,
    seed_students,
    submit_import,
)

app = FastAPI(title=APP_TITLE)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def current_user(request: Request, authorization: str | None = Header(default=None, alias="Authorization")) -> dict[str, Any]:
    try:
        claims = get_user_claims_from_request(authorization)
    except PermissionError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    return claims


class DemoTokenRequest(BaseModel):
    user_id: str = Field(..., min_length=1)
    role: str = Field(..., min_length=1)
    department: str | None = None


@app.get("/health")
def health() -> dict[str, Any]:
    return {"status": "ok", "app_env": APP_ENV, "local_demo_auth_bypass": LOCAL_DEMO_AUTH_BYPASS}


@app.get("/api/auth/role-matrix")
def role_matrix() -> dict[str, Any]:
    return get_policy_summary()


@app.post("/api/auth/local-demo-token")
def local_demo_token(payload: DemoTokenRequest) -> dict[str, Any]:
    if APP_ENV != "local":
        raise HTTPException(status_code=403, detail="Local auth tokens are disabled outside local mode.")
    token = generate_demo_token(payload.user_id, payload.role, payload.department)
    return {"token": token, "user_id": payload.user_id, "role": payload.role}


@app.get("/api/auth/claims")
def auth_claims(user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    return user


@app.get("/api/dashboard/overview")
def dashboard_overview(user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    return get_dashboard_summary()


@app.get("/api/students")
def students(user: dict[str, Any] = Depends(current_user)) -> list[dict[str, Any]]:
    return list_student_summaries()


@app.get("/api/students/{student_id}")
def student_profile(student_id: str, user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    student = get_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.post("/api/setup/seed")
def seed_endpoint(user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    return seed_students()


@app.post("/api/students/{student_id}/recompute")
def recompute_endpoint(student_id: str, user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    student = recompute_student(student_id)
    return {"student_id": student_id, "status": "recomputed", "score": student["score"]}


@app.get("/api/imports/template")
def import_template() -> str:
    return student_csv_template()


@app.post("/api/imports/preview")
def import_preview_endpoint(payload: dict[str, str], user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    csv_content = payload.get("csv")
    if not csv_content:
        raise HTTPException(status_code=400, detail="CSV content required")
    return import_preview(csv_content, user)


@app.post("/api/imports/submit")
def import_submit(payload: dict[str, str], user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    import_id = payload.get("import_id")
    if not import_id:
        raise HTTPException(status_code=400, detail="import_id required")
    return submit_import(import_id, user)


@app.get("/api/interventions")
def interventions(user: dict[str, Any] = Depends(current_user)) -> list[dict[str, Any]]:
    return list_interventions()


@app.post("/api/interventions")
def create_intervention_endpoint(payload: dict[str, Any], user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    return create_intervention(payload, user)


@app.get("/api/audit")
def audit(user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    return audit_view()


@app.get("/api/seeded")
def seeded() -> dict[str, Any]:
    return {"status": "ok"}
