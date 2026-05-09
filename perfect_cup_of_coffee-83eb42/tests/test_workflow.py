import pytest
from unittest.mock import AsyncMock, patch
from workflow import PerfectCupOfCoffeeWorkflow, BrewRequest, BrewLog
from activities import (
    SelectBeansOutput, GrindBeansOutput, HeatWaterOutput,
    PrepBrewerOutput, DoseCoffeeOutput, BloomPourOutput,
    MainBrewOutput, TasteEvalOutput, ChooseMilkOutput,
)

@pytest.mark.asyncio
async def test_perfect_cup_with_oat_milk():
    req = BrewRequest(
        brew_method="pour_over",
        bean_origin="Ethiopia Yirgacheffe",
        roast_level="light",
        dose_grams=20.0,
        water_ml=320.0,
        milk_preference="oat",
    )

    mock_select  = AsyncMock(return_value=SelectBeansOutput(freshness_ok=True, notes="Fresh beans"))
    mock_grind   = AsyncMock(return_value=GrindBeansOutput(grind_size="medium-fine", notes="Grind ok"))
    mock_water   = AsyncMock(return_value=HeatWaterOutput(temp_c=96.0, notes="96C"))
    mock_prep    = AsyncMock(return_value=PrepBrewerOutput(notes="Filter rinsed"))
    mock_dose    = AsyncMock(return_value=DoseCoffeeOutput(ratio="1:16.0", notes="Ratio ok"))
    mock_bloom   = AsyncMock(return_value=BloomPourOutput(bloom_weight_g=40.0, wait_s=45, notes="Bloom"))
    mock_brew    = AsyncMock(return_value=MainBrewOutput(total_brew_s=210, notes="Brew done"))
    mock_taste   = AsyncMock(return_value=TasteEvalOutput(
        flavour_notes="pour_over at 96C, medium-fine, 1:16.0",
        balance="balanced",
        recommendation="No changes needed — enjoy!",
    ))
    mock_milk    = AsyncMock(return_value=ChooseMilkOutput(
        milk_type="oat",
        milk_amount_ml=40.0,
        milk_temp_c=60.0,
        notes="Steam to 60°C. Oat milk froths well and adds a subtle sweetness.",
    ))

    with patch("workflow.select_beans", mock_select), \
         patch("workflow.grind_beans",  mock_grind), \
         patch("workflow.heat_water",   mock_water), \
         patch("workflow.prep_brewer",  mock_prep), \
         patch("workflow.dose_coffee",  mock_dose), \
         patch("workflow.bloom_pour",   mock_bloom), \
         patch("workflow.main_brew",    mock_brew), \
         patch("workflow.taste_eval",   mock_taste), \
         patch("workflow.choose_milk",  mock_milk):

        wf = PerfectCupOfCoffeeWorkflow()
        result = await wf.run(req)

    assert isinstance(result, BrewLog)
    assert result.milk_type == "oat"
    assert result.balance == "balanced"

@pytest.mark.asyncio
async def test_perfect_cup_no_milk():
    req = BrewRequest(
        brew_method="pour_over",
        bean_origin="Kenya AA",
        roast_level="medium",
        dose_grams=20.0,
        water_ml=320.0,
        milk_preference="none",
    )

    mock_select  = AsyncMock(return_value=SelectBeansOutput(freshness_ok=True, notes="Fresh"))
    mock_grind   = AsyncMock(return_value=GrindBeansOutput(grind_size="medium-fine", notes="Grind ok"))
    mock_water   = AsyncMock(return_value=HeatWaterOutput(temp_c=93.0, notes="93C"))
    mock_prep    = AsyncMock(return_value=PrepBrewerOutput(notes="Filter rinsed"))
    mock_dose    = AsyncMock(return_value=DoseCoffeeOutput(ratio="1:16.0", notes="Ratio ok"))
    mock_bloom   = AsyncMock(return_value=BloomPourOutput(bloom_weight_g=40.0, wait_s=30, notes="Bloom"))
    mock_brew    = AsyncMock(return_value=MainBrewOutput(total_brew_s=210, notes="Brew done"))
    mock_taste   = AsyncMock(return_value=TasteEvalOutput(
        flavour_notes="pour_over at 93C, medium-fine, 1:16.0",
        balance="balanced",
        recommendation="No changes needed — enjoy!",
    ))
    mock_milk    = AsyncMock(return_value=ChooseMilkOutput(
        milk_type="none",
        milk_amount_ml=0.0,
        milk_temp_c=0.0,
        notes="No milk — serve black.",
    ))

    with patch("workflow.select_beans", mock_select), \
         patch("workflow.grind_beans",  mock_grind), \
         patch("workflow.heat_water",   mock_water), \
         patch("workflow.prep_brewer",  mock_prep), \
         patch("workflow.dose_coffee",  mock_dose), \
         patch("workflow.bloom_pour",   mock_bloom), \
         patch("workflow.main_brew",    mock_brew), \
         patch("workflow.taste_eval",   mock_taste), \
         patch("workflow.choose_milk",  mock_milk):

        wf = PerfectCupOfCoffeeWorkflow()
        result = await wf.run(req)

    assert result.milk_type == "none"
    assert result.milk_amount_ml == 0.0
