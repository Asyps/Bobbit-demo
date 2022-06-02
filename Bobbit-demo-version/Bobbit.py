from msvcrt import getch

from data.Andrews_magic import *
from data.maps import *
from data.graphics import *
from data.interactions import *

vt_seq_win()

PlaySound("./data/music/title-theme.wav", SND_FILENAME | SND_LOOP | SND_ASYNC)
fancy_print("\033cBobbit\n\n\n\n\n\nDemo verze\n\nStiskněte cokoliv pro počátek hry ")
getch()

fancy_print("Kdysi dávno...")
sleep(dialog_pace * 3)
PlaySound("./data/music/main-theme.wav", SND_FILENAME | SND_LOOP | SND_ASYNC)

current_map = "starting_house"
map = load_map("starting_house", 0)

# movement and interactions
while True:
    inp = getch()

    if inp == b'i':             # this is for testing
        print("\033c", end = "")
        print_stats(player_stats)
        print_inventory(inventory)
        sleep(dialog_pace)
        render_map(map)
        continue

    elif inp == b'w':
        coords = (map["player"][0], map["player"][1] - 1)
        a, b  = 1, -1
                    
    elif inp == b'a':
        coords = (map["player"][0] - 1, map["player"][1])
        a, b = 0, -1

    elif inp == b's':
        coords = (map["player"][0], map["player"][1] + 1)
        a, b = 1, 1
            
    elif inp == b'd':
        coords = (map["player"][0] + 1, map["player"][1])
        a, b = 0, 1
    
    else:
        continue

    # move or interact
    if coords not in map:
        if not (0 in coords or coords[0] == map["size"][0]-1 or coords[1] == map["size"][1]-1):
            overwrite(*map["player"], "blank", map["size"][1] + 1)
            map["player"][a] += b
            overwrite(*map["player"], "player", map["size"][1] + 1)

    elif (coords, "interaction") in map:
        current_check = (coords, "interaction")
        deletion_option = interaction(map[current_check])           
        if deletion_option == 1 or deletion_option == 2:
            del map[current_check]
        if deletion_option == 2:
            del map[coords]
        
        render_map(map)

    elif (coords, "monologue") in map:
        say(map[(coords, "monologue")])
        render_map(map)
  
    elif (coords, "teleport") in map:
        current_check = (coords, "teleport")
        world[current_map] = map
        current_map = map[current_check][0]
        map = load_map(*map[current_check])
