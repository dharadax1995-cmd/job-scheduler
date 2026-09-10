"""
models.py

Defines the Job hierarchy (parent + child classes).

Polymorphism: each subclass implements its own execute().
Encapsulation: job logs are private and accessed through methods.
"""


class Job:
    """Parent/base class shared by all job types."""

    def __init__(self, job_id: int, description: str) -> None:
        self.job_id = job_id
        self.description = description
        self.status = "pending"

        # Private attribute for encapsulation
        self.__logs = []

    def add_log(self, message: str) -> None:
        """Add a message to the private job logs."""
        self.__logs.append(message)

    def get_logs(self) -> list[str]:
        """Return a copy of the job logs."""
        return self.__logs.copy()

    def execute(self) -> None:
        """Must be overridden by subclasses."""
        raise NotImplementedError(
            "Each job must implement its own execution logic."
        )

    def mark_done(self) -> None:
        self.status = "completed"

    def __repr__(self) -> str:
        return (
            f"<Job id={self.job_id} status={self.status} "
            f"description='{self.description}'>"
        )


class EmailJob(Job):
    """Child class: sends an email."""

    def __init__(self, job_id: int, recipient: str) -> None:
        super().__init__(job_id, f"Send email to {recipient}")
        self.recipient = recipient

    def execute(self) -> None:
        print(f"Sending email to {self.recipient}...")

        # Status is managed by TaskManager.update_status().


class DataProcessingJob(Job):
    """Child class: processes a dataset."""

    def __init__(self, job_id: int, dataset: str) -> None:
        super().__init__(job_id, f"Process dataset {dataset}")
        self.dataset = dataset

    def execute(self) -> None:
        print(f"Processing dataset {self.dataset}...")

        # Status is managed by TaskManager.update_status().


class PriorityJob(DataProcessingJob):
    """A data-processing job with an assigned priority."""

    def __init__(self, job_id: int, dataset: str, priority: int) -> None:
        super().__init__(job_id, dataset)
        self.priority = priority

    def __str__(self) -> str:
        return (
            f"PriorityJob(id={self.job_id}, dataset={self.dataset}, "
            f"priority={self.priority})"
        )