# Perfect Cup of Coffee Workflow

## Purpose
A step-by-step guided workflow that walks a user through brewing a perfect cup of coffee — from bean selection through to the final taste check. Each stage is tracked as a discrete activity, producing a structured brew log.

## Steps
1. Select beans (origin, roast level, freshness check)
2. Grind beans (method, grind size, dose in grams)
3. Heat water (target temp, actual temp, elapsed time)
4. Prep brewer and filter (method, rinse, preheat)
5. Measure and dose coffee (weight, ratio)
6. Bloom pour (water weight, wait time)
7. Main brew pour (total water weight, pour duration)
8. Taste evaluation (flavour notes, balance check, adjustment recommendation)

## Output
A structured `BrewLog` dataclass capturing all parameters and the final evaluation, suitable for saving to a brew journal.

## Inputs
- `brew_method`: str — e.g. "pour_over", "french_press", "aeropress"
- `bean_origin`: str — e.g. "Ethiopia Yirgacheffe"
- `roast_level`: str — e.g. "light", "medium", "dark"
- `dose_grams`: float — grams of coffee
- `water_ml`: float — millilitres of water

## Change History
- 2026-05-09 v1 — Initial deployment
