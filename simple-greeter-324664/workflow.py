
import dataclasses
from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy
import asyncio

with workflow.unsafe.imports_passed_through():
    from activities import GreetInput, GreetOutput, build_greeting


@dataclasses.dataclass
class WorkflowInput:
    name: str


@workflow.defn
class SimpleGreeterWorkflow:
    def __init__(self) -> None:
        self._approved: bool | None = None

    @workflow.signal
    async def approve(self) -> None:
        self._approved = True

    @workflow.signal
    async def reject(self) -> None:
        self._approved = False

    @workflow.run
    async def run(self, inp: WorkflowInput) -> str:
        # Wait for human approval signal (up to 1 hour)
        await workflow.wait_condition(
            lambda: self._approved is not None,
            timeout=timedelta(hours=1),
        )

        if not self._approved:
            return f"Workflow rejected for name: {inp.name}"

        result: GreetOutput = await workflow.execute_activity(
            build_greeting,
            GreetInput(name=inp.name),
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=RetryPolicy(maximum_attempts=3),
        )
        return result.message
