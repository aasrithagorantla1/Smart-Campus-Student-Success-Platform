# Smart Campus Student Success Platform

This repository contains a complete platform prototype for a student success workflow using:
- Angular + TypeScript frontend
- FastAPI backend
- DynamoDB-aware data layer abstractions
- Lambda-oriented deployment templates for AWS
- Role-based authorization and synthetic seed data generation

## Design assumptions
- The prototype intentionally uses a low-cost CloudFront + Lambda Function URL model.
- Details are for local development and deployment review; no AWS deployment occurs automatically.
- Demo and operational data are distinct, and demo records are excluded from real aggregates by default.
