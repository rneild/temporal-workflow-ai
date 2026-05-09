# Perfect Cup of Coffee Workflow

## Purpose

A step-by-step guided workflow that walks a user through brewing a perfect cup of coffee — from bean selection through to sugar and milk choice. Each stage is a discrete Temporal activity, producing a fully structured `BrewLog` at the end.

## Workflow diagram

```
flowchart TD
    A[select_beans] --> B[grind_beans]
    B --> C[heat_water]
    C --> D[prep_brewer]
    D --> E[dose_coffee]
    E --> F[bloom_pour]
    F --> G[main_brew]
    G --> H[taste_eval]
    H --> I[add_sugar]
    I --> J[choose_milk]
    J --> K[BrewLog output]
```

## Steps

| # | Activity | Key inputs | Key outputs |
|---|----------|-----------|-------------|
| 1 | `select_beans` | `origin`, `roast_level` | `freshness_ok`, `notes` |
| 2 | `grind_beans` | `brew_method`, `dose_grams`, `roast_level` | `grind_size`, `notes` |
| 3 | `heat_water` | `brew_method`, `roast_level` | `temp_c`, `notes` |
| 4 | `prep_brewer` | `brew_method` | `notes` |
| 5 | `dose_coffee` | `dose_grams`, `water_ml` | `ratio`, `notes` |
| 6 | `bloom_pour` | `dose_grams`, `roast_level` | `bloom_weight_g`, `wait_s`, `notes` |
| 7 | `main_brew` | `brew_method`, `water_ml`, `bloom_weight_g` | `total_brew_s`, `notes` |
| 8 | `taste_eval` | `brew_method`, `grind_size`, `water_temp_c`, `dose_grams`, `water_ml`, `total_brew_s` | `flavour_notes`, `balance`, `recommendation` |
| 9 | `add_sugar` | `brew_method`, `sugar_preference` | `sugar_type`, `amount_tsp`, `notes` |
| 10 | `choose_milk` | `brew_method`, `milk_preference` | `milk_type`, `milk_amount_ml`, `milk_temp_c`, `notes` |

## Inputs (`BrewRequest`)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `brew_method` | str | required | One of: `pour_over`, `french_press`, `aeropress`, `chemex`, `moka_pot`, `espresso`, `cold_brew` |
| `bean_origin` | str | required | Free-text origin, e.g. `"Ethiopia Yirgacheffe"` |
| `roast_level` | str | required | One of: `light`, `medium`, `dark` |
| `dose_grams` | float | required | Coffee dose in grams (must be > 0) |
| `water_ml` | float | required | Water volume in ml (must be > 0) |
| `milk_preference` | str | `"none"` | One of: `whole`, `oat`, `skimmed`, `almond`, `soy`, `none` |
| `sugar_preference` | str | `"none"` | One of: `white`, `brown`, `raw`, `honey`, `syrup`, `none` |

## Output (`BrewLog`)

| Field | Type | Source activity |
|-------|------|----------------|
| `brew_method` | str | input |
| `bean_origin` | str | input |
| `roast_level` | str | input |
| `grind_size` | str | `grind_beans` |
| `dose_grams` | float | input |
| `water_ml` | float | input |
| `ratio` | str | `dose_coffee` |
| `water_temp_c` | float | `heat_water` |
| `bloom_weight_g` | float | `bloom_pour` |
| `bloom_wait_s` | int | `bloom_pour` |
| `total_brew_s` | int | `main_brew` |
| `flavour_notes` | str | `taste_eval` |
| `balance` | str | `taste_eval` |
| `recommendation` | str | `taste_eval` |
| `sugar_type` | str | `add_sugar` |
| `sugar_amount_tsp` | float | `add_sugar` |
| `sugar_notes` | str | `add_sugar` |
| `milk_type` | str | `choose_milk` |
| `milk_amount_ml` | float | `choose_milk` |
| `milk_temp_c` | float | `choose_milk` |
| `milk_notes` | str | `choose_milk` |

