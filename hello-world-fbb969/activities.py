from dataclasses import dataclass
from temporalio import activity
@dataclass
class HelloInput:
    name: str
@activity.defn
async def greet(inp: HelloInput) -> str:
    return f"Hello, {inp.name}!"