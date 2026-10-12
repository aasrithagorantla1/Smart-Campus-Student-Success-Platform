from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import jwt
from fastapi import Header, HTTPException

from backend.app.config import APP_ENV, COGNITO_APP_CLIENT_ID, COGNITO_ISSUER, JWT_SECRET


def generate_demo_token(user_id: str, role: str, department: str | None = None) -> str:
    payload = {
        "sub": user_id,
        "cognito:username": user_id,
        "role": role,
        "department": department,
        "scope": "smart-campus",
        "aud": COGNITO_APP_CLIENT_ID,
        "iss": COGNITO_ISSUER,
        "token_use": "id",
        "exp": int(datetime.now(timezone.utc).timestamp()) + 3600,
        "iat": int(datetime.now(timezone.utc).timestamp()),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def verify_token(token: str) -> dict[str, Any]:
    if not token:
        raise PermissionError("Missing bearer token")
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=["HS256"],
            audience=COGNITO_APP_CLIENT_ID,
            issuer=COGNITO_ISSUER,
            options={"require": ["exp", "iss", "aud", "token_use", "sub"]},
        )
    except Exception as exc:
        raise PermissionError(f"Invalid token: {exc}")

    if payload.get("token_use") != "id":
        raise PermissionError("Unexpected token use")
    return payload


def build_demo_user_map() -> dict[str, dict[str, Any]]:
    return {
        "admin-001": {"user_id": "admin-001", "role": "College Administrator", "department": "college"},
        "hod-cs": {"user_id": "hod-cs", "role": "HOD", "department": "Computer Science"},
        "mentor-001": {"user_id": "mentor-001", "role": "Faculty or Mentor", "department": "Computer Science"},
        "placement-001": {"user_id": "placement-001", "role": "Placement Officer", "department": "Computer Science"},
        "activity-001": {"user_id": "activity-001", "role": "Activity Coordinator", "department": "Computer Science"},
        "student-001": {"user_id": "student-001", "role": "Student", "department": "Computer Science"},
        "sysadmin-001": {"user_id": "sysadmin-001", "role": "System Administrator", "department": "college"},
    }


def get_user_claims_from_request(auth_header: str | None) -> dict[str, Any]:
    if not auth_header:
        if APP_ENV == "local":
            return {"user_id": "admin-001", "role": "College Administrator", "department": "college"}
        raise PermissionError("Authentication required")

    scheme, _, token = auth_header.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise PermissionError("Bearer token required")

    payload = verify_token(token)
    return {
        "user_id": payload.get("sub"),
        "role": payload.get("role", "Student"),
        "department": payload.get("department"),
        "claims": payload,
    }


def create_auth_dependency():
    def dependency(authorization: str | None = Header(default=None, alias="Authorization")):
        try:
            claims = get_user_claims_from_request(authorization)
        except PermissionError as exc:
            raise HTTPException(status_code=401, detail=str(exc)) from exc
        return claims

    return dependency

__all__ = [
    "generate_demo_token",
    "verify_token",
    "build_demo_user_map",
    "get_user_claims_from_request",
    "create_auth_dependency",
]
