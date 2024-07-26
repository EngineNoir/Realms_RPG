import random
import time
import json
from functions.character_class_functions import Character
from functions.creature_class_functions import Creature

def combat_time(player: Character, enemy: Creature):

    while enemy.health > 0 and player.health > 0:

        # print some useful statistics
        print('\n' + enemy.name + " health: " + str(enemy.health))
        print('Your health: ' + str(player.health))
        print('Your mana: ' + str(player.mana))
        print("1. Attack with a Weapon\n2. Cast a Spell\n3. Use a Potion\n4. Attempt to Hide\n5. Attempt to Flee")
        # check if enemy spots the player
        enemy.spot_player(player)
        # prompt player action
        action_choice = int(input("\nWhat do you choose to do?: "))
        match action_choice:
            case 1:
                # player strikes at the opponent
                player.deal_damage_to_enemy(enemy)
                # if the player is stealthed they get a free attack
                if enemy.health > 0 and not player.stealth:
                    enemy.deal_damage_to_player(player)                    # the player is revealed from stealth after their attack
                if player.stealth:
                    print('You are spotted again, and are no longer hidden or invisible.')
                    player.stealth = False
            case 2:
                # TODO code for spellcasting
                # return True if spell cast, and if True enemy deals damage
                return 0
            case 3:
                # TODO code for potion consumption
                # if use_potion is true, enemy deals damage
                return 0
            case 4:
                player.attempt_stealth_in_combat(enemy)
            case 5:
                flight = player.fleeing_combat(enemy)
                if flight:
                    break
            case _:
                print('\nPlease select a valid action.')
                action_choice = int(input("\nWhat do you choose to do?: "))

    # decide if fight is over, and appropriately reward the player
    combat_succesful = False

    if player.health <= 0:
        print('\nYou have been defeated and faint!')
    elif enemy.health <= 0:
        combat_succesful = True
        print('\nYou have defeated your foe and gained ' + str(enemy.xp) + ' XP.')
        if enemy.gold != 0:
            print('You loot ' + str(enemy.gold) + ' gold.')
            player.gold += enemy.gold
        player.current_xp += enemy.xp

    return combat_succesful



def player_combat_magic(player: Character, enemy: Creature):
    # TODO
    return 0
