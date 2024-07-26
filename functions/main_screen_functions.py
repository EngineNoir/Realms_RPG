from multiprocessing.sharedctypes import Value
import time
from functions.exploration_functions import explore
from functions.character_class_functions import load_character, make_character, save_character
from functions.character_inspection import inspect_sheet

def ask_to_load(classes, armors, weapons):
    player = None
    print("1. New Character\n2. Load Character\n")
    answer = int(input('\nSelect one of the above: '))
    match answer:
        case 1:
            print("\nAlright, time to make a new character!")
            player = make_character(classes, armors, weapons)
        case 2:
            player = load_character()
        case _:
            print("\nPlease select a valid action")
            print("\n1. New Character\n2. Load Character\n")
            answer = input('\nSelect one of the above: ')
    return player


def request_action(player):
    while True:
        if player.health <= 0:
            print('You awake in the tavern, barely alive. Rest here to regain the rest of your vigour.')
            player.health = 1

        print('\nAvailable actions:\n1. Inspect Character Sheet\n2. Explore\n3. '
              'Rest at the Tavern\n4. Buy Potions\n5. Save and Exit the Game')
        action = int(input('\nWhat would you like to do?: '))
        match action:
            case 1:
                inspect_sheet(player)
            case 2:
                explore(player)
            case 3:
                player.health = player.max_health
                print("\nYou rest at the tavern and regain all of your health.")
            case 4:
                # shopping_for_potions(char_sheet) needs to be made/updated
                print("TODO")
                pass
            case 5:
                print('\nSaving and quitting the game.')
                save_character(player)
                time.sleep(3)
                break
            case _:
                print("\nPlease select a valid action.")
                print('\nAvailable actions:\n1. Inspect Character Sheet\n2. Explore\n3. '
                    'Rest at the Tavern\n4. Buy Potions\n5. Save and Exit the Game')
                action = int(input('\nWhat would you like to do?: '))
