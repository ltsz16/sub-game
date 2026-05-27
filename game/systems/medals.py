"""
systems/medals.py — Medal and promotion evaluation.
"""

from game.constants import MEDALS, RANKS


# ─── Medal criteria ────────────────────────────────────────────────────────────
# Each tuple: (medal_name, tonnage_threshold, bonus_condition_fn)
# bonus_condition_fn receives patrol_result → True/False

def _sank_carrier(r):
    return any(s.get("ship_id") == "carrier" for s in r.ships_sunk)

def _sank_battleship(r):
    return any(s.get("ship_id") == "battleship" for s in r.ships_sunk)

def _sank_heavy_cruiser(r):
    return any(s.get("ship_id") == "heavy_cruiser" for s in r.ships_sunk)

def _survived_heavy_damage(r):
    return r.depth_charges_taken >= 20 and r.sub_survived

MEDAL_CRITERIA = [
    # (tonnage threshold, extra condition fn or None, medal name)
    (0,     _sank_carrier,       "Medal of Honor"),
    (30000, _sank_battleship,    "Medal of Honor"),
    (0,     _sank_battleship,    "Navy Cross"),
    (50000, None,                "Navy Cross"),
    (0,     _sank_heavy_cruiser, "Silver Star"),
    (30000, None,                "Silver Star"),
    (20000, None,                "Bronze Star"),
    (10000, None,                "Bronze Star"),
    (0,     _survived_heavy_damage, "Navy Commendation Medal"),
    (5000,  None,                "Navy Commendation Medal"),
]

# ─── Promotion thresholds (career total score) ────────────────────────────────
PROMOTION_SCORE_THRESHOLDS = [
    0,      # Ensign — start
    15,     # Lieutenant JG
    40,     # Lieutenant
    100,    # Lieutenant Commander
    200,    # Commander
    400,    # Captain
    700,    # Rear Admiral
]


def evaluate_patrol(patrol_result, career_state) -> dict:
    """
    Evaluate a patrol result and award medals / promotions.
    Returns dict with:
        medals  : list of medal names awarded this patrol
        promoted: new rank name or None
        messages: list of display strings
    """
    awarded   = []
    messages  = []
    r         = patrol_result

    if not r.sub_survived:
        messages.append("Your submarine was lost. No awards this patrol.")
        return {"medals": [], "promoted": None, "messages": messages}

    # Check medal criteria
    seen_medals = set(career_state.medals)
    for tonnage_thresh, cond_fn, medal_name in MEDAL_CRITERIA:
        if medal_name in seen_medals and medal_name not in ("Bronze Star", "Navy Commendation Medal"):
            continue  # Can't earn most medals twice
        if r.total_tonnage < tonnage_thresh:
            continue
        if cond_fn is not None and not cond_fn(r):
            continue
        if medal_name not in awarded:
            awarded.append(medal_name)
            career_state.medals.append(medal_name)
            messages.append(f"AWARDED: {medal_name}")

    # Check promotion
    promoted_to = None
    new_score   = career_state.total_score
    old_rank    = career_state.rank_index

    for rank_idx, threshold in enumerate(PROMOTION_SCORE_THRESHOLDS):
        if new_score >= threshold:
            if rank_idx > career_state.rank_index:
                career_state.rank_index = rank_idx
                promoted_to = RANKS[rank_idx]

    if promoted_to:
        messages.append(f"PROMOTED TO: {promoted_to}")

    if not messages:
        if r.total_tonnage > 0:
            messages.append(f"Good patrol. {r.total_tonnage:,} tons sunk.")
        else:
            messages.append("No ships sunk this patrol.")

    return {"medals": awarded, "promoted": promoted_to, "messages": messages}


def rank_name(career_state) -> str:
    idx = min(career_state.rank_index, len(RANKS) - 1)
    return RANKS[idx]
