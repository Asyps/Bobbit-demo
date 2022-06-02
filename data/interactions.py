from winsound import PlaySound, SND_LOOP, SND_ASYNC, SND_FILENAME
from json import load
from time import sleep
from random import randint

inventory = {
    "coins": 0,
    "heals": 0
}
weapons = ["ruka", "klacek", "palice"]
player_stats = {
    "hp": 15, 
    "dmg": 0
}
world_flags = {
    "village_wolf_killed": False,
    "gate_key_collected": False,
    "is_gate_open": False
}
is_gate_open = False

print("\033cDisclaimer: Tato hra je testována pouze pro visual studio code, a je možné, že na jiných konzolích apod. nebude fungovat. Hrajte jinde na vlastní nebezpečí.")
sleep(1.25)
print("Pokud máte visual studio code, prosím, zvětšete toto okno s konzolí na co největší velikost, abyste zamezili rozbití hry.")
sleep(1.25)

# determines the pace of dialogs
while True:
    dialog_pace = input("Jak rychlé chcete dialogy [pomalé/střední/rychlé]: ")
    if dialog_pace == "pomalé":
        dialog_pace = 1.25                                  # this number then multiplies the seconds in sleep() functions
        break
    elif dialog_pace == "střední":
        dialog_pace = 1
        break
    elif dialog_pace == "rychlé":
        dialog_pace = 0.75
        break

# load the JSON
with open("./data/dialog_strings.json", encoding="utf-8") as data: 
    data = load(data)                                       # load() turns data into a dictionary usable in python


# prints in a fancy way
def fancy_print(to_print, newline=True):
    for i in to_print:
        print(i, end = "", flush = True)                    # prints the appropriate text character by character, flush ensures it always prints
        sleep(dialog_pace * 0.05)
    if newline:
        print()

# prints the statistics
def print_stats(stats):
    fancy_print("Zdraví: {0} \nSíla: {1}\n" . format(stats["hp"], stats["dmg"]))
    sleep(dialog_pace * 0.75)

# prints the inventory
def print_inventory(inventory):
    fancy_print("Mince: {0}\nLéčivé lektvary: {1}\n" . format(inventory["coins"], inventory["heals"]))
    sleep(dialog_pace * 0.75)

# says smth (from the JSON file)
def say(name, does_clear = True, end=""):                                         
    if does_clear:
        print("\033c", end = "")                            # clears the console if the parameter does_clear is True
    
    fancy_print(data[name] + str(end))                    # adds the end parameter to the end

    sleep(dialog_pace * 1.5)
"""
syntax for say() in JSON:

"name": "text",
"""

# asks a question (from the JSON file)
def ask(name, does_clear = True):
    text = data[name]                                       # takes the according dictionary from data into it's own variable
    options = ""

    if does_clear:
        print("\033c", end = "")

    fancy_print(text["greet"])                              # greet is printed first

    sleep(dialog_pace * 1)
         
    for i in text.keys():                                   # this part generates the brackets after the question - [opt1/opt2/.../optN]
        if i not in "greet ask":                            # it adds all keywords that are not greet or ask into the string
            options += "/" + i

    while True:
        fancy_print(text["ask"] + " [" + options[1:] + "] ", False)   # this assembles the question text, options[1:] is to get rid of the first /

        inp = input()                                       # asks the question
        
        if inp in text.keys() and not inp in "greet ask":   # checks if the awnser is valid, if not, the cycle asks again
            sleep(dialog_pace * 0.25)

            fancy_print(text[inp])                          # prints the text for the choosen option

            sleep(dialog_pace * 1)
            return inp                                      # returns the choosen option name
"""
syntax for ask() in JSON:

"name": {
    "greet": "what to say first",
    "ask": "the question",

    "option 1": "text to say for option 1",
    "option 2": "text to say for option 2",
    ...
    "option N": "text to say for option N"
},

note: the choosen option name is returned 
"""
# asks a math question to determine success/failure of certain task
def math_question(difficulty):                                          # difficulty can be >= 0  
    def check_type(awnser, type):
        if type == "float":                                             # awnser checking function
            try:
                PlaySound("./data/music/main-theme.wav", SND_FILENAME | SND_LOOP | SND_ASYNC)
                return False, float(awnser)
            except:
                return True, None
        elif type == "int":
            try:
                return False, int(awnser)
            except:
                return True, None

    invalid_awnser = True
    is_correct = False
    
    if difficulty < 2:
        operation = randint(1, 2)
    elif difficulty < 4:                                                # depending on the difficulty, an operation is choosen
        operation = randint(1, 3)
    else:
        operation = randint(1, 4)

    number1 = randint(difficulty, 5*difficulty+2)                       # number1 is always choosen the same
    
    if operation == 4:
        number2 = randint(1, difficulty+2)
    elif operation == 3:                                                # and number2 is choosen depending on the operation
        number2 = randint(0, 4*difficulty+2)                            # to prevent division by 0 and moderate the difficulty
    else: 
        number2 = randint(0, 5*difficulty+2)

    if operation == 1:                                                  # chain of if's determines the operation
        while invalid_awnser:    
            fancy_print(f"\nKolik je {number1} plus {number2}? ")
            invalid_awnser, awnser = check_type(input(), "int")         # awnser is always checked for type
        if awnser == number1 + number2:                                 # you can be wrong only within the correct type
            sleep(dialog_pace * 1)
            is_correct = True

    elif operation == 2:
        while invalid_awnser:    
            fancy_print(f"\nKolik je {number1} mínus {number2}? ")
            invalid_awnser, awnser = check_type(input(), "int")
        if awnser == number1 - number2:
            sleep(dialog_pace * 1)
            is_correct = True

    elif operation == 3:
        while invalid_awnser:    
            fancy_print(f"\nKolik je {number1} krát {number2}? ")
            invalid_awnser, awnser = check_type(input(), "int")
        if awnser == number1 * number2:
            is_correct = True

    elif operation == 4:
        while invalid_awnser:    
            fancy_print(f"\nKolik je {number1} děleno {number2} (zaokrouhlujte na tři desetinná místa, použijte tečku jako desetinnou čárku)? ")
            invalid_awnser, awnser = check_type(input(), "float")       # some extra rounding
        if awnser == round(number1 / number2, 3):
            is_correct = True

    sleep(dialog_pace * 1)

    if is_correct:
        fancy_print("Správná odpověď!\n")
        sleep(dialog_pace * 1)
        return True
    else:
        fancy_print("Špatná odpověď!\n")
        sleep(dialog_pace * 1)
        return False

