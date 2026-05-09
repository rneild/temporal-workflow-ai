
import dataclasses
from temporalio import activity
from temporalio.exceptions import ApplicationError


@dataclasses.dataclass
class GreetInput:
    name: str


@dataclasses.dataclass
class GreetOutput:
    message: str


@activity.defn
async def build_greeting(inp: GreetInput) -> GreetOutput:
    if not inp.name or not inp.name.strip():
        raise ApplicationError("Name must not be empty", non_retryable=True)
    return GreetOutput(message=f"Hello, {inp.name.strip()}! Workflow complete.")
