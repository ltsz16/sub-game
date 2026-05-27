"""
data/historical_events.py — WWII Pacific events timeline 1941-1945.

Each event:
    date        : (year, month, day) tuple
    title       : short headline
    body        : paragraph of text (newspaper style)
    impact      : dict of gameplay effects
        patrol_areas_blocked : list of area IDs to close
        patrol_areas_opened  : list of area IDs to open
        enemy_density_mult   : float multiplier on enemy frequency (1.0=normal)
        enemy_warship_mult   : float multiplier on warship presence
        base_changes         : dict {base_id: "open"/"close"}
"""

EVENTS = [
    {
        "date": (1941, 12, 7),
        "title": "JAPAN ATTACKS PEARL HARBOR",
        "body": (
            "Japanese carrier aircraft have launched a devastating surprise attack on "
            "the US Naval Base at Pearl Harbor, Hawaii. Eight battleships were sunk or "
            "damaged, along with numerous other vessels. 2,403 Americans have been killed. "
            "The United States is now at war with Japan. All submarines are ordered to begin "
            "war patrols immediately. Shoot on sight."
        ),
        "impact": {
            "patrol_areas_opened": ["luzon_strait", "south_china_sea", "formosa",
                                    "empire_waters", "marianas", "palau"],
            "patrol_areas_blocked": [],
            "enemy_density_mult": 1.0,
            "enemy_warship_mult": 1.2,
            "base_changes": {"pearl_harbor": "open", "cavite": "open", "fremantle": "open"},
        },
    },
    {
        "date": (1942, 1, 10),
        "title": "FALL OF MANILA — CAVITE BASE LOST",
        "body": (
            "Japanese forces have captured Manila and the Cavite Naval Yard has been "
            "abandoned. Submarines previously based in the Philippines must now operate "
            "from Fremantle, Australia or Pearl Harbor. Supply lines to the Philippines "
            "are being cut off. Concentrate patrols in the South China Sea and Luzon Strait."
        ),
        "impact": {
            "patrol_areas_opened": [],
            "patrol_areas_blocked": [],
            "enemy_density_mult": 1.1,
            "enemy_warship_mult": 1.3,
            "base_changes": {"cavite": "close"},
        },
    },
    {
        "date": (1942, 4, 18),
        "title": "DOOLITTLE RAID STRIKES TOKYO",
        "body": (
            "B-25 Mitchell bombers launched from USS Hornet have bombed Tokyo and other "
            "Japanese cities in a daring raid led by Lt. Col. Jimmy Doolittle. Though "
            "damage was limited, the psychological impact was enormous. Japan is now "
            "reinforcing home waters and the defensive perimeter. Expect increased "
            "anti-submarine patrols near the Empire."
        ),
        "impact": {
            "patrol_areas_opened": [],
            "patrol_areas_blocked": [],
            "enemy_density_mult": 1.0,
            "enemy_warship_mult": 1.4,
            "base_changes": {},
        },
    },
    {
        "date": (1942, 5, 8),
        "title": "BATTLE OF THE CORAL SEA",
        "body": (
            "In a historic first, the Coral Sea naval battle has been fought entirely by "
            "carrier aircraft — no surface ships engaged each other directly. USS Lexington "
            "was lost but the Japanese invasion of Port Moresby was turned back. "
            "The carrier Shoho was sunk. Japanese carrier power is being whittled down."
        ),
        "impact": {
            "patrol_areas_opened": ["coral_sea", "solomon_sea"],
            "patrol_areas_blocked": [],
            "enemy_density_mult": 1.1,
            "enemy_warship_mult": 1.2,
            "base_changes": {"brisbane": "open"},
        },
    },
    {
        "date": (1942, 6, 4),
        "title": "DECISIVE VICTORY AT MIDWAY",
        "body": (
            "US forces have achieved a stunning victory at Midway Island. Four Japanese "
            "fleet carriers — Akagi, Kaga, Soryu, and Hiryu — have been sunk along with "
            "a heavy cruiser. Japan has lost the strategic initiative. The tide in the "
            "Pacific is turning. Submarine patrols in the Central Pacific area are now "
            "critically important to interdict Japanese resupply efforts."
        ),
        "impact": {
            "patrol_areas_opened": ["central_pacific"],
            "patrol_areas_blocked": [],
            "enemy_density_mult": 0.9,
            "enemy_warship_mult": 0.8,
            "base_changes": {"midway": "open"},
        },
    },
    {
        "date": (1942, 8, 7),
        "title": "MARINES LAND ON GUADALCANAL",
        "body": (
            "US Marines have landed on Guadalcanal in the Solomon Islands, beginning a "
            "grueling six-month campaign. The Japanese are running the 'Tokyo Express' — "
            "destroyer convoys at night — to resupply and reinforce their troops. "
            "Submarines are urgently needed to interdict this supply route. The waters "
            "around the Solomons are heavily patrolled by both sides."
        ),
        "impact": {
            "patrol_areas_opened": ["guadalcanal"],
            "patrol_areas_blocked": [],
            "enemy_density_mult": 1.3,
            "enemy_warship_mult": 1.5,
            "base_changes": {},
        },
    },
    {
        "date": (1943, 2, 9),
        "title": "GUADALCANAL SECURED",
        "body": (
            "After six months of bitter fighting, Guadalcanal has been secured. Japanese "
            "forces have been evacuated. This is the first major land victory against Japan "
            "and proves they can be pushed back. The submarine campaign against Japanese "
            "supply lines has contributed significantly to the victory by cutting off "
            "reinforcements and supplies."
        ),
        "impact": {
            "patrol_areas_opened": [],
            "patrol_areas_blocked": [],
            "enemy_density_mult": 1.0,
            "enemy_warship_mult": 0.9,
            "base_changes": {},
        },
    },
    {
        "date": (1943, 11, 20),
        "title": "GILBERTS CAMPAIGN — TARAWA FALLS",
        "body": (
            "US forces have seized Tarawa and Makin in the Gilbert Islands after fierce "
            "fighting. The island-hopping campaign is underway. Japanese shipping lanes "
            "are being squeezed. Submarine operations in the Central Pacific are yielding "
            "excellent results as enemy merchant tonnage plummets. New Mark 18 electric "
            "torpedoes are now available — no bubble wake to betray your position."
        ),
        "impact": {
            "patrol_areas_opened": ["gilberts"],
            "patrol_areas_blocked": [],
            "enemy_density_mult": 1.1,
            "enemy_warship_mult": 0.8,
            "base_changes": {},
        },
    },
    {
        "date": (1944, 2, 1),
        "title": "OPERATION FLINTLOCK — MARSHALLS INVADED",
        "body": (
            "US forces have stormed the Marshall Islands. Kwajalein and Roi-Namur have "
            "fallen, and Eniwetok will soon follow. The outer defensive ring of the "
            "Japanese Empire is crumbling. Submarine wolf-pack operations are being "
            "expanded. Convoys are now being targeted with coordinated multi-submarine attacks."
        ),
        "impact": {
            "patrol_areas_opened": ["marshalls"],
            "patrol_areas_blocked": [],
            "enemy_density_mult": 1.2,
            "enemy_warship_mult": 0.7,
            "base_changes": {},
        },
    },
    {
        "date": (1944, 6, 19),
        "title": "GREAT MARIANAS TURKEY SHOOT",
        "body": (
            "The Battle of the Philippine Sea has been a catastrophic defeat for Japan. "
            "Over 600 Japanese aircraft have been destroyed and three carriers sunk — "
            "including the giants Taiho and Shokaku. US submarines contributed by sinking "
            "both fleet carriers. Japanese naval air power is effectively destroyed. "
            "Saipan will soon fall, bringing Japan within B-29 bombing range."
        ),
        "impact": {
            "patrol_areas_opened": ["marianas"],
            "patrol_areas_blocked": [],
            "enemy_density_mult": 1.3,
            "enemy_warship_mult": 0.6,
            "base_changes": {},
        },
    },
    {
        "date": (1944, 10, 23),
        "title": "BATTLE OF LEYTE GULF — JAPAN'S LAST STAND",
        "body": (
            "The largest naval battle in history has been fought at Leyte Gulf. The "
            "Japanese navy has been virtually annihilated — 4 carriers, 3 battleships, "
            "10 cruisers, and 11 destroyers sunk. The Philippines are being liberated. "
            "Japanese convoys are now desperately scrambling for any route to resupply "
            "their forces. The end of the war is in sight."
        ),
        "impact": {
            "patrol_areas_opened": ["leyte_gulf", "mindanao"],
            "patrol_areas_blocked": [],
            "enemy_density_mult": 1.4,
            "enemy_warship_mult": 0.4,
            "base_changes": {},
        },
    },
    {
        "date": (1945, 2, 19),
        "title": "MARINES STORM IWO JIMA",
        "body": (
            "US Marines have landed on Iwo Jima in the most costly battle in Marine Corps "
            "history. The island brings US fighters within range of Japan itself. Submarine "
            "operations now extend into waters close to the Japanese home islands. Enemy "
            "shipping has been pushed into coastal routes but is becoming increasingly "
            "scarce as Japan's merchant fleet approaches annihilation."
        ),
        "impact": {
            "patrol_areas_opened": ["tokyo_bay", "sea_of_japan"],
            "patrol_areas_blocked": [],
            "enemy_density_mult": 1.5,
            "enemy_warship_mult": 0.3,
            "base_changes": {},
        },
    },
    {
        "date": (1945, 4, 1),
        "title": "INVASION OF OKINAWA BEGINS",
        "body": (
            "The largest amphibious assault in the Pacific has begun at Okinawa — just "
            "340 miles from Japan. Japanese Kamikaze attacks are causing severe casualties "
            "to the invasion fleet. The Yamato, the world's largest battleship, has been "
            "sunk by US aircraft on a one-way mission. The final campaign against Japan's "
            "home islands is being planned."
        ),
        "impact": {
            "patrol_areas_opened": [],
            "patrol_areas_blocked": [],
            "enemy_density_mult": 1.6,
            "enemy_warship_mult": 0.2,
            "base_changes": {},
        },
    },
    {
        "date": (1945, 8, 15),
        "title": "JAPAN SURRENDERS — WAR OVER",
        "body": (
            "Emperor Hirohito has announced Japan's unconditional surrender following the "
            "atomic bombing of Hiroshima and Nagasaki. The war in the Pacific is over. "
            "US submarines sank 1,314 ships totaling 5.3 million tons — 55% of all "
            "Japanese shipping lost during the war. The submarine service paid dearly: "
            "52 submarines and 3,506 officers and men were lost. Your service record "
            "will now be evaluated. Well done, Commander."
        ),
        "impact": {
            "patrol_areas_opened": [],
            "patrol_areas_blocked": ["luzon_strait", "south_china_sea", "formosa",
                                      "empire_waters", "marianas", "palau", "coral_sea",
                                      "central_pacific", "guadalcanal", "gilberts",
                                      "marshalls", "leyte_gulf", "tokyo_bay", "sea_of_japan"],
            "enemy_density_mult": 0.0,
            "enemy_warship_mult": 0.0,
            "base_changes": {},
        },
    },
]
