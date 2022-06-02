from data.graphics import render_map

"""
Map structure

Each map is a dict named after the map, and in it, it's required to have:
    - "size" - a tuple, which determines the size of the map (width, height)
    - "player_starting_coordinates" - tuple of tuples containing starting coordinates for the player

The map has by default walls on the edges and nothing in the middle. This basic configuration is then overwritten by adding terms in this format:
(x, y): "entity_name"
For possible entity names, see graphics.py

Then, if you want any interactions, you add them separately in this format:
((x, y), "interaction_type"): {interaction_data}

Interaction types:
- "interaction"
    - Data: "interaction_name"
    - executes an interaction from the interaction() function

- "monologue"
    - Data: "dialog_strings_name"
    - plainly says smth from dialog_strings

- "teleport"
    - Data: ["map_name", "position_index"]
    - loads a map of the name, with a player on the position determined by the index (choosen from the "player_string_coordinates" list)
"""

world = {
    "village": {
        "size": (25, 15),
        "player_starting_coords": ((1, 1), (4, 4), (8, 7), (9, 11), (12, 6)),
        (3, 3): "wall",
        (3, 5): "wall",
        (2, 4): "wall",
        (3, 4): "door",
        ((3, 4), "teleport"): ("house_1", 0),

        (7, 6): "wall",
        (7, 8): "wall",
        (6, 7): "wall",
        (7, 7): "door",
        ((7, 7), "teleport"): ("house_2", 0),

        (8, 10): "wall",
        (8, 12): "wall",
        (7, 11): "wall",
        (8, 11): "door",
        ((8, 11), "teleport"): ("starting_house", 1),

        (11, 5): "wall",
        (11, 7): "wall",
        (10, 6): "wall",
        (11, 6): "door",
        ((11, 6), "teleport"): ("house_with_key", 0),
        (12, 6): "enemy",
        ((12, 6), "interaction"): "wolf_first_fight",

        (14, 8): "friend",
        ((14, 8), "interaction"): "villager_wolf_attack",

        (23, 6): "wall",
        (23, 8): "wall",
        (22, 6): "friend",
        ((22, 6), "interaction"): "gatekeeper",
        (24, 7): "door",
        ((24, 7), "interaction"): "gate",
        ((24, 7), "teleport"): ("demo_end_area", 0),

        (3, 1): "collectable",
        ((3, 1), "interaction"): "collect_weapon"
    },

    "house_1": {
        "size": (6, 6),
        "player_starting_coords": ((4, 4),),
        (1, 1): "collectable",
        ((1, 1), "interaction"): "collect_coins",
        (5, 4): "door",
        ((5, 4), "teleport"): ("village", 1)
    },

    "house_2": {
        "size": (6, 6),
        "player_starting_coords": ((4, 4),),
        (1, 1): "friend",
        ((1, 1), "monologue"): "old_friend_village",
        (5, 4): "door",
        ((5, 4), "teleport"): ("village", 2)
    },

    "starting_house": {
        "size": (6, 6),
        "player_starting_coords": ((1, 1), (4, 4)),
        (4, 1): "collectable",
        ((4, 1), "interaction"): "collect_coins",
        (4, 4): "friend",
        ((4, 4), "interaction"): "Vorin_first_meet",
        (5, 4): "door",
        ((5, 4), "teleport"): ("village", 3)
    },

    "house_with_key": {
        "size": (6, 6),
        "player_starting_coords": ((4, 4), (5, 5)),
        (1, 1): "collectable",
        ((1, 1), "interaction"): "gate_key_collect",
        (5, 4): "door",
        ((5, 4), "teleport"): ("village", 4)
    },

    "demo_end_area": {
        "size": (5, 5),
        "player_starting_coords": ((1, 2),),
        (3, 2): "friend",
        ((3, 2), "monologue"): "demo_end"
    }
}
"""
    "louka": { #text něco jako napadli vás skřeti schovej se do jeskyně
        "size": (9, 9),
        "player_starting_coords": ((1, 1), (1, 2)),
        (3, 3): "wall",
        (3, 5): "wall",
        (2, 4): "wall",
        (3, 4): "door",
        ((3, 4), "teleport"): ("jeskyne1", 0)
        
    },

    "jeskyne1": {
        "size": (8, 8),
        "player_starting_coords": ((1, 1), (1, 2)),
        (1, 2): "collectable", #meč žihadlo
        (6, 6): "door",
        ((6, 6), "teleport"): ("jeskyne2", 0)
    },

    "jeskyne2": {
        "size": (8, 8),
        "player_starting_coords": ((1, 1), (1, 2)),
        (6, 5): "friend", #glum
        (4, 4): "collectable", #prsten
        (6, 6): "door",
        ((6, 6), "teleport"): ("hvozd", 0),
        
    },

     "hvozd": { #úkol zabít pavouky a zachránit ostatní
        "size": (10, 10),
        "player_starting_coords": ((1, 1), (1, 2)),
        (2, 3): "friend",
        (4, 3): "friend",
        (6, 3): "friend",
        (2, 4): "enemy", #pavouk1
        (4, 4): "enemy", #pavouk2
        (6, 4): "enemy", #pavouk3
        (8, 8): "door",
        ((8, 8), "teleport"): ("hora1", 0),
    },

    "hora1": { #před horou
        "size": (13, 13),
        "player_starting_coords": ((1, 1), (1, 2)),
        (6, 4): "wall",
        (7, 4): "wall",
        (4, 5): "wall",
        (8, 5): "wall",
        (4, 6): "wall",
        (9, 6): "wall",
        (3, 7): "wall",
        (10, 7): "wall",
        (4, 8): "wall",
        (5, 8): "wall",
        (6, 8): "wall",
        (7, 8): "wall",
        (8, 8): "wall",
        (9, 8): "wall",
        (5, 4): "door",
        ((5, 4), "teleport"): ("hora2", 0)
    },

    "hora2": { #úkol zabít draka
        "size": (9, 9),
        "player_starting_coords": ((1, 1), (1, 2)),
        (4, 4): "enemy", #drak
    },
}
"""

# loads a map from world
def load_map(name, position_index = 0):         
    map = world[name]                                                       # chooses the map from world depending on the name
    map["player"] = list(map["player_starting_coords"][position_index])     # overwrites the player coordinates to be on the right spot
    render_map(map)                                                         # map is then rendered
    return map                                                              # and returned
