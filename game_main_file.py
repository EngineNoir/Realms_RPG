import json
import time
from functions.main_screen_functions import ask_to_load, request_action

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


print('\n-----------------------------------')
print('--------A----A-A-A-A-A----A--------')
print('-------A-A----A-----A----A-A-------')
print('------A---A----A---A----A---A------')
print('-----A-----A----A-A----A-----A-----')
print('----A-A-A-A-A----A----A-A-A-A-A----')
print('-----------------------------------\n')


player_character = ask_to_load(character_classes, armors, weapons)

print('\nWelcome, ' + player_character.name + ' the ' + player_character.char_class + '!')

request_action(player_character)
