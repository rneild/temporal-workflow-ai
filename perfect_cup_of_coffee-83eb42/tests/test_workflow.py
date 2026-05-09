import pytest
from unittest.mock import AsyncMock, patch
from workflow import PerfectCupOfCoffeeWorkflow, BrewRequest, BrewLog
from activities import (
    SelectBeansOutput, GrindBeansOutput, HeatWaterOutput,
    PrepBrewerOutput, DoseCoffeeOutput, BloomPourOutput,
    MainBrewOutput, TasteEvalOutput,
)

@pytest.mark.asyncio
async def test_perfect_cup_workflow():
    req = BrewRequest(
        brew_method="pour_over",
        bean_origin="Ethiopia Yirgacheffe",
        roast_level="light",
        dose_grams=20.0,
        water_ml=320.0,
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

    with patch("workflow.select_beans", mock_select), \
         patch("workflow.grind_beans",  mock_grind), \
         patch("workflow.heat_water",   mock_water), \
         patch("workflow.prep_brewer",  mock_prep), \
         patch("workflow.dose_coffee",  mock_dose), \
         patch("workflow.bloom_pour",   mock_bloom), \
         patch("workflow.main_brew",    mock_brew), \
         patch("workflow.taste_eval",   mock_taste):

        wf = PerfectCupOfCoffeeWorkflow()
        result = await wf.run(req)

    assert isinstance(result, BrewLog)
    assert result.brew_method == "pour_over"
    assert result.grind_size == "medium-fine"
    assert result.water_temp_c == 96.0
    assert result.bloom_weight_g == 40.0
    assert result.bloom_wait_s == 45
    assert result.total_brew_s == 210
    assert result.balance == "balanced"
    assert result.ratio == "1:16.0"
    assert result.recommendation == "No changes needed — enjoy!"
