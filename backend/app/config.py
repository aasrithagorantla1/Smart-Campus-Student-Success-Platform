from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parents[1]
APP_ENV = os.getenv("APP_ENV", "local")
LOCAL_DEMO_AUTH_BYPASS = os.getenv("LOCAL_DEMO_AUTH_BYPASS", "false").lower() == "true"

if APP_ENV != "local" and LOCAL_DEMO_AUTH_BYPASS:
    raise RuntimeError("Local authentication bypass is disabled outside local mode.")

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
COGNITO_USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID", "local-demo-user-pool")
COGNITO_APP_CLIENT_ID = os.getenv("COGNITO_APP_CLIENT_ID", "local-demo-client-id")
COGNITO_ISSUER = os.getenv("COGNITO_ISSUER", "https://localhost:8443")
JWT_SECRET = os.getenv("JWT_SECRET", "smart-campus-demo-secret")
ROLE_MATRIX_PATH = BASE_DIR / "config" / "role-matrix.json"

APP_TITLE = "Smart Campus Student Success Platform"
