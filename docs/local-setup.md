# Smart Campus Student Success Platform

This repository contains a working local prototype skeleton for the student success platform, including:
- FastAPI backend with seed and role policy enforcement
- Angular frontend shell for the dashboard and overview experience
- deterministic synthetic seed data and score logic
- CloudFormation and cost review documentation

## Local setup

### Python backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export APP_ENV=local
export LOCAL_DEMO_AUTH_BYPASS=false
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Angular frontend
```bash
cd frontend
npm install
npm start
```

## Notes
- The implementation intentionally avoids paid AI or backend hosting services.
- The local front end is a browser-based shell that reads from the backend API.
- AWS deployment remains blocked pending explicit review and free-tier validation.
