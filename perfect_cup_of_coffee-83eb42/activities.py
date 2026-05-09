import dataclasses
from temporalio import activity
from temporalio.exceptions import ApplicationError

# ── Select beans ──────────────────────────────────────────────────────────────

@dataclasses.dataclass
class SelectBeansInput:
    origin: str
    roast_level: str

@dataclasses.dataclass
class SelectBeansOutput:
    freshness_ok: bool
    notes: str

@activity.defn
async def select_beans(inp: SelectBeansInput) -> SelectBeansOutput:
    roast_level = inp.roast_level.lower()
    if roast_level not in ("light", "medium", "dark"):
        raise ApplicationError(
            f"Unknown roast level: {inp.roast_level}. Use light, medium, or dark.",
            non_retryable=True,
        )
    notes = (
        f"{inp.origin} — {roast_level} roast. "
        "Ensure beans were roasted within the last 2–4 weeks and "
        "are stored in an airtight container away from light."
    )
    return SelectBeansOutput(freshness_ok=True, notes=notes)

# ── Grind beans ───────────────────────────────────────────────────────────────

GRIND_SIZES = {
    "pour_over": "medium-fine",
    "french_press": "coarse",
    "aeropress": "medium-fine",
    "espresso": "fine",
    "chemex": "medium-coarse",
    "moka_pot": "fine",
    "cold_brew": "extra-coarse",
}

@dataclasses.dataclass
class GrindBeansInput:
    brew_method: str
    dose_grams: float
    roast_level: str

@dataclasses.dataclass
class GrindBeansOutput:
    grind_size: str
    notes: str

@activity.defn
async def grind_beans(inp: GrindBeansInput) -> GrindBeansOutput:
    method = inp.brew_method.lower()
    grind_size = GRIND_SIZES.get(method)
    if not grind_size:
        raise ApplicationError(
            f"Unsupported brew method: {inp.brew_method}",
            non_retryable=True,
        )
    if inp.dose_grams <= 0:
        raise ApplicationError("dose_grams must be greater than 0", non_retryable=True)
    notes = (
        f"Grind {inp.dose_grams:.1f}g to {grind_size} for {inp.brew_method}. "
        "Grind immediately before brewing for best results."
    )
    return GrindBeansOutput(grind_size=grind_size, notes=notes)

# ── Heat water ────────────────────────────────────────────────────────────────

WATER_TEMPS = {
    "light": 96,
    "medium": 93,
    "dark": 90,
}

@dataclasses.dataclass
class HeatWaterInput:
    brew_method: str
    roast_level: str

@dataclasses.dataclass
class HeatWaterOutput:
    temp_c: float
    notes: str

@activity.defn
async def heat_water(inp: HeatWaterInput) -> HeatWaterOutput:
    roast = inp.roast_level.lower()
    temp = WATER_TEMPS.get(roast)
    if temp is None:
        raise ApplicationError(
            f"Unknown roast level for temp lookup: {inp.roast_level}",
            non_retryable=True,
        )
    notes = (
        f"Target water temperature: {temp}°C. "
        "Bring to boil then let rest ~30 seconds, or use a temperature-controlled kettle."
    )
    return HeatWaterOutput(temp_c=float(temp), notes=notes)

# ── Prep brewer ───────────────────────────────────────────────────────────────

PREP_NOTES = {
    "pour_over": "Place filter in dripper, rinse thoroughly with hot water, discard rinse water. Preheat server.",
    "french_press": "Preheat the French press with hot water, discard. No filter rinse needed.",
    "aeropress": "Wet the paper filter and cap, insert into aeropress. Preheat with a small pour.",
    "chemex": "Fold Chemex filter (thicker side toward spout), rinse, discard water.",
    "moka_pot": "Fill base chamber with pre-heated water to just below the valve.",
    "espresso": "Purge portafilter with hot water. Preheat cup.",
    "cold_brew": "No heat required. Ensure container is clean and chilled.",
}

@dataclasses.dataclass
class PrepBrewerInput:
    brew_method: str

@dataclasses.dataclass
class PrepBrewerOutput:
    notes: str

@activity.defn
async def prep_brewer(inp: PrepBrewerInput) -> PrepBrewerOutput:
    method = inp.brew_method.lower()
    notes = PREP_NOTES.get(method)
    if not notes:
        raise ApplicationError(
            f"No prep instructions for brew method: {inp.brew_method}",
            non_retryable=True,
        )
    return PrepBrewerOutput(notes=notes)

# ── Dose coffee ───────────────────────────────────────────────────────────────

