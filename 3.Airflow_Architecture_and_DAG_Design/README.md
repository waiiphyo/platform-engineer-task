# 3.Airflow DAG Resilience & Debugging
## 3.1 DAG Resilience & Best Practices
I want to be transparent here—I haven’t worked directly with Airflow in production, as this responsibility is handled by our dedicated ETL team. However, I’m actively learning about Airflow and have explored concepts like DAG structure, task retries, and operator usage.

While I don’t have production experience to draw from for this part of the assignment, I haven’t completed the DAG exercise yet but I haven’t completed the first DAG exercise yet, so I don’t have production experience to draw from for that part. However, I’m actively learning and reviewing the concepts involved. In the meantime, I’d still like to respond to the second question based on what I’ve learned so far.

## 3.2 Debugging Scenario
I’d like to answer this question, as I’ve studied common issues in DAG execution and task scheduling. Here's my response:

**Problem:** A task in the DAG is "randomly skipped" even though the previous task has succeeded.
### Possible Causes as I learned
- The task might have a trigger_rule that prevents it from running unless specific upstream conditions are met. The default is all_success, but it might be set to something like none_failed_min_one_success unintentionally.
- The task could be incorrectly marked as depends_on_past=True, causing it to skip if the previous run’s task was not successful.
- The DAG could have a schedule_interval or start_date misalignment, causing a task to be scheduled outside of a valid execution window.
- External triggers or sensors may be skipping the task unintentionally.

### What to Inspect
- Task’s `trigger_rule`
- `depends_on_past` and `wait_for_downstream` flags
- The upstream task’s state history
- DAG execution logs and task instance logs
- If it's a dynamic DAG, inspect conditional branching or templating logic

### Fix
- Set the correct `trigger_rule` (e.g., all_success if you expect the task to run only after successful upstream tasks).
- Disable `depends_on_past` unless necessary.
- Review DAG definition dates, schedule intervals, and ensure correct dependency chains are declared.
