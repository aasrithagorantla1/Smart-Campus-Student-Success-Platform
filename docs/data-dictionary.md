# Smart Campus data dictionary

## Core entities
### Student
- `student_id` – unique student identifier
- `department` – one of three demo departments
- `study_year` – year number
- `dataset_id` – `demo` or `real`
- `reporting_periods` – six monthly periods
- `mentor_id` – staff assignment
- `risk_flags` – nested academic and placement risk
- `score_history` – score snapshots by period

### Score
- `component_values` – academic, attendance, lms, placement, skills, engagement
- `weights` – configured percentages for each component
- `coverage` – proportion of applicable weight still covered
- `status` – `ready`, `provisional`, `insufficient_data`

### Intervention
- `intervention_id`
- `student_id`
- `suggested_action`
- `supporting_evidence`
- `owner`
- `due_date`
- `review_date`
- `status`
- `outcome`
- `updated_by`

### Import
- `import_id`
- `source`
- `batch_size`
- `accepted_count`
- `rejected_count`
- `status`
- `errors`
