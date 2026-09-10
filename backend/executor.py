"""
executor.py

Runs jobs concurrently using threads to simulate a scheduler.

- Random delay: simulates work
- Random failure: exercises exception handling
- Job logs: records execution events for auditing and debugging
"""


import threading
import time
import random

from datetime import datetime
from typing import List

from errors import JobExecutionError
from models import Job


class Executor:
    def __init__(self, jobs: List[Job], manager) -> None:
        self.jobs = jobs
        self.manager = manager

    def _ts(self) -> str:
        return datetime.now().strftime("%H:%M:%S")

    def run_job(self, job: Job) -> None:
        try:
            start_message = (
                f"[{self._ts()}] Executing job "
                f"{job.job_id} ({job.description})..."
            )

            print(start_message)
            job.add_log(start_message)

            time.sleep(random.uniform(1, 3))

            if random.random() < 0.2:
                raise JobExecutionError(job.job_id)

            job.execute()
            self.manager.update_status(job, "completed")

            completed_message = (
                f"[{self._ts()}] Completed job {job.job_id}."
            )

            print(completed_message)
            job.add_log(completed_message)

        except JobExecutionError as error:
            self.manager.update_status(job, "failed")

            error_message = (
                f"[{self._ts()}] Error in job "
                f"{error.job_id}: {error}"
            )

            print(error_message)
            job.add_log(error_message)

    def run(self) -> None:
        threads: List[threading.Thread] = []

        for job in self.jobs:
            thread = threading.Thread(
                target=self.run_job,
                args=(job,)
            )

            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()