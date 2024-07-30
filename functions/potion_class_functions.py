import json

from colorama import Fore

from functions.character_class_functions import Character

load_consumables = open('jsons/consumables.json')
consumables = json.load(load_consumables)

class Potion():
    def __init__(self,
                 name: str,
                 stat: str,
                 rec: int,
                 val: int
                 ):
                self.name = name
                self.stat = stat
                self.rec = rec
                self.val = val

def __str__(self):
    return self.name

def generate_potions(consumables):
    potions = []
    for potion in consumables:
        pot = Potion(potion["potion_name"], potion["stat"], potion["recover"], potion["value"])
        potions.append(pot)
    return potions

def shopping_for_potions(player: Character):
    print(f"{Fore.BLUE}--- POTION STORE ---{Fore.RESET}")
    potions = generate_potions(consumables)
    player_choice = None
    while True:
        print(f'\n1. Lesser Health Potion (10g)'
              f'\n2. Health Potion (50g)\n3. Greater Health Potion (200g)\n4. Lesser Mana Potion (10g)\n5. Mana Potion (50g)'
              f'\n6. Greater Mana Potion (200g)\n7. {Fore.RED}Return{Fore.RESET}')
        print(f"\nYou have {player.gold} gold.")
        while True:
            try:
                player_choice = int(input(f"\n{Fore.YELLOW}What is your choice?: {Fore.RESET}"))
            except ValueError:
                print(f"\n{Fore.RED}Please select a valid option.{Fore.RESET}")
            else:
                break
        if player_choice == 7:
            print(f"\n{Fore.RED}You leave the potions store.{Fore.RESET}")
            return 0
        pot = potions[player_choice - 1]
        if player.gold < pot.val:
            print(f"\n{Fore.RED}Unfortunately, you cannot afford this item right now.{Fore.RESET}")
        elif pot.name in player.potions:
            print(f"\n{Fore.RED}You already have this item, and cannot carry more.{Fore.RESET}")
        else:
            print(f"\n{Fore.GREEN}--- PURCHASE SUCCESS ---")
            print(f"\n{Fore.RED if "Health" in pot.name else Fore.BLUE}{pot.name}{Fore.GREEN} has been added to your inventory.{Fore.RESET}")
            player.potions.append(pot.name)
            player.gold -= pot.val
    return 0


def use_potions(player: Character):
    potions = generate_potions(consumables)
    did_drink = False
    i = 1
    # prints all the potions
    print(f"\n{Fore.GREEN}--- POTIONS ---{Fore.RESET}")
    for potion in player.potions:
        print(f"{i}. {Fore.RED if "Health" in potion else Fore.BLUE}{potion}{Fore.RESET}")
        i += 1
    print(f'{i}. {Fore.RED}Return{Fore.RESET}')
    #
    player_choice = None
    while player_choice not in range(0, len(player.potions) + 1):
        player_choice = int(input(f"\n{Fore.YELLOW}What is your choice?: {Fore.RESET}")) - 1
        if player_choice == len(player.potions):
            return did_drink
        else:
            pot = None
            for potion in potions:
               if potion.name == player.potions[player_choice]:
                   pot = potion
            if pot.stat == 'health':
                player.health = min(player.health + pot.rec, player.max_health)
                print(f"\n{Fore.RED}--- HEALTH RESTORED ---{Fore.RESET}")
                print(f"\nYou consume the {Fore.RED}{pot.name}{Fore.RESET} bringing your health up to {Fore.RED}{player.health}{Fore.RESET}.")
            else:
                player.mana = min(player.mana + pot.rec, player.max_mana)
                print(f"\n{Fore.BLUE}--- MANA RECOVERED ---{Fore.RESET}")
                print(f"\nYou consume the {Fore.BLUE}{pot.name}{Fore.RESET} bringing your mana up to {Fore.BLUE}{player.mana}{Fore.RESET}.")
            player.potions.remove(pot.name)
            did_drink = True
    return did_drink
