"""
data/ships.py — Japanese ship types encountered in the Pacific.

Fields:
    id              : unique string key
    name            : display name
    category        : "merchant" | "warship" | "escort"
    tonnage         : gross tons (determines score)
    hp              : hit points (torpedoes do ~33% hull each)
    speed           : knots
    sonar_range     : nm radius for escort sonar detection
    visual_range    : nm radius for daytime visual detection
    dc_patterns     : (depth_charges_per_drop, drops_per_attack) — warships only
    gun_range       : nm for surface gun threat
    score_value     : patrol score multiplier (1.0 = standard merchant)
    silhouette_scale: scale factor for periscope rendering
    description     : flavour text
"""

SHIPS = [
    # ─── Merchants ─────────────────────────────────────────────────────────────
    {
        "id": "small_freighter",
        "name": "Small Freighter",
        "category": "merchant",
        "tonnage": 2800,
        "hp": 2,
        "speed": 9.0,
        "sonar_range": 0,
        "visual_range": 5,
        "dc_patterns": (0, 0),
        "gun_range": 0.0,
        "score_value": 0.8,
        "silhouette_scale": 0.6,
        "description": "Small coastal cargo vessel. Common but not high-value.",
    },
    {
        "id": "large_freighter",
        "name": "Large Freighter",
        "category": "merchant",
        "tonnage": 8200,
        "hp": 3,
        "speed": 11.0,
        "sonar_range": 0,
        "visual_range": 6,
        "dc_patterns": (0, 0),
        "gun_range": 0.0,
        "score_value": 1.0,
        "silhouette_scale": 1.0,
        "description": "Standard cargo vessel supplying the Japanese island garrisons.",
    },
    {
        "id": "tanker",
        "name": "Oil Tanker",
        "category": "merchant",
        "tonnage": 10500,
        "hp": 3,
        "speed": 10.0,
        "sonar_range": 0,
        "visual_range": 6,
        "dc_patterns": (0, 0),
        "gun_range": 0.0,
        "score_value": 1.4,
        "silhouette_scale": 1.1,
        "description": "Vital fuel supply ship. High priority target — flames spectacularly.",
    },
    {
        "id": "ammo_ship",
        "name": "Ammunition Ship",
        "category": "merchant",
        "tonnage": 7000,
        "hp": 2,
        "speed": 12.0,
        "sonar_range": 0,
        "visual_range": 6,
        "dc_patterns": (0, 0),
        "gun_range": 0.0,
        "score_value": 1.5,
        "silhouette_scale": 0.9,
        "description": "Carries ordnance and explosives. One hit often causes catastrophic explosion.",
    },
    {
        "id": "troop_transport",
        "name": "Troop Transport",
        "category": "merchant",
        "tonnage": 14000,
        "hp": 4,
        "speed": 15.0,
        "sonar_range": 0,
        "visual_range": 7,
        "dc_patterns": (0, 0),
        "gun_range": 0.5,
        "score_value": 1.6,
        "silhouette_scale": 1.2,
        "description": "Carries troops to island garrisons. Often heavily escorted.",
    },
    {
        "id": "passenger_cargo",
        "name": "Passenger-Cargo Ship",
        "category": "merchant",
        "tonnage": 9500,
        "hp": 3,
        "speed": 16.0,
        "sonar_range": 0,
        "visual_range": 6,
        "dc_patterns": (0, 0),
        "gun_range": 0.0,
        "score_value": 1.2,
        "silhouette_scale": 1.0,
        "description": "Fast and valuable — requisitioned liners carrying supplies and personnel.",
    },

    # ─── Escorts ───────────────────────────────────────────────────────────────
    {
        "id": "escort",
        "name": "Escort Vessel (Kaibokan)",
        "category": "escort",
        "tonnage": 940,
        "hp": 3,
        "speed": 17.5,
        "sonar_range": 3.0,
        "visual_range": 8,
        "dc_patterns": (7, 3),
        "gun_range": 2.0,
        "score_value": 1.0,
        "silhouette_scale": 0.5,
        "description": "Dedicated convoy escort. Good sonar, dangerous depth-charge capability.",
    },

    # ─── Warships ──────────────────────────────────────────────────────────────
    {
        "id": "destroyer",
        "name": "Destroyer",
        "category": "warship",
        "tonnage": 2500,
        "hp": 4,
        "speed": 35.0,
        "sonar_range": 4.0,
        "visual_range": 10,
        "dc_patterns": (10, 4),
        "gun_range": 4.0,
        "score_value": 2.0,
        "silhouette_scale": 0.7,
        "description": "Fast, deadly anti-submarine hunter. Primary depth-charge threat.",
    },
    {
        "id": "light_cruiser",
        "name": "Light Cruiser",
        "category": "warship",
        "tonnage": 8500,
        "hp": 6,
        "speed": 32.0,
        "sonar_range": 3.0,
        "visual_range": 10,
        "dc_patterns": (5, 2),
        "gun_range": 6.0,
        "score_value": 3.0,
        "silhouette_scale": 1.1,
        "description": "Well-armed cruiser with long-range guns. High-value target.",
    },
    {
        "id": "heavy_cruiser",
        "name": "Heavy Cruiser",
        "category": "warship",
        "tonnage": 15000,
        "hp": 8,
        "speed": 31.0,
        "sonar_range": 2.5,
        "visual_range": 10,
        "dc_patterns": (5, 2),
        "gun_range": 8.0,
        "score_value": 4.0,
        "silhouette_scale": 1.3,
        "description": "Formidable warship. Heavily armored — requires multiple torpedo hits.",
    },
    {
        "id": "battleship",
        "name": "Battleship",
        "category": "warship",
        "tonnage": 45000,
        "hp": 14,
        "speed": 27.0,
        "sonar_range": 2.0,
        "visual_range": 12,
        "dc_patterns": (5, 2),
        "gun_range": 12.0,
        "score_value": 8.0,
        "silhouette_scale": 2.0,
        "description": "The ultimate prize. Enormous but slow. Heavily defended. Requires a salvo of torpedoes.",
    },
    {
        "id": "carrier",
        "name": "Aircraft Carrier",
        "category": "warship",
        "tonnage": 28000,
        "hp": 10,
        "speed": 30.0,
        "sonar_range": 1.5,
        "visual_range": 12,
        "dc_patterns": (3, 1),
        "gun_range": 3.0,
        "score_value": 7.0,
        "silhouette_scale": 1.8,
        "description": "Strategic prize of the Pacific war. Large, fast but relies on escorts for defense.",
    },
]

SHIP_BY_ID = {s["id"]: s for s in SHIPS}

# Convoy composition templates: list of (ship_id, count) per category
CONVOY_TEMPLATES = [
    # Small coastal convoy
    [("small_freighter", 2), ("escort", 1)],
    # Standard supply convoy
    [("large_freighter", 3), ("small_freighter", 1), ("escort", 2)],
    # Tanker convoy — high value
    [("tanker", 2), ("large_freighter", 1), ("escort", 2), ("destroyer", 1)],
    # Troop convoy
    [("troop_transport", 2), ("passenger_cargo", 1), ("destroyer", 2), ("light_cruiser", 1)],
    # Ammo resupply
    [("ammo_ship", 2), ("small_freighter", 1), ("escort", 1)],
    # Single high-value merchant
    [("passenger_cargo", 1), ("destroyer", 1)],
    # Warship task force
    [("heavy_cruiser", 1), ("destroyer", 3)],
    # Major fleet
    [("battleship", 1), ("heavy_cruiser", 2), ("destroyer", 4)],
]