## Activity reference

### `select_beans`
Validates roast level (`light`, `medium`, `dark`) and returns freshness guidance for the origin. Non-retryable on unknown roast level.

### `grind_beans`
Looks up the correct grind size for the brew method from a static map. Raises non-retryable error on unknown method or zero dose. Grind sizes: pour_over → medium-fine, french_press → coarse, aeropress → medium-fine, espresso → fine, chemex → medium-coarse, moka_pot → fine, cold_brew → extra-coarse.

### `heat_water`
Maps roast level to target temperature: light → 96°C, medium → 93°C, dark → 90°C. Non-retryable on unknown roast level.

### `prep_brewer`
Returns method-specific prep instructions (filter rinse, preheat, chamber fill, etc.) from a static map. Non-retryable on unknown method.

### `dose_coffee`
Calculates brew ratio (`water_ml / dose_grams`). Flags ratio as "good" if between 1:14–1:18, otherwise "outside recommended range". Both inputs must be > 0.

### `bloom_pour`
Calculates bloom water weight as `dose_grams × 2`. Wait time is 45s for light roast, 30s for medium/dark. Output `bloom_weight_g` is consumed by `main_brew`.

### `main_brew`
Subtracts bloom weight from total water to get remaining pour volume. Looks up target brew time by method. Raises non-retryable error if remaining water ≤ 0 or method is unknown.

### `taste_eval`
Evaluates the brew against five balance criteria in order: strong (ratio < 1:14), weak (ratio > 1:18), under-extracted sour risk (temp < 88°C), under-extracted too fast (brew < 60s, non-espresso), balanced (all clear). Returns `flavour_notes`, `balance`, and `recommendation`.

### `add_sugar`
Maps sugar preference to amount and instructions. Granulated types (white, brown, raw) → 1 tsp; liquid types (honey, syrup) → 0.5 tsp; none → 0 tsp. Cold brew + honey triggers an advisory to use simple syrup instead. Non-retryable on unknown preference.

### `choose_milk`
Maps milk preference to amount (method-dependent: 60ml for espresso/moka_pot, 80ml for cold_brew, 40ml otherwise) and temperature (whole/skimmed → 65°C, oat/soy → 60°C, almond → 55°C). Cold brew with any steamed milk appends a cold-add advisory. Non-retryable on unknown preference.

## Design decisions

- **Sugar after taste eval**: the balance assessment reflects the brew itself before sweetening — consistent with how a trained barista would evaluate a cup.
- **Bloom weight coupling**: `bloom_pour` output feeds directly into `main_brew` to ensure pour volumes are internally consistent.
- **Ratio check in both `dose_coffee` and `taste_eval`**: `dose_coffee` is advisory (notes only); `taste_eval` drives the `balance` field and recommendation. This separation keeps the dosing step lightweight.
- **All validation is non-retryable**: bad input (unknown method, zero dose, etc.) fails immediately without burning retry budget.
- **`sugar_preference` and `milk_preference` default to `"none"`**: existing callers with no sugar/milk fields are unaffected.

## Supported brew methods

`pour_over` · `french_press` · `aeropress` · `chemex` · `moka_pot` · `espresso` · `cold_brew`

## Files

| File | Purpose |
|------|---------|
| `workflow.py` | `PerfectCupOfCoffeeWorkflow` — orchestration, `BrewRequest` and `BrewLog` dataclasses |
| `activities.py` | All 10 activity functions with typed dataclass I/O |
| `worker.py` | Temporal worker entrypoint |
| `test_workflow_py` | Unit tests with mocked activities |
| `requirements.txt` | `temporalio==1.7.1`, `dataclasses-json==0.6.7` |

## Change History
- 2026-05-09 v1 — Added add_sugar activity (step 9) with support for white, brown, raw, honey, syrup, none; BrewRequest and BrewLog updated accordingly
- 2026-05-09 v2 — Regenerated README — full step table, BrewRequest/BrewLog field tables, per-activity reference, design decisions, all 10 activities documented
