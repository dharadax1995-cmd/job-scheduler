"""
job_factory.py

Creates job objects without exposing their construction details
to the rest of the application.
"""

from models import EmailJob, DataProcessingJob, PriorityJob


class JobFactory:
    """Factory responsible for creating different job types."""

    @staticmethod
    def create_job(job_type: str, job_id: int, **kwargs):
        if job_type == "email":
            return EmailJob(
                job_id,
                kwargs["recipient"]
            )

        if job_type == "data":
            return DataProcessingJob(
                job_id,
                kwargs["dataset"]
            )

        if job_type == "priority":
            return PriorityJob(
                job_id,
                kwargs["dataset"],
                kwargs["priority"]
            )

        raise ValueError(f"Unknown job type: {job_type}")