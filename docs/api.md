# API contract summary

## Auth
- `POST /api/auth/local-demo-token` – local development only when explicit local mode is enabled
- `GET /api/auth/claims` – authenticated caller claims
- `GET /api/auth/role-matrix` – canonical role policy

## Dashboard
- `GET /api/dashboard/overview`
- `GET /api/dashboard/department-summary`
- `GET /api/dashboard/segmentation`

## Students
- `GET /api/students`
- `GET /api/students/{student_id}`
- `POST /api/students/search`

## Scoring and risk
- `GET /api/students/{student_id}/score`
- `GET /api/students/{student_id}/risk`
- `POST /api/students/{student_id}/recompute`

## Imports
- `GET /api/imports/templates`
- `POST /api/imports/preview`
- `POST /api/imports/submit`
- `GET /api/imports/{import_id}`

## Interventions
- `GET /api/interventions`
- `POST /api/interventions`
- `PATCH /api/interventions/{id}`

## Setup
- `POST /api/setup/seed`
- `POST /api/setup/reset-demo`
