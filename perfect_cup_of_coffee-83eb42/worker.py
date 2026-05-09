import asyncio
import temporalio.worker
from temporalio.client import Client
from workflow import PerfectCupOfCoffeeWorkflow
from activities import (
    select_beans, grind_beans, heat_water, prep_brewer,
    dose_coffee, bloom_pour, main_brew, taste_eval, choose_milk,
)

async def main():
    client = await Client.connect("localhost:7233")
    worker = temporalio.worker.Worker(
        client,
        task_queue="perfect-cup-of-coffee",
        workflows=[PerfectCupOfCoffeeWorkflow],
        activities=[
            select_beans, grind_beans, heat_water, prep_brewer,
            dose_coffee, bloom_pour, main_brew, taste_eval, choose_milk,
        ],
    )
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
