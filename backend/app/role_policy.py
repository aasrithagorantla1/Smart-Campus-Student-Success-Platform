import json
from pathlib import Path
from typing import Any

from backend.app.config import ROLE_MATRIX_PATH


with open(ROLE_MATRIX_PATH, "r", encoding="utf-8") as file:
    POLICY = json.load(file)

ROLE_PERMISSIONS = {role["role"]: role["permissions"] for role in POLICY["roles"]}


def get_role_permissions(role_name: str) -> list[dict[str, Any]]:
    return ROLE_PERMISSIONS.get(role_name, [])


def is_allowed(role_name: str, resource: str, action: str) -> bool:
    for permission in get_role_permissions(role_name):
        if permission.get("resource") == resource and permission.get("action") == action:
            return True
    return False


def allowed_fields(role_name: str, resource: str, action: str) -> list[str]:
    for permission in get_role_permissions(role_name):
        if permission.get("resource") == resource and permission.get("action") == action:
            return permission.get("allowed_fields", [])
    return []


def get_policy_summary() -> dict[str, Any]:
    return POLICY
