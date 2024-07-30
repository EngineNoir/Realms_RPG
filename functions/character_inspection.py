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
    print(f'\n{Fore.GREEN}--- CHARACTER SHEET ---{Fore.RESET}')
    print(f'Name: {Fore.RED}{player.name}{Fore.RESET}')
    print(f'Class: {Fore.YELLOW}{player.char_class}{Fore.RESET}')
    print(f'Level: {Fore.RED}{player.level}{Fore.RESET}')
    print(f'Current XP: {player.current_xp}')
    print(f'XP until next level: {player.xp_to_level}')

    print(f'\nHealth: {Fore.RED}{player.health}{Fore.RESET} (Max: {Fore.RED}{player.max_health}{Fore.RESET}).')
    print(f'Mana: {Fore.BLUE}{player.mana}{Fore.RESET} (Max: {Fore.BLUE}{player.max_mana}{Fore.RESET}).')
    print(f'Strength: {Fore.RED}{player.strength}{Fore.RESET}')
    print(f'Dexterity: {Fore.RED}{player.dexterity}{Fore.RESET}')
    print(f'Willpower: {Fore.RED}{player.willpower}{Fore.RESET}')

    print(f'\nGold: {player.gold}')
    print(f'Potions: {player.potions}')
    print(f'Abilities: ')
    list_abilities(player)
    print(f'{Fore.GREEN}--- CHARACTER SHEET ---{Fore.RESET}')

    # level option if there's enough XP
    choice = None
    print(f"\n1. Equipment\n2. Level Up\n3. {Fore.RED}Return{Fore.RESET}")
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
        print(f'- {Fore.RED}{abilities[ability]["name"]}{Fore.RESET}: {abilities[ability]["description"]} '
            f'(Cost: {Fore.BLUE}{abilities[ability]["cost"]}{Fore.RESET}, Dmg: {Fore.RED}{abilities[ability]["effect"]} + {abilities[ability]["attribute"]}{Fore.RESET})')
