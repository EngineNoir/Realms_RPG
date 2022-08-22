import time

from functions.create_character import load_character, make_character, save_character
from functions.character_inspection import inspect_sheet

def ask_to_load(classes, armors, weapons):
    # establish None type variables to overwrite with player choice, and player character
    player_character = None
    answer = None

    print("1. New Character\n2. Load Character\n")
    while answer not in [1, 2]:
        answer = int(input('Select one of the above: '))
    if answer == 2:
        player_character = load_character()
    else:
        print("\nAlright, time to make a new character!")
        player_character = make_character(classes, armors, weapons)
    
    return player_character


def request_action(player):
    while True:
        print('\nAvailable actions:\n1. Inspect Character Sheet\n2. Explore\n3. '
              'Visit the Tavern\n4. Buy Potions\n5. Save and Exit the Game')
        action = int(input('\nWhat would you like to do?: '))
        if player.health <= 0:
            print('You awake in the tavern, somewhat recovered from your injuries.')
            player.health = 1
        elif action == 1:
            inspect_sheet(player)
        elif action == 2:
            # explore(char_sheet, locations, creatures, bosses)
            player.gain_xp(50)
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
