import json
from functions.inventory_class_functions import Inventory
from functions.main_screen_functions import ask_to_load, request_action

load_spells = open('jsons/spells.json')
load_consumables = open('jsons/consumables.json')
load_classes = open('jsons/classes.json')
load_armors = open('jsons/armors.json')
load_weapons = open('jsons/weapons.json')
load_amulets = open('jsons/amulets.json')
load_rings = open('jsons/rings.json')

armors = json.load(load_armors)
weapons = json.load(load_weapons)
character_classes = json.load(load_classes)
spells = json.load(load_spells)
consumables = json.load(load_consumables)
amulets = json.load(load_amulets)
rings = json.load(load_rings)


print('\n-----------------------------------')
print('--------A----A-A-A-A-A----A--------')
print('-------A-A----A-----A----A-A-------')
print('------A---A----A---A----A---A------')
print('-----A-----A----A-A----A-----A-----')
print('----A-A-A-A-A----A----A-A-A-A-A----')
print('-----------------------------------\n')


player_character = ask_to_load(character_classes, armors, weapons, amulets, rings)
game_inventory = Inventory(armors, weapons, amulets, rings)

print('\nWelcome, ' + player_character.name + ' the ' + player_character.char_class + '!')

request_action(player_character, game_inventory)
