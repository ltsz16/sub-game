"""
data/patrol_areas.py — Pacific Ocean patrol zones and home ports.

Coordinate system: lat/lon in degrees (positive=N/E, negative=S/W).
Center of each zone given plus rough radius in degrees.

Ports:
    id          : unique key
    name        : display name
    lon, lat    : location
    available   : whether open at game start

Patrol Areas:
    id              : unique key
    name            : display name
    center_lon      : center longitude
    center_lat      : center latitude
    radius_deg      : approximate patrol zone radius in degrees
    accessible_from : list of port IDs that can reach this area
    convoy_density  : float 0-3 (enemy traffic density)
    warship_density : float 0-1 (warship encounter probability)
    year_opened     : year this area becomes relevant
    description     : flavour text
"""

PORTS = [
    {
        "id": "pearl_harbor",
        "name": "Pearl Harbor, Hawaii",
        "lon": -157.95,
        "lat": 21.36,
        "available": True,
    },
    {
        "id": "fremantle",
        "name": "Fremantle, Australia",
        "lon": 115.74,
        "lat": -32.05,
        "available": True,
    },
    {
        "id": "brisbane",
        "name": "Brisbane, Australia",
        "lon": 153.02,
        "lat": -27.47,
        "available": False,
    },
    {
        "id": "midway",
        "name": "Midway Island",
        "lon": -177.37,
        "lat": 28.21,
        "available": False,
    },
    {
        "id": "cavite",
        "name": "Cavite, Philippines",
        "lon": 120.90,
        "lat": 14.49,
        "available": True,   # closed by event Jan 1942
    },
]

PORT_BY_ID = {p["id"]: p for p in PORTS}

