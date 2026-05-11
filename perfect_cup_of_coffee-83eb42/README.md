# Perfect Cup of Coffee

Guides a barista (or automated system) through every step needed to brew a technically correct cup of coffee, from bean selection through to milk preparation, and returns a structured brew log with a taste-balance assessment and dialling-in recommendation.

## What it does

Accepts a `BrewRequest` specifying brew method, bean origin, roast level, dose, water volume, and milk preference. Executes nine sequential activities — each responsible for one discrete stage of the brewing process — and assembles the results into a `BrewLog` dataclass returned to the caller.

## Activity pipeline

| Step | Activity | Responsibility |
|------|----------|----------------|
| 1 | `select_beans` | Validates roast level; confirms freshness guidance |
| 2 | `grind_beans` | Looks up correct grind size per brew method |
| 3 | `heat_water` | Sets target water temperature by roast level (light 96°C / medium 93°C / dark 90°C) |
| 4 | `prep_brewer` | Returns method-specific equipment setup instructions |
| 5 | `dose_coffee` | Computes coffee-to-water ratio; flags if outside 1:14–1:18 |
| 6 | `bloom_pour` | Calculates bloom water weight (2× dose) and wait time (45s light / 30s others) |
| 7 | `main_brew` | Computes remaining pour volume and target brew time per method |
| 8 | `taste_eval` | Evaluates extraction balance; returns flavour notes and a dialling-in recommendation |
| 9 | `choose_milk` | Returns milk type, steaming temperature, amount, and handling notes |

## Supported brew methods

`pour_over`, `french_press`, `aeropress`, `chemex`, `moka_pot`, `espresso`, `cold_brew`

## Supported milk options

`whole`, `oat`, `skimmed`, `almond`, `soy`, `none`

## Error handling

All activities raise `ApplicationError(non_retryable=True)` for invalid inputs. Transient failures retry up to 3 times with a 2-second initial interval.

## Secrets

None required.

## Change History
- 2026-05-09 v1 — Added add_sugar activity (step 9) with support for white, brown, raw, honey, syrup, none; BrewRequest and BrewLog updated accordingly
- 2026-05-09 v2 — Regenerated README — full step table, BrewRequest/BrewLog field tables, per-activity reference, design decisions, all 10 activities documented
- 2026-05-11 v3 — Added requirements.txt and intent_md
