# Perfect Cup of Coffee Workflow

## Purpose
A step-by-step guided workflow that walks a user through brewing a perfect cup of coffee — from bean selection through to milk choice. Each stage is tracked as a discrete activity, producing a structured brew log.

## Steps
1. Select beans (origin, roast level, freshness check)
2. Grind beans (method, grind size, dose in grams)
3. Heat water (target temp, actual temp, elapsed time)
4. Prep brewer and filter (method, rinse, preheat)
5. Measure and dose coffee (weight, ratio)
6. Bloom pour (water weight, wait time)
7. Main brew pour (total water weight, pour duration)
8. Taste evaluation (flavour notes, balance check, adjustment recommendation)
9. Milk choice (type, amount, temperature recommendation)

## Output
A structured `BrewLog` dataclass capturing all parameters, the final evaluation, and milk recommendation.

## Inputs
- `brew_method`: str — e.g. "pour_over", "french_press", "aeropress"
- `bean_origin`: str — e.g. "Ethiopia Yirgacheffe"
- `roast_level`: str — e.g. "light", "medium", "dark"
- `dose_grams`: float — grams of coffee
- `water_ml`: float — millilitres of water
- `milk_preference`: str — e.g. "whole", "oat", "skimmed", "almond", "soy", "none"

## Change History
- 2026-05-09 v1 — Initial deployment
- 2026-05-09 v2 — Added choose_milk activity (step 9) — supports whole, oat, skimmed, almond, soy, none with method-appropriate amounts and steam temps
