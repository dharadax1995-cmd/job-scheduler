"""

app.py

Build a few jobs, register them, run them, print a summary.

"""


from job_factory import JobFactory

from task_manager import TaskManager

from executor import Executor


def build_jobs():
    return [
        JobFactory.create_job(
            "email",
            1,
            recipient="user@example.com"
        ),
        JobFactory.create_job(
            "data",
            2,
            dataset="dataset_A"
        ),
        JobFactory.create_job(
            "email",
            3,
            recipient="admin@example.com"
        ),
        JobFactory.create_job(
            "data",
            4,
            dataset="dataset_B"
        ),
        JobFactory.create_job(
            "priority",
            5,
            dataset="critical_dataset",
            priority=1
        ),
        JobFactory.create_job(
            "priority",
            6,
            dataset="standard_dataset",
            priority=3
        ),
        JobFactory.create_job(
            "priority",
            7,
            dataset="important_dataset",
            priority=2
        ),
    ]


if __name__ == "__main__":

    jobs = build_jobs()
    jobs.sort(key=lambda job: getattr(job, "priority", 999))


    manager = TaskManager()

    for job in jobs:

        manager.add_job(job)  # all start as 'pending'


    # FIX (app.py): pass 'manager' to Executor so it can update statuses.
    # Previously Executor(jobs).run() had no manager reference — statuses never changed.
    Executor(jobs, manager).run()


    print("\n=== SUMMARY ===")

    print(f"Pending:   {len(manager.get_jobs_by_status('pending'))}")

    print(f"Completed: {len(manager.get_jobs_by_status('completed'))}")

    # FIX (app.py): added 'failed' count to summary so failures are visible.
    print(f"Failed:    {len(manager.get_jobs_by_status('failed'))}")

    print("\n=== JOB LOGS ===")

for job in jobs:
    print(f"\nJob {job.job_id} logs:")

    for log in job.get_logs():
        print(f"- {log}")