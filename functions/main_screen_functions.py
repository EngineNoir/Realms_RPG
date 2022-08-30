from multiprocessing.sharedctypes import Value
import time
from functions.combat_function import combat_time
from functions.exploration_functions import explore
from functions.character_class_functions import load_character, make_character, save_character
from functions.character_inspection import inspect_sheet


# def ask_to_load(classes, armors, weapons):
#     # establish None type variables to overwrite with player choice, and player character
#     player_character = None
#     answer = None

#     print("1. New Character\n2. Load Character\n")
#     while answer not in [1, 2]:
#         while True:
#             try:
#                 answer = int(input('\nSelect one of the above: '))
#             except ValueError:
#                 print('\nPlease make a valid choice.')
#             else:
#                 break
#     if answer == 2:
#         player_character = load_character()
#     else:
#         print("\nAlright, time to make a new character!")
#         player_character = make_character(classes, armors, weapons)
#     
#     return player_character


def ask_to_load(classes, armors, weapons):
    # establish None type variables to overwrite with player choice, and player character
    player_character = None
    answer = None
    choices = ["1", "2"]

    print("1. New Character\n2. Load Character\n")
    while answer not in choices:
        while True:
            try:
                answer = input('\nSelect one of the above: ')
            except ValueError:
                print('Please input a valid choice.')
            else:
                break
    if answer == "2":
        player_character = load_character()
    else:
        print("\nAlright, time to make a new character!")
        player_character = make_character(classes, armors, weapons)
    
    return player_character


def request_action(player):
    while True:
        if player.health <= 0:
            print('You awake in the tavern, barely alive. Rest here to regain the rest of your vigour.')
            player.health = 1

        print('\nAvailable actions:\n1. Inspect Character Sheet\n2. Explore\n3. '
              'Visit the Tavern\n4. Buy Potions\n5. Save and Exit the Game')
        while True:
            try:
                action = int(input('\nWhat would you like to do?: '))
            except ValueError:
                print('\nPlease input a valid choice.')
            else:
                break

        if action == 1:
            inspect_sheet(player)
        elif action == 2:
            explore(player)
            pass
        elif action == 3:
            # rest_at_tavern(player) needs to be made
            pass
        elif action == 4:
            # shopping_for_potions(char_sheet) needs to be made/updated
            pass
        if action == 5:
            print('\nSaving and quitting the game.')
            save_character(player)
            time.sleep(3)
            break
