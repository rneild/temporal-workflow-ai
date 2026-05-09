from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy
import dataclasses

with workflow.unsafe.imports_passed_through():
    from activities import (
        SelectBeansInput, SelectBeansOutput, select_beans,
        GrindBeansInput, GrindBeansOutput, grind_beans,
        HeatWaterInput, HeatWaterOutput, heat_water,
        PrepBrewerInput, PrepBrewerOutput, prep_brewer,
        DoseCoffeeInput, DoseCoffeeOutput, dose_coffee,
        BloomPourInput, BloomPourOutput, bloom_pour,
        MainBrewInput, MainBrewOutput, main_brew,
        TasteEvalInput, TasteEvalOutput, taste_eval,
        ChooseMilkInput, ChooseMilkOutput, choose_milk,
    )

@dataclasses.dataclass
class BrewRequest:
    brew_method: str
    bean_origin: str
    roast_level: str
    dose_grams: float
    water_ml: float
    milk_preference: str = "none"

@dataclasses.dataclass
class BrewLog:
    brew_method: str
    bean_origin: str
    roast_level: str
    grind_size: str
    dose_grams: float
    water_ml: float
    ratio: str
    water_temp_c: float
    bloom_weight_g: float
    bloom_wait_s: int
    total_brew_s: int
    flavour_notes: str
    balance: str
    recommendation: str
    milk_type: str
    milk_amount_ml: float
    milk_temp_c: float
    milk_notes: str

RETRY = RetryPolicy(maximum_attempts=3, initial_interval=timedelta(seconds=2))

@workflow.defn
class PerfectCupOfCoffeeWorkflow:
    @workflow.run
    async def run(self, req: BrewRequest) -> BrewLog:
        beans = await workflow.execute_activity(
            select_beans,
            SelectBeansInput(origin=req.bean_origin, roast_level=req.roast_level),
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=RETRY,
        )
        grind = await workflow.execute_activity(
            grind_beans,
            GrindBeansInput(brew_method=req.brew_method, dose_grams=req.dose_grams, roast_level=req.roast_level),
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=RETRY,
        )
        water = await workflow.execute_activity(
            heat_water,
            HeatWaterInput(brew_method=req.brew_method, roast_level=req.roast_level),
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=RETRY,
        )
        prep = await workflow.execute_activity(
            prep_brewer,
            PrepBrewerInput(brew_method=req.brew_method),
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=RETRY,
        )
        dose = await workflow.execute_activity(
            dose_coffee,
            DoseCoffeeInput(dose_grams=req.dose_grams, water_ml=req.water_ml),
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=RETRY,
        )
        bloom = await workflow.execute_activity(
            bloom_pour,
            BloomPourInput(dose_grams=req.dose_grams, roast_level=req.roast_level),
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=RETRY,
        )
        brew = await workflow.execute_activity(
            main_brew,
            MainBrewInput(brew_method=req.brew_method, water_ml=req.water_ml, bloom_weight_g=bloom.bloom_weight_g),
            start_to_close_timeout=timedelta(seconds=60),
            retry_policy=RETRY,
        )
        taste = await workflow.execute_activity(
            taste_eval,
            TasteEvalInput(
                brew_method=req.brew_method,
                grind_size=grind.grind_size,
                water_temp_c=water.temp_c,
                dose_grams=req.dose_grams,
                water_ml=req.water_ml,
                total_brew_s=brew.total_brew_s,
            ),
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=RETRY,
        )
        milk = await workflow.execute_activity(
            choose_milk,
            ChooseMilkInput(brew_method=req.brew_method, milk_preference=req.milk_preference),
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=RETRY,
        )
        return BrewLog(
            brew_method=req.brew_method,
            bean_origin=req.bean_origin,
            roast_level=req.roast_level,
            grind_size=grind.grind_size,
            dose_grams=req.dose_grams,
            water_ml=req.water_ml,
            ratio=dose.ratio,
            water_temp_c=water.temp_c,
            bloom_weight_g=bloom.bloom_weight_g,
            bloom_wait_s=bloom.wait_s,
            total_brew_s=brew.total_brew_s,
            flavour_notes=taste.flavour_notes,
            balance=taste.balance,
            recommendation=taste.recommendation,
            milk_type=milk.milk_type,
            milk_amount_ml=milk.milk_amount_ml,
            milk_temp_c=milk.milk_temp_c,
            milk_notes=milk.notes,
        )