PATROL_AREAS = [
    {
        "id": "luzon_strait",
        "name": "Luzon Strait",
        "center_lon": 121.5,
        "center_lat": 20.5,
        "radius_deg": 3.5,
        "accessible_from": ["cavite", "pearl_harbor", "fremantle"],
        "convoy_density": 2.5,
        "warship_density": 0.4,
        "year_opened": 1941,
        "description": "Critical chokepoint between the Philippines and Formosa. "
                        "Main Japanese convoy route from the Empire to Southeast Asia.",
    },
    {
        "id": "south_china_sea",
        "name": "South China Sea",
        "center_lon": 112.0,
        "center_lat": 12.0,
        "radius_deg": 6.0,
        "accessible_from": ["cavite", "fremantle"],
        "convoy_density": 2.0,
        "warship_density": 0.3,
        "year_opened": 1941,
        "description": "Vast sea lanes supplying Japanese oil and resources from "
                        "the Dutch East Indies. Excellent hunting grounds.",
    },
    {
        "id": "formosa",
        "name": "Formosa Strait",
        "center_lon": 119.5,
        "center_lat": 23.5,
        "radius_deg": 2.5,
        "accessible_from": ["cavite", "pearl_harbor"],
        "convoy_density": 2.8,
        "warship_density": 0.5,
        "year_opened": 1941,
        "description": "Narrow, heavily trafficked waters between Formosa and the "
                        "Chinese coast. Dangerous but very rewarding.",
    },
    {
        "id": "empire_waters",
        "name": "Empire Waters (Home Islands)",
        "center_lon": 135.0,
        "center_lat": 33.0,
        "radius_deg": 5.0,
        "accessible_from": ["pearl_harbor", "midway"],
        "convoy_density": 1.5,
        "warship_density": 0.7,
        "year_opened": 1941,
        "description": "The most dangerous waters in the Pacific — Japanese home "
                        "waters teeming with ASW patrols. Highest risk, highest reward.",
    },
    {
        "id": "marianas",
        "name": "Marianas / Caroline Islands",
        "center_lon": 148.0,
        "center_lat": 13.5,
        "radius_deg": 4.0,
        "accessible_from": ["pearl_harbor", "midway"],
        "convoy_density": 1.8,
        "warship_density": 0.5,
        "year_opened": 1941,
        "description": "The island chains connecting Japan to its southern empire. "
                        "Truk Lagoon nearby serves as the main Japanese naval base.",
    },
    {
        "id": "palau",
        "name": "Palau Islands",
        "center_lon": 134.5,
        "center_lat": 7.5,
        "radius_deg": 3.0,
        "accessible_from": ["fremantle", "cavite", "brisbane"],
        "convoy_density": 2.0,
        "warship_density": 0.4,
        "year_opened": 1941,
        "description": "Important Japanese staging area between the Philippines and the Carolines.",
    },
    {
        "id": "coral_sea",
        "name": "Coral Sea",
        "center_lon": 154.0,
        "center_lat": -16.0,
        "radius_deg": 5.0,
        "accessible_from": ["brisbane", "fremantle"],
        "convoy_density": 1.3,
        "warship_density": 0.4,
        "year_opened": 1942,
        "description": "Scene of the famous 1942 carrier battle. Japanese supply lines "
                        "to New Guinea run through here.",
    },
    {
        "id": "solomon_sea",
        "name": "Solomon Sea",
        "center_lon": 156.0,
        "center_lat": -8.0,
        "radius_deg": 3.5,
        "accessible_from": ["brisbane"],
        "convoy_density": 1.8,
        "warship_density": 0.6,
        "year_opened": 1942,
        "description": "Home to the Tokyo Express destroyer convoys supplying Guadalcanal.",
    },
    {
        "id": "guadalcanal",
        "name": "Guadalcanal / Iron Bottom Sound",
        "center_lon": 160.0,
        "center_lat": -9.5,
        "radius_deg": 3.0,
        "accessible_from": ["brisbane"],
        "convoy_density": 2.2,
        "warship_density": 0.8,
        "year_opened": 1942,
        "description": "The bitterly contested island and surrounding waters. Both "
                        "sides have lost so many ships here the sound is called Iron Bottom.",
    },
    {
        "id": "central_pacific",
        "name": "Central Pacific",
        "center_lon": -170.0,
        "center_lat": 15.0,
        "radius_deg": 8.0,
        "accessible_from": ["pearl_harbor", "midway"],
        "convoy_density": 1.2,
        "warship_density": 0.3,
        "year_opened": 1942,
        "description": "Vast open ocean. Encounters are less frequent but "
                        "the area provides a pathway toward the Marianas.",
    },
    {
        "id": "gilberts",
        "name": "Gilbert / Marshall Islands",
        "center_lon": 172.0,
        "center_lat": 3.0,
        "radius_deg": 4.0,
        "accessible_from": ["pearl_harbor", "midway"],
        "convoy_density": 1.5,
        "warship_density": 0.4,
        "year_opened": 1943,
        "description": "Island chains that served as forward Japanese bases. "
                        "Target of major US amphibious operations in late 1943.",
    },
    {
        "id": "marshalls",
        "name": "Marshall Islands",
        "center_lon": 167.0,
        "center_lat": 9.0,
        "radius_deg": 4.0,
        "accessible_from": ["pearl_harbor", "midway"],
        "convoy_density": 1.5,
        "warship_density": 0.4,
        "year_opened": 1944,
        "description": "Seized by US forces in early 1944. Provides forward base "
                        "for continuing the Central Pacific drive.",
    },
    {
        "id": "leyte_gulf",
        "name": "Leyte Gulf / Philippines",
        "center_lon": 125.5,
        "center_lat": 11.0,
        "radius_deg": 3.5,
        "accessible_from": ["fremantle", "brisbane", "pearl_harbor"],
        "convoy_density": 1.8,
        "warship_density": 0.5,
        "year_opened": 1944,
        "description": "Scene of the greatest naval battle in history. "
                        "Philippine liberation is underway.",
    },
    {
        "id": "mindanao",
        "name": "Mindanao Sea",
        "center_lon": 124.0,
        "center_lat": 7.5,
        "radius_deg": 3.0,
        "accessible_from": ["fremantle", "brisbane"],
        "convoy_density": 1.6,
        "warship_density": 0.4,
        "year_opened": 1944,
        "description": "Southern Philippine waters, increasingly important as "
                        "Japanese forces are pushed north.",
    },
    {
        "id": "tokyo_bay",
        "name": "Tokyo Bay / Approaches",
        "center_lon": 139.8,
        "center_lat": 35.0,
        "radius_deg": 2.0,
        "accessible_from": ["pearl_harbor", "midway"],
        "convoy_density": 1.0,
        "warship_density": 0.9,
        "year_opened": 1945,
        "description": "The most dangerous water on earth — inside the enemy's front door. "
                        "Extreme ASW patrols but convoys still run in desperation.",
    },
    {
        "id": "sea_of_japan",
        "name": "Sea of Japan",
        "center_lon": 134.0,
        "center_lat": 38.0,
        "radius_deg": 4.0,
        "accessible_from": ["pearl_harbor", "midway"],
        "convoy_density": 2.0,
        "warship_density": 0.5,
        "year_opened": 1945,
        "description": "Landlocked waters between Japan and the Asian continent. "
                        "In 1945 submarines penetrated here for devastating effect.",
    },
]

AREA_BY_ID = {a["id"]: a for a in PATROL_AREAS}