# combat
def combat(difficulty):
    def end_check():                                                    # checks if the battle is over
        if enemy_stats["hp"] <= 0:
            PlaySound("./data/music/main-theme.wav", SND_FILENAME | SND_LOOP | SND_ASYNC)
            say("battle_victory")
            return True
        elif player_stats["hp"] <= 0:
            say("dead")
            quit()
        else:
            return False
    
    enemy_stats = {                                                     # generates the enemy stats
        "hp": 3 * randint(1, difficulty + 1),
        "dmg": randint(1, difficulty + 1)
    }
    actions = 2
    enemy_actions = 2
    round = 1
    if difficulty < 3:                                                  # allows enemy healing only from a certain difficulty
        enemy_healing = 1
    else:
        enemy_healing = 2

    PlaySound("./data/music/battle-theme.wav", SND_FILENAME | SND_LOOP | SND_ASYNC)
    say("battle")

    while True:
        say("round", end=str(round) + "\n")

        fancy_print("Tvoje statistiky:")
        print_stats(player_stats)
        fancy_print("Nepřítelovy statistiky:")
        print_stats(enemy_stats)

        say("your_turn", False)
        say("actions", end=actions)

        for i in range(actions):
            inp = ask("battle_choose")
            if inp == "útok":
                if math_question(difficulty * round * randint(1, 2)):
                    dmg_dealt = player_stats["dmg"] * randint(1, 2)

                    say("attack_success", end=dmg_dealt)
                    enemy_stats["hp"] -= dmg_dealt
                else:
                    say("attack_failure")

            elif inp == "vyléčení":
                if inventory["heals"] == 0:
                    say("cant_heal")
                else:
                    amt_healed = randint(1, 3)

                    say("you_healed", end=amt_healed)
                    player_stats["hp"] += amt_healed
                    inventory["heals"] -= 1

            elif inp == "zmatení":
                if randint(1, difficulty + 1) < 3:
                    say("distraction_success")
                    enemy_actions -= 1
                else:
                    say("distraction_fail")
                    

            elif inp == "útěk":
                if randint(0, difficulty) == 0:
                    say("escape_success")
                else:
                    dmg_dealt = enemy_stats["dmg"] * randint(1, 2)
                    say("escape_fail", end=dmg_dealt)
                    player_stats["hp"] -= dmg_dealt
                
                end_check()
                return 0
            
            if end_check():
                return 2

        actions = 2

        say("enemy_turn", False)
        say("enemy_actions", end=enemy_actions)

        for i in range(enemy_actions):
            action = randint(1, enemy_healing)
            if action == 1:
                dmg_dealt = enemy_stats["dmg"] * randint(1, 2)
                if ask("block_enemy") == "ano":
                    actions -= 1
                    if not math_question(difficulty * round * randint(1, 2)):
                        say("block_fail", end=dmg_dealt)
                        player_stats["hp"] -= dmg_dealt
                    else:
                        say("block_success")
                else:
                    say("enemy_attack", end=dmg_dealt)
                    player_stats["hp"] -= dmg_dealt
            elif action == 2:
                amt_healed = randint(1, difficulty + 1)
                say("enemy_heal", end=amt_healed)
                enemy_stats["hp"] += amt_healed

            if end_check():
                return 2
        enemy_actions = 2
        round += 1

"""
return values for interactions():
0 - don't do anything
1 - delete the interaction from the map, but keep the item
2 - remove both the interaction and the item from the map
"""
# interaction
def interaction(name):  
    # mass collectables
    if name == "collect_coins":
        amt = randint(1, 3)
        say("coin", end=amt)   
        inventory["coins"] += amt
        return 2
    elif name == "collect_heal":
        say("heal")
        inventory["heals"] += 1
        return 2
    elif name == "collect_weapon":
        player_stats["dmg"] += 1
        say(weapons[player_stats["dmg"]])
        return 2

    elif name == "Vorin_first_meet":
        awnser = ask("Vorin_first_meet")
        if awnser == "ano":
            return 2

    elif name == "gate_key_collect":
        say("gate_key_collect")
        world_flags["gate_key_collected"] = True
        return 2
    elif name == "gatekeeper":
        if world_flags["gate_key_collected"]:
            say("gatekeeper_unlocked")
            world_flags["is_gate_open"] = True
        else:
            say("gatekeeper_locked")
    elif name == "gate":
        if world_flags["is_gate_open"]:
            say("gate_unlocked")
            return 1
        else:
            say("gate_locked")

    elif name == "wolf_first_fight":
        say("wolf_first_fight")
        result = combat(0)
        if result == 2:
            world_flags["village_wolf_killed"] = True
            return 2
    elif name == "villager_wolf_attack":
        if world_flags["village_wolf_killed"]:
            say("villager_thankful")
        else:
            say("villager_scared_of_wolf")
    return 0
