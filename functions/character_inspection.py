# inspect sheet new
from functions.inventory_class_functions import Inventory
import json

load_armors = open('jsons/armors.json')
load_weapons = open('jsons/weapons.json')
load_amulets = open('jsons/amulets.json')
load_rings = open('jsons/rings.json')
load_abilities = open('jsons/abilities.json')

armors = json.load(load_armors)
weapons = json.load(load_weapons)
amulets = json.load(load_amulets)
rings = json.load(load_rings)
abilities = json.load(load_abilities)

def inspect_sheet(player, inventory):
    print('\n-----------------')
    print('Name: ' + player.name)
    print('Class: ' + player.char_class)
    print('Level: ' + str(player.level))
    print('Current XP: ' + str(player.current_xp))
    print('XP until next level: ' + str(player.xp_to_level))

    print('\nHealth: ' + str(player.health) + ' (Max: ' + str(player.max_health) + ').')
    print('Mana: ' + str(player.mana) + ' (Max: ' + str(player.max_mana) + ').')
    print('Strength: ' + str(player.strength))
    print('Dexterity: ' + str(player.dexterity))
    print('Willpower: ' + str(player.willpower))

    print('\nGold: ' + str(player.gold))
    print('Potions: ' + str(player.potions))
    print('Abilities: ')
    list_abilities(player)
    print('-----------------')

    # level option if there's enough XP
    choice = None
    print("1. Equipment\n2. Level Up\n3. Return")
    while choice == None or choice not in list(range(1,4)):
        while True:
            try:
                choice = int(input("\nWhat is your choice?: "))
            except ValueError:
                print("\nPlease select a valid input")
            else:
                break
        match choice:
            case 1:
                inventory.equipment_functions(player)
                return 0
            case 2:
                if player.current_xp >= player.xp_to_level:
                    player.level_up()
                    return 0
                else:
                    print("\nYou do not have enough XP to level.")
            case 3:
                return 0


def list_abilities(player):
    for ability in player.abilities:
        print(f"- {abilities[ability]["name"]}: {abilities[ability]["description"]} "
            f"(Cost: {abilities[ability]["cost"]}, Dmg: {abilities[ability]["effect"]} + {abilities[ability]["attribute"]})")
