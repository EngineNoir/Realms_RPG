import random
import time
import json

from colorama import Fore

from functions.combat_function import combat_time
from functions.character_inspection import inspect_sheet
from functions.character_class_functions import Character
from functions.creature_class_functions import Creature
from functions.boss_class_functions import Boss
from functions.location_class_functions import Location
from functions.inventory_class_functions import Inventory

load_locations = open('jsons/locations.json')
locations = json.load(load_locations)

def explore(player: Character, inventory: Inventory):
    print(f"\n{Fore.BLUE}--- EXPLORATION ---{Fore.RESET}")
    print("\nYou may explore the following places:")
    for i in range(0, len(locations)):
        print(f'{i+1}. {locations[i]["location_name"]}')
    print(f"{len(locations) + 1}. {Fore.RED}Return{Fore.RESET}")

    player_choice = int(input(f"\n{Fore.YELLOW}What is your choice?: {Fore.RESET}")) - 1
    match player_choice:
        case _ if 0 <= player_choice < len(locations):
            l = locations[player_choice]
            location = Location(l["location_name"],
                                l["min_rooms"],
                                l["max_rooms"],
                                l["entry_description"],
                                l["room_descriptions"],
                                l["encounter_descriptions"],
                                l["final_room_description"],
                                l["boss_death"],
                                l["final_room_return"])
            location.explore(player, inventory)
        case _ if player_choice == len(locations):
            print(f'\n{Fore.RED}Returning to menu.{Fore.RESET}')
            time.sleep(1)
            return 0
    # end stealth
    if player.stealth == True:
        player.stealth = False
        print(f"\n{Fore.RED}--- STEALTH CANCELLED ---")
        print(f'\nYou are no longer stealthed.{Fore.RESET}')
