# Update

import os
import json
import time
from characters.create_character import load_character
from characters.create_character import make_character
from functions.char_creation import character_creation
from functions.menu_functions import inspect_sheet
from functions.exploration_functions import explore
from functions.potion_functions import shopping_for_potions

current_directory = os.getcwd()

load_creatures = open('jsons/creatures.json')
load_locations = open('jsons/locations.json')
load_spells = open('jsons/spells.json')
load_bosses = open('jsons/bosses.json')
load_consumables = open('jsons/consumables.json')
load_classes = open('jsons/classes.json')
load_armors = open('jsons/armors.json')
load_weapons = open('jsons/weapons.json')
    
armors = json.load(load_armors)
weapons = json.load(load_weapons)
character_classes = json.load(load_classes)
creatures = json.load(load_creatures)
locations = json.load(load_locations)
spells = json.load(load_spells)
bosses = json.load(load_bosses)
consumables = json.load(load_consumables)

# test the new function to create dictionary based character
# make_character(character_classes, armors, weapons)

# test loading a character
# player_character = load_character()
# print(player_character.name)


print('\n-----------------------------------')
print('--------A----A-A-A-A-A----A--------')
print('-------A-A----A-----A----A-A-------')
print('------A---A----A---A----A---A------')
print('-----A-----A----A-A----A-----A-----')
print('----A-A-A-A-A----A----A-A-A-A-A----')
print('-----------------------------------\n')


def ask_to_load():
    answer = None
    print("1. New Character\n2. Load Character\n")
    while answer not in [1, 2]:
        answer = int(input('Select one of the above: '))
    if answer == 2:
        char_name = input('\nWhat is your characters name?: ')
        load_char = open('characters/' + char_name + '.json')
        char_sheet = json.load(load_char)
    else:
        print("\nAlright, time to make a new character!")
        char_name = character_creation()
        load_char = open('characters/' + char_name + '.json')
        char_sheet = json.load(load_char)
    return char_sheet


character_sheet = ask_to_load()
print('\nWelcome, ' + character_sheet[0] + ' the ' + character_sheet[5] + '!')


def request_action(char_sheet):
    while True:
        print('\nAvailable actions:\n1. Inspect Character Sheet\n2. Explore\n3. '
              'Visit the Tavern\n4. Buy Potions\n5. Save and Exit the Game')
        action = int(input('\nWhat would you like to do?: '))
        if char_sheet[4] <= 0:
            print('You awake in the tavern, somewhat recovered from your injuries.')
            char_sheet[4] = 1
        if action == 1:
            inspect_sheet(char_sheet)
        if action == 2:
            explore(char_sheet, locations, creatures, bosses)
        if action == 3:
            if char_sheet[2] >= 5:
                char_sheet[2] -= 5
                char_sheet[4] = char_sheet[9]
                char_sheet[12] = char_sheet[13]
                print('\nYou rest at a tavern, regaining your vigour and calming your mind, at the cost of 5 gold.')
                print('You heal back to full health, and recover your mana.')
            else:
                print('You cannot afford to recover at the tavern, unfortunately.')
        if action == 4:
            shopping_for_potions(char_sheet)
        if action == 5:
            print('\nSaving and quitting the game.')
            time.sleep(3)
            break


request_action(character_sheet)

char_sheet_save = json.dumps(character_sheet, indent=1)
with open('characters/' + character_sheet[0] + '.json', 'w') as outfile:
    outfile.write(char_sheet_save)
