import random
import time
import json

from functions.combat_function import combat_time
from functions.character_inspection import inspect_sheet
from functions.character_class_functions import Character
from functions.creature_class_functions import Creature
from functions.boss_class_functions import Boss

load_locations = open('jsons/locations.json')
locations = json.load(load_locations)

load_creatures = open('jsons/creatures.json')
creatures = json.load(load_creatures)

load_bosses = open('jsons/bosses.json')
bosses = json.load(load_bosses)


def explore(player: Character):
    print("\nYou may explore the following places:")
    for i in range(0, len(locations)):
        print(str(i+1) + '. ' + locations[i]['location_name'])
    print(str(len(locations)+1) + '. Return')
    
    player_choice = None
    while player_choice not in range(0, len(locations)+1):
        while True:
            try:
                player_choice = int(input("Where do you wish to go?: ")) - 1
            except ValueError:
                print('Please input a valid choice.')
            else:
                break
        if player_choice in range(0, len(locations)):
            location_exploration(player, locations[player_choice]['location_name'])
        if player_choice == len(locations):
            print('\nReturning to menu.')
            time.sleep(1)
            break
    
    # end stealth
    if player.stealth == True:
        player.stealth = False
        print('\nYou are no longer stealthed.')

def location_exploration(player: Character, location_name):
    location = [exp_location for exp_location in locations if exp_location['location_name'] == location_name][0]

    print(location['entry_description'])
    # dungeon length and movement
    location_length = random.randint(location['min_rooms'], location['max_rooms'])
    exploration_counter = 0

    while exploration_counter < location_length and player.health > 0:
        action = exploration_player_actions(player, location)
        if action == 1:
            print(random.choice(location['room_descriptions']))
            exploration_counter += 1
        elif action == 6:
            break

    if exploration_counter == location_length:
        print(location['final_room_description'])

        # make this neater
        chosen_boss = [boss for boss in bosses if boss['location'] == location['location_name']]
        picked_enemy = chosen_boss[0]
        enemy = Boss(picked_enemy['name'], picked_enemy['moveset'], picked_enemy['health'], picked_enemy['health'],
                        picked_enemy['damage_min'], picked_enemy['damage_max'], picked_enemy['damage_final'], picked_enemy['armor'], 
                        picked_enemy['loot'], picked_enemy['location'], picked_enemy['gold'], picked_enemy['xp'], picked_enemy['awareness'], 
                        picked_enemy['speed'], picked_enemy['taunts'])

        if location['location_name'] not in player.cleared_dungeons:
            print(enemy.taunts[0])
            combat_result = combat_time(player, enemy)
            if combat_result:
                print(location['boss_death'])
                player.cleared_dungeons.append(location['location_name'])
                print('\nYou return to Hubberton City.')
        else:
            print(location['final_room_return'])


def exploration_player_actions(player: Character, location):

    player_choice = None

    if player.health > 0:
        print('\nYou may do the following:\n1. Continue Exploring.\n2. Stealth.\n3. Use Magic.\n4. Use a potion'
              '\n5. Inspect Character Sheet\n6. Leave the Location.')

    while player_choice not in range(1,6) and player.health > 0:
        while True:
            try:
                player_choice = int(input('What would you like to do?: '))
            except ValueError:
                print('Please input a valid choice.')
            else:
                break

        if player_choice == 1:
            print('\nYou explore further in this location...')

            # check if fight or encounter
            if_fight = random.randint(1, 100)

            if if_fight > 50:

                # generate an enemy based on area
                picked_enemy = random.choice([creature for creature in creatures if creature['location'] == location['location_name']])
                enemy = Creature(picked_enemy['name'], picked_enemy['moveset'], picked_enemy['health'], picked_enemy['damage_min'], 
                        picked_enemy['damage_max'], picked_enemy['armor'], picked_enemy['loot'], picked_enemy['location'],
                        picked_enemy['gold'], picked_enemy['xp'], picked_enemy['awareness'], picked_enemy['speed'])

                print("\nYou encounter " + enemy.name + "!")

                # maybe add additional condition if player is invisible... or remove invisibility
                if player.stealth and player.dexterity > enemy.awareness:
                    print(
                        '\nYou remain hidden, and may ambush ' + enemy.name + '.\n1. Ambush.\n2. Stealth past.')
                    player_choice = None
                    while player_choice not in [1, 2]:
                        while True:
                            try:
                                player_choice = int(input("What do you do?: "))
                            except ValueError:
                                print('Please input a valid response.')
                            else:
                                break

                        if player_choice == 1:
                            print('\nYou ambush your foe!')
                            combat_time(player, enemy)
                        if player_choice == 2:
                            print('\nYou sneak past ' + enemy.name + '.')
                elif player.stealth and player.dexterity <= enemy.awareness:
                    print('You are spotted and ready yourself for a fight!')
                    player.stealth = False
                    combat_time(player, enemy)
                elif not player.stealth:
                    print('You prepare for a fight!')
                    combat_time(player, enemy)
            else:
                print(random.choice(location['encounter_descriptions']))

        if player_choice == 2:
            player.stealth_in_exploration()
        if player_choice == 3:
            # add something for magic exploration_magic(char_sheet)
            break
        if player_choice == 4:
            # add a use item thing use_potions(char_sheet)
            break
        if player_choice == 5:
            inspect_sheet(player)
        if player_choice == 6:
            print('\nYou choose to leave this location, perhaps to return another time.')
        
        return player_choice

