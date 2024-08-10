import time

from colorama import Fore
from functions.exploration_functions import explore
from functions.character_class_functions import load_character, make_character, save_character
from functions.character_inspection import inspect_sheet
from functions.potion_class_functions import shopping_for_potions

def ask_to_load(classes, armors, weapons, amulets, rings):
    player = None
    answer = None
    while answer not in [1,2,3]:
        while True:
            try:
                print(f"\n1. New Character\n2. Load Character\n3. {Fore.RED}Exit{Fore.RESET}")
                answer = int(input(f'\n{Fore.YELLOW}What is your choice?: {Fore.RESET}'))
            except ValueError:
                print(f"\n{Fore.RED}Please select a valid option.{Fore.RESET}")
            else:
                break
        match answer:
            case 1:
                print("Time to make a new character!")
                time.sleep(1)
                player = make_character(classes, armors, weapons, amulets, rings)
            case 2:
                player = load_character()
            case 3:
                print(f"{Fore.RED}\n--- QUITTING GAME ---")
                print(f"\nQuitting the game.{Fore.RESET}\n")
                time.sleep(1)
                return -1
            case _:
                print(f"\n{Fore.RED}Please select a valid option.{Fore.RESET}")
    return player


def request_action(player, inventory):
    while True:
        if player.health <= 0:
            print('\n...')
            time.sleep(1)
            print(f'\n{Fore.RED}--- DEFEAT ---{Fore.RESET}')
            print(f'\nYou awake in the tavern, barely alive. {Fore.RED}Rest here{Fore.RESET} to regain the rest of your {Fore.RED}HP{Fore.RESET} and {Fore.BLUE}MP{Fore.RESET}.')
            player.health = 1

        print(f'\n{Fore.BLUE}--- VILLAGE ---{Fore.RESET}')
        print(f'\n1. Inspect Character Sheet\n2. Explore\n3. '
            f'Rest at the Tavern\n4. Buy Potions\n5. Save\n6. Save and {Fore.RED}Exit{Fore.RESET} the Game')
        while True:
            try:
                action = int(input(f'\n{Fore.YELLOW}What is your choice?: {Fore.RESET}'))
            except TypeError:
                print(f"\n{Fore.RED}Please select a valid option.{Fore.RESET}")
            else:
                break
        match action:
            case 1:
                inspect_sheet(player, inventory)
            case 2:
                explore(player, inventory)
            case 3:
                player.health = player.max_health
                player.mana = player.max_mana
                print(f'\n{Fore.GREEN}--- REST ---')
                print(f"\nYou rest at the tavern and regain all of your health and mana.{Fore.RESET}")
            case 4:
                shopping_for_potions(player)
            case 5:
                print(f"\n{Fore.GREEN}--- SAVING ---")
                save_character(player)
                print(f"\nDone!{Fore.RESET}")
            case 6:
                print(f"\n{Fore.GREEN}--- SAVING ---")
                save_character(player)
                print(f"\nDone!{Fore.RESET}")
                print(f"\n{Fore.RED}--- QUITTING THE GAME ---")
                print(f"\nQuitting the game.{Fore.RESET}\n")
                time.sleep(1)
                break
            case _:
                print(f"\n{Fore.RED}Please select a valid option.{Fore.RESET}")
                print(f'\n{Fore.BLUE}--- VILLAGE ---{Fore.RESET}')
                print('\n1. Inspect Character Sheet\n2. Explore\n3. '
                    'Rest at the Tavern\n4. Buy Potions\n5. Save and Exit the Game')
