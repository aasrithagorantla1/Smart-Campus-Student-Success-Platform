# Smart Campus Student Success Platform

A complete low-cost student success platform prototype built with Angular, FastAPI, and DynamoDB-oriented data modeling for a Lambda-based AWS deployment pattern.

## Features
- Student success score with transparent weighting and missing-data rules
- Academic and placement risk logic with evidence and suggested interventions
- Role-based backend authorization using trusted server-side assignments
- Deterministic synthetic population of 150 students
- CSV import templates and validation workflow
- Responsive Angular dashboard and detailed student views
- CloudFormation/infrastructure templates and cost review notes

## Local quick start

### Backend
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
export APP_ENV=local
export LOCAL_DEMO_AUTH_BYPASS=false
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## Defaults and restrictions
- Local demo auth is explicitly isolated and must not be enabled for AWS deployment.
- Deployment is intentionally blocked when the local bypass flag is enabled in non-local environments.
- The platform is structured for a CloudFront + Lambda Function URL prototype and avoids paid hosting services.

## Repository structure
- `backend/` – FastAPI API, policy enforcement, seeding, scoring, and tests
- `frontend/` – Angular UI shell and dashboard views
- `infra/` – CloudFormation and deployment notes
- `config/` – canonical role policy
- `docs/` – architecture, API, scoring, cost, and deployment docs
- `templates/` – CSV import templates
- `tests/` – higher-level validation scripts

## Documentation index
- `docs/architecture.md`
- `docs/api.md`
- `docs/data-dictionary.md`
- `docs/scoring-methodology.md`
- `docs/role-matrix.md`
- `docs/cost-assumptions.md`
- `docs/deployment-preflight.md`
- `docs/demo-script.md`
