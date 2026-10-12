from __future__ import annotations

from typing import Any

from backend.app.config import ROLE_MATRIX_PATH
from backend.app.role_policy import get_policy_summary as _get_policy_summary

# Re-export policy summary for callers that expect it in this module.
def get_policy_summary() -> dict[str, Any]:
    return _get_policy_summary()

__all__ = [
    "generate_demo_token",
    "verify_token",
    "build_demo_user_map",
    "get_user_claims_from_request",
    "create_auth_dependency",
    "get_policy_summary",
]
