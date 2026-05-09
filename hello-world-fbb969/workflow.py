from dataclasses import dataclass
import datetime
from temporalio import workflow
from temporalio.common import RetryPolicy
from activities import greet
@dataclass
class HelloInput:
    name: str
@workflow.defn
class HelloWorkflow:
    @workflow.run
    async def run(self, inp: HelloInput) -> str:
        return await workflow.execute_activity(greet, inp, start_to_close_timeout=datetime.timedelta(seconds=10), retry_policy=RetryPolicy(maximum_attempts=3))