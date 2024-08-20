import json
import pyfiglet
from colorama import Fore
from functions.inventory_class_functions import Inventory
from functions.main_screen_functions import ask_to_load, request_action

load_abilities = open('jsons/abilities.json')
load_consumables = open('jsons/consumables.json')
load_classes = open('jsons/classes.json')
load_armors = open('jsons/armors.json')
load_weapons = open('jsons/weapons.json')
load_amulets = open('jsons/amulets.json')
load_rings = open('jsons/rings.json')

armors = json.load(load_armors)
weapons = json.load(load_weapons)
character_classes = json.load(load_classes)
abilities = json.load(load_abilities)
consumables = json.load(load_consumables)
amulets = json.load(load_amulets)
rings = json.load(load_rings)

print(f"\n{Fore.BLUE}" + pyfiglet.figlet_format("REALMS", font='epic') + f"{Fore.RESET}")

player_character = ask_to_load(character_classes, armors, weapons, amulets, rings)
game_inventory = Inventory(armors, weapons, amulets, rings)

if player_character != 0:
    print(f'\nWelcome, {Fore.RED}{player_character.name}{Fore.RESET} the {Fore.YELLOW}{player_character.char_class}{Fore.RESET}!')
    request_action(player_character, game_inventory)
