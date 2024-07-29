# inspect sheet new
import json

from colorama import Fore
from functions.inventory_class_functions import Inventory

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
    print(f'\n{Fore.GREEN}--- CHARACTER SHEET ---')
    print(f'Name: {player.name}')
    print(f'Class: {player.char_class}')
    print(f'Level: {player.level}')
    print(f'Current XP: {player.current_xp}')
    print(f'XP until next level: {player.xp_to_level}')

    print(f'\nHealth: {player.health} (Max: {player.max_health} ).')
    print(f'Mana: {player.mana} (Max: {player.max_mana}).')
    print(f'Strength: {player.strength}')
    print(f'Dexterity: {player.dexterity}')
    print(f'Willpower: {player.willpower}')

    print(f'\nGold: {player.gold}')
    print(f'Potions: {player.potions}')
    print(f'Abilities: ')
    list_abilities(player)
    print(f'{Fore.GREEN}--- CHARACTER SHEET ---{Fore.RESET}')

    # level option if there's enough XP
    choice = None
    print(f"\n{Fore.GREEN}1. Equipment\n2. Level Up\n3. {Fore.RED}Return{Fore.RESET}")
    while choice == None or choice not in list(range(1,4)):
        while True:
            try:
                choice = int(input(f"\n{Fore.YELLOW}What is your choice?: {Fore.RESET}"))
            except ValueError:
                print(f"\n{Fore.RED}Please select a valid option.{Fore.RESET}")
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
                    print(f"{Fore.RED}\n--- LEVEL UP CANCELLED ---")
                    print(f"\nYou do not have enough XP to level.{Fore.RESET}")
            case 3:
                return 0


def list_abilities(player):
    for ability in player.abilities:
        print(f"- {Fore.YELLOW}{abilities[ability]["name"]}{Fore.BLUE}: {abilities[ability]["description"]} "
            f"{Fore.GREEN}(Cost: {abilities[ability]["cost"]}, Dmg: {abilities[ability]["effect"]} + {abilities[ability]["attribute"]}){Fore.RESET}")
