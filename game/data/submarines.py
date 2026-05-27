"""
data/submarines.py — All playable US submarine types (WW2 Pacific).

Each entry is a dict with the following keys:
    name            : class name
    year_available  : first year usable in career
    max_depth       : crush depth in feet
    speed_surface   : knots surfaced
    speed_submerged : knots submerged
    tubes_fore      : number of forward torpedo tubes
    tubes_aft       : number of aft torpedo tubes
    torpedo_capacity: total torpedoes carried
    deck_guns       : list of (caliber_mm, description)
    battery_hours   : hours of battery at 2-knot submerged speed
    fuel_range_nm   : surface range in nautical miles
    crew            : crew complement
    displacement    : surface displacement (tons)
    description     : short flavour text
"""

SUBMARINES = [
    {
        "id": "s_class",
        "name": "S-Class",
        "year_available": 1941,
        "max_depth": 200,
        "speed_surface": 14.5,
        "speed_submerged": 11.0,
        "tubes_fore": 4,
        "tubes_aft": 1,
        "torpedo_capacity": 12,
        "deck_guns": [(76, '3\"/23 deck gun')],
        "battery_hours": 30,
        "fuel_range_nm": 5000,
        "crew": 42,
        "displacement": 876,
        "description": (
            "Obsolete WWI-era design. Limited range and depth, but available "
            "at war's outbreak in the Asiatic Fleet. Often assigned early Pacific patrols."
        ),
    },
    {
        "id": "porpoise",
        "name": "Porpoise-Class",
        "year_available": 1941,
        "max_depth": 250,
        "speed_surface": 19.0,
        "speed_submerged": 8.75,
        "tubes_fore": 6,
        "tubes_aft": 4,
        "torpedo_capacity": 16,
        "deck_guns": [(76, '3\"/50 deck gun')],
        "battery_hours": 36,
        "fuel_range_nm": 10000,
        "crew": 55,
        "displacement": 1310,
        "description": (
            "Pre-war design incorporating lessons from S-class. Better range and "
            "armament make it a capable fleet submarine."
        ),
    },
    {
        "id": "salmon",
        "name": "Salmon/Sargo-Class",
        "year_available": 1941,
        "max_depth": 250,
        "speed_surface": 21.0,
        "speed_submerged": 9.0,
        "tubes_fore": 8,
        "tubes_aft": 4,
        "torpedo_capacity": 24,
        "deck_guns": [(76, '3\"/50 deck gun')],
        "battery_hours": 40,
        "fuel_range_nm": 11000,
        "crew": 59,
        "displacement": 1450,
        "description": (
            "An improvement over the Porpoise, with more tubes and a higher surface speed. "
            "Sargo class added modifications improving reliability."
        ),
    },
    {
        "id": "tambor",
        "name": "Tambor/Gar-Class",
        "year_available": 1941,
        "max_depth": 300,
        "speed_surface": 20.0,
        "speed_submerged": 8.75,
        "tubes_fore": 6,
        "tubes_aft": 4,
        "torpedo_capacity": 24,
        "deck_guns": [(76, '3\"/50 deck gun')],
        "battery_hours": 48,
        "fuel_range_nm": 11000,
        "crew": 60,
        "displacement": 1475,
        "description": (
            "The first true fleet submarines, capable of operating with surface forces. "
            "Reliable and well-armed, they formed the backbone of early patrols."
        ),
    },
    {
        "id": "gato",
        "name": "Gato-Class",
        "year_available": 1942,
        "max_depth": 300,
        "speed_surface": 20.25,
        "speed_submerged": 8.75,
        "tubes_fore": 6,
        "tubes_aft": 4,
        "torpedo_capacity": 24,
        "deck_guns": [(76, '3\"/50 deck gun'), (20, '20mm AA gun')],
        "battery_hours": 48,
        "fuel_range_nm": 11000,
        "crew": 60,
        "displacement": 1526,
        "description": (
            "The definitive WWII US submarine. 77 boats commissioned. Gato-class subs "
            "sank more enemy tonnage than any other class. The workhorse of the Pacific."
        ),
    },
    {
        "id": "balao",
        "name": "Balao-Class",
        "year_available": 1943,
        "max_depth": 400,
        "speed_surface": 20.25,
        "speed_submerged": 8.75,
        "tubes_fore": 6,
        "tubes_aft": 4,
        "torpedo_capacity": 24,
        "deck_guns": [(102, '4\"/50 deck gun'), (40, '40mm Bofors'), (20, '20mm AA')],
        "battery_hours": 48,
        "fuel_range_nm": 11000,
        "crew": 60,
        "displacement": 1526,
        "description": (
            "Improved Gato with high-tensile steel hull allowing 400ft operating depth. "
            "Virtually identical externally but far safer in deep-water evasion."
        ),
    },
    {
        "id": "tench",
        "name": "Tench-Class",
        "year_available": 1944,
        "max_depth": 400,
        "speed_surface": 20.25,
        "speed_submerged": 8.75,
        "tubes_fore": 6,
        "tubes_aft": 4,
        "torpedo_capacity": 28,
        "deck_guns": [(102, '4\"/50 deck gun'), (40, '40mm Bofors'), (20, '20mm AA')],
        "battery_hours": 60,
        "fuel_range_nm": 11000,
        "crew": 66,
        "displacement": 1570,
        "description": (
            "The final and most refined US WWII submarine design. Improved habitability, "
            "larger battery, 28-torpedo capacity. Very few saw extended combat before war's end."
        ),
    },
]

# Index by id for quick lookup
SUBMARINE_BY_ID = {s["id"]: s for s in SUBMARINES}
