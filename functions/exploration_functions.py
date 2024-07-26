import random
import time
import json

from functions.combat_function import combat_time
from functions.character_inspection import inspect_sheet
from functions.character_class_functions import Character
from functions.creature_class_functions import Creature
from functions.boss_class_functions import Boss
from functions.location_class_functions import Location

load_locations = open('jsons/locations.json')
locations = json.load(load_locations)


def explore(player: Character):
    print("\nYou may explore the following places:")
    for i in range(0, len(locations)):
        print(str(i+1) + '. ' + locations[i]['location_name'])
    print(str(len(locations)+1) + '. Return')

    player_choice = int(input("\nWhere do you wish to go?: ")) - 1
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
            location.explore(player)
        case _ if player_choice == len(locations):
            print('\nReturning to menu.')
            time.sleep(1)
            return 0
    # end stealth
    if player.stealth == True:
        player.stealth = False
        print('\nYou are no longer stealthed.')
