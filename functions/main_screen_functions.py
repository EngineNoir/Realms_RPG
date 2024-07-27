from multiprocessing.sharedctypes import Value
import time
from functions.exploration_functions import explore
from functions.character_class_functions import load_character, make_character, save_character
from functions.character_inspection import inspect_sheet
from functions.potion_class_functions import shopping_for_potions

def ask_to_load(classes, armors, weapons, amulets, rings):
    player = None
    while player == None:
        while True:
            try:
                print("\n1. New Character\n2. Load Character\n")
                answer = int(input('\nSelect one of the above: '))
            except TypeError:
                print("\nYou must select a number!")
            else:
                break
        match answer:
            case 1:
                print("\nAlright, time to make a new character!")
                player = make_character(classes, armors, weapons, amulets, rings)
            case 2:
                player = load_character()
            case _:
                print("\nPlease select a valid action")
                print("\n1. New Character\n2. Load Character\n")
    return player


def request_action(player):
    while True:
        if player.health <= 0:
            print('\nYou awake in the tavern, barely alive. Rest here to regain the rest of your vigour.')
            player.health = 1

        print('\nAvailable actions:\n1. Inspect Character Sheet\n2. Explore\n3. '
              'Rest at the Tavern\n4. Buy Potions\n5. Save\n6. Save and Exit the Game')
        while True:
            try:
                action = int(input('\nWhat would you like to do?: '))
            except TypeError:
                print("\nPlease select a valid action!")
            else:
                break
        match action:
            case 1:
                inspect_sheet(player)
            case 2:
                explore(player)
            case 3:
                player.health = player.max_health
                player.mana = player.max_mana
                print("\nYou rest at the tavern and regain all of your health and mana.")
            case 4:
                shopping_for_potions(player)
            case 5:
                print('\nSaving...')
                save_character(player)
                time.sleep(3)
                print("\nDone!")
                time.sleep(1)
            case 6:
                print("\nSaving...")
                save_character(player)
                time.sleep(3)
                print("\nDone!")
                time.sleep(1)
                print("\nQuitting the game.")
                time.sleep(2)
                break
            case _:
                print("\nPlease select a valid action.")
                print('\nAvailable actions:\n1. Inspect Character Sheet\n2. Explore\n3. '
                    'Rest at the Tavern\n4. Buy Potions\n5. Save and Exit the Game')