@dataclasses.dataclass
class DoseCoffeeInput:
    dose_grams: float
    water_ml: float

@dataclasses.dataclass
class DoseCoffeeOutput:
    ratio: str
    notes: str

@activity.defn
async def dose_coffee(inp: DoseCoffeeInput) -> DoseCoffeeOutput:
    if inp.dose_grams <= 0 or inp.water_ml <= 0:
        raise ApplicationError("dose_grams and water_ml must both be > 0", non_retryable=True)
    ratio_num = inp.water_ml / inp.dose_grams
    ratio = f"1:{ratio_num:.1f}"
    quality = "good" if 14 <= ratio_num <= 18 else "outside recommended range (14–18)"
    notes = f"Using {inp.dose_grams:.1f}g coffee to {inp.water_ml:.0f}ml water — ratio {ratio} ({quality})."
    return DoseCoffeeOutput(ratio=ratio, notes=notes)

# ── Bloom pour ────────────────────────────────────────────────────────────────

@dataclasses.dataclass
class BloomPourInput:
    dose_grams: float
    roast_level: str

@dataclasses.dataclass
class BloomPourOutput:
    bloom_weight_g: float
    wait_s: int
    notes: str

@activity.defn
async def bloom_pour(inp: BloomPourInput) -> BloomPourOutput:
    bloom_weight = round(inp.dose_grams * 2, 1)
    wait_s = 45 if inp.roast_level.lower() == "light" else 30
    notes = (
        f"Pour {bloom_weight}g water evenly over all grounds. "
        f"Wait {wait_s} seconds until bubbling subsides — this is the bloom (CO₂ off-gassing)."
    )
    return BloomPourOutput(bloom_weight_g=bloom_weight, wait_s=wait_s, notes=notes)

# ── Main brew ─────────────────────────────────────────────────────────────────

BREW_TIMES = {
    "pour_over": 210,
    "french_press": 240,
    "aeropress": 120,
    "chemex": 270,
    "moka_pot": 300,
    "espresso": 30,
    "cold_brew": 86400,
}

@dataclasses.dataclass
class MainBrewInput:
    brew_method: str
    water_ml: float
    bloom_weight_g: float

@dataclasses.dataclass
class MainBrewOutput:
    total_brew_s: int
    notes: str

@activity.defn
async def main_brew(inp: MainBrewInput) -> MainBrewOutput:
    method = inp.brew_method.lower()
    total_brew_s = BREW_TIMES.get(method)
    if total_brew_s is None:
        raise ApplicationError(
            f"No brew time data for method: {inp.brew_method}",
            non_retryable=True,
        )
    remaining_ml = inp.water_ml - inp.bloom_weight_g
    if remaining_ml <= 0:
        raise ApplicationError(
            "water_ml must be greater than bloom water weight",
            non_retryable=True,
        )
    notes = (
        f"Pour remaining {remaining_ml:.0f}ml in slow, even spirals starting from centre. "
        f"Target total brew time: ~{total_brew_s}s."
    )
    return MainBrewOutput(total_brew_s=total_brew_s, notes=notes)

# ── Taste evaluation ──────────────────────────────────────────────────────────

@dataclasses.dataclass
class TasteEvalInput:
    brew_method: str
    grind_size: str
    water_temp_c: float
    dose_grams: float
    water_ml: float
    total_brew_s: int

@dataclasses.dataclass
class TasteEvalOutput:
    flavour_notes: str
    balance: str
    recommendation: str

@activity.defn
async def taste_eval(inp: TasteEvalInput) -> TasteEvalOutput:
    ratio = inp.water_ml / inp.dose_grams
    if ratio < 14:
        balance = "strong"
        recommendation = "Increase water or reduce dose for a less intense cup."
    elif ratio > 18:
        balance = "weak"
        recommendation = "Reduce water or increase dose for more body."
    elif inp.water_temp_c < 88:
        balance = "under-extracted (sour risk)"
        recommendation = "Raise water temperature closer to 90–96°C."
    elif inp.total_brew_s < 60 and inp.brew_method not in ("espresso",):
        balance = "under-extracted (too fast)"
        recommendation = "Grind finer to slow extraction."
    else:
        balance = "balanced"
        recommendation = "No changes needed — enjoy!"
    flavour_notes = (
        f"Brewed via {inp.brew_method} at {inp.water_temp_c:.0f}°C, "
        f"{inp.grind_size} grind, 1:{ratio:.1f} ratio."
    )
    return TasteEvalOutput(
        flavour_notes=flavour_notes,
        balance=balance,
        recommendation=recommendation,
    )
