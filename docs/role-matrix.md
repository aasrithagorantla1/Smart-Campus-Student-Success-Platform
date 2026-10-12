# Role matrix

This document is generated from the canonical policy in `config/role-matrix.json`.

## College Administrator
| Resource | Action | Allowed fields | Scope |
| --- | --- | --- | --- |
| student_master | manage | all | college |
| dashboard | view | all | college |
| mentor_assignment | assign | mentor_id, department_id, student_ids | college |
| intervention | review | all | college |
| scoring_config | manage | version, weights, thresholds, approved_by, audit_log | college |

## HOD
| Resource | Action | Allowed fields | Scope |
| --- | --- | --- | --- |
| department_dashboard | view | department_summary, risk_counts, student_metrics | department |
| mentor_assignment | assign | mentor_id, student_ids | department |
| corrections | approve | marks, attendance, notes | department |
| intervention | monitor | status, owner, due_date, outcome | department |

## Faculty or Mentor
| Resource | Action | Allowed fields | Scope |
| --- | --- | --- | --- |
| marks | enter | subject_code, student_id, mark, assessment_type, term | assigned_subject |
| attendance | enter | student_id, subject_code, percentage, period | assigned_subject |
| assessment_summary | enter | student_id, summary, assessment_notes, lms_activity | assigned_subject |
| student_insight | view | risk_summary, score, trend, recommendations | assigned_students |
| intervention | create_update | student_id, action, owner, notes, status, due_date | assigned_students |

## Placement Officer
| Resource | Action | Allowed fields | Scope |
| --- | --- | --- | --- |
| placement_assessment | enter | aptitude_score, coding_score, mock_interview_score, placement_readiness | assigned_students |
| skill_assessment | maintain | technical_skills, communication_skills, project_work, certifications | assigned_students |
| placement_training | assign | training_plan, due_date, owner | assigned_students |
| student_fields | view | student_id, department, year, placement_results, skill_summary, interview_notes | assigned_students |

## Activity Coordinator
| Resource | Action | Allowed fields | Scope |
| --- | --- | --- | --- |
| events | maintain | event_name, department, participation, attendance | department |
| engagement_verification | verify | club_activity, certifications, engagement | department |
| student_engagement | view | engagement_summary, event_history, certifications | department |

## Student
| Resource | Action | Allowed fields | Scope |
| --- | --- | --- | --- |
| own_profile | view | scores, recommendations, profile_summary | own_record |
| feedback | submit | message, category, sentiment | own_record |
| certifications | submit | name, issuer, date, evidence | own_record |

## System Administrator
| Resource | Action | Allowed fields | Scope |
| --- | --- | --- | --- |
| accounts | manage | user_id, email, role, department_id | college |
| technical_config | manage | settings, feature_flags, audit_trail | college |
