
import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from activities import build_greeting
from workflow import SimpleGreeterWorkflow


async def main() -> None:
    client = await Client.connect("localhost:7233")
    async with Worker(
        client,
        task_queue="simple-greeter-queue",
        workflows=[SimpleGreeterWorkflow],
        activities=[build_greeting],
    ):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
