# Perfect Cup of Coffee Workflow

## Purpose
A step-by-step guided workflow that walks a user through brewing a perfect cup of coffee — from bean selection through to sugar and milk choice. Each stage is tracked as a discrete activity, producing a structured brew log.

## Steps
1. Select beans (origin, roast level, freshness check)
2. Grind beans (method, grind size, dose in grams)
3. Heat water (target temp, actual temp, elapsed time)
4. Prep brewer and filter (method, rinse, preheat)
5. Measure and dose coffee (weight, ratio)
6. Bloom pour (water weight, wait time)
7. Main brew pour (total water weight, pour duration)
8. Taste evaluation (flavour notes, balance check, adjustment recommendation)
9. Add sugar (type, amount, method-appropriate guidance)
10. Milk choice (type, amount, temperature recommendation)

## Output
A structured `BrewLog` dataclass capturing all parameters, the final evaluation, sugar details, and milk recommendation.

## Inputs
- `brew_method`: str — e.g. "pour_over", "french_press", "aeropress"
- `bean_origin`: str — e.g. "Ethiopia Yirgacheffe"
- `roast_level`: str — e.g. "light", "medium", "dark"
- `dose_grams`: float — grams of coffee
- `water_ml`: float — millilitres of water
- `milk_preference`: str — e.g. "whole", "oat", "skimmed", "almond", "soy", "none"
- `sugar_preference`: str — e.g. "white", "brown", "raw", "honey", "syrup", "none"

## Sugar Options
- `white` — 1 tsp, stir while hot
- `brown` — 1 tsp, subtle molasses depth
- `raw` — 1 tsp, light caramel note
- `honey` — 0.5 tsp, mild variety recommended
- `syrup` — 0.5 tsp, even sweetness, no graininess
- `none` — serve unsweetened

## Design Notes
- Sugar step sits after taste evaluation so the balance assessment reflects the brew itself before sweetening
- Cold brew + honey triggers an advisory to use simple syrup instead
- All activities use typed dataclasses; no raw dicts
- Retry policy: 3 attempts, 2s initial interval

## Change History
- 2026-05-09 v1 — Added add_sugar activity (step 9) with support for white, brown, raw, honey, syrup, none; BrewRequest and BrewLog updated accordingly
