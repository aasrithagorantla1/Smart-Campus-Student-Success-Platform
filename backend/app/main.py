from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.config import APP_ENV, APP_TITLE, LOCAL_DEMO_AUTH_BYPASS
from backend.app.security import build_demo_user_map, create_auth_dependency
from backend.app.service import (
    audit_view,
    create_intervention,
    get_dashboard_summary,
    get_student,
    import_preview,
    list_interventions,
    list_student_summaries,
    recompute_student,
    seed_students,
    submit_import,
)
from backend.app.seed import student_csv_template
from backend.app.role_policy import get_policy_summary

app = FastAPI(title=APP_TITLE)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency for authenticated routes using server-side trust model.
current_user = create_auth_dependency()

@app.get("/health")
def health():
    return {"status": "ok", "app_env": APP_ENV, "local_demo_auth_bypass": LOCAL_DEMO_AUTH_BYPASS}

@app.get("/api/auth/role-matrix")
def role_matrix():
    return get_policy_summary()

@app.get("/api/auth/demo-users")
def demo_users():
    return build_demo_user_map()

@app.get("/api/dashboard/overview")
def dashboard_overview(user=Depends(current_user)):
    return get_dashboard_summary()

@app.get("/api/students")
def students(user=Depends(current_user)):
    return list_student_summaries()

@app.get("/api/students/{student_id}")
def student_profile(student_id: str, user=Depends(current_user)):
    student = get_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.post("/api/setup/seed")
def seed_endpoint(user=Depends(current_user)):
    return seed_students()

@app.post("/api/students/{student_id}/recompute")
def recompute_endpoint(student_id: str, user=Depends(current_user)):
    student = recompute_student(student_id)
    return {"student_id": student_id, "status": "recomputed", "score": student["score"]}

@app.get("/api/imports/template")
def import_template():
    return {"csv": student_csv_template()}

@app.post("/api/imports/preview")
def import_preview_endpoint(payload: dict, user=Depends(current_user)):
    csv_content = payload.get("csv")
    if not csv_content:
        raise HTTPException(status_code=400, detail="CSV content required")
    return import_preview(csv_content, user)

@app.post("/api/imports/submit")
def import_submit(payload: dict, user=Depends(current_user)):
    import_id = payload.get("import_id")
    if not import_id:
        raise HTTPException(status_code=400, detail="import_id required")
    return submit_import(import_id, user)

@app.get("/api/interventions")
def interventions(user=Depends(current_user)):
    return list_interventions()

@app.post("/api/interventions")
def create_intervention_endpoint(payload: dict, user=Depends(current_user)):
    return create_intervention(payload, user)

@app.get("/api/audit")
def audit(user=Depends(current_user)):
    return audit_view()

@app.get("/api/auth/claims")
def auth_claims(user=Depends(current_user)):
    return user

@app.post("/api/auth/local-demo-token")
def local_demo_token(payload: dict):
    if APP_ENV != "local":
        raise HTTPException(status_code=403, detail="Local auth tokens are disabled outside local mode.")
    from backend.app.security import generate_demo_token
    user_id = payload.get("user_id")
    role = payload.get("role")
    department = payload.get("department")
    token = generate_demo_token(user_id or "admin-001", role or "College Administrator", department)
    return {"token": token, "user_id": user_id, "role": role}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
