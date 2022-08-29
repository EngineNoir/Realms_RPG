import random
import time
import json
from functions.character_class_functions import Character
from functions.creature_class_functions import Creature

def combat_time(player: Character, enemy: Creature):

    while enemy.health > 0 and player.health > 0:

        # print some useful statistics
        print('\n' + enemy.name + "'s health: " + str(enemy.health))
        print('Your health: ' + str(player.health))
        print('Your mana: ' + str(player.mana))
        print("1. Attack with a Weapon\n2. Cast a Spell\n3. Use a Potion\n4. Attempt to Hide\n5. Attempt to Flee")
        while True:
            try:
                action_choice = int(input("\nWhat do you choose to do?: "))
            except ValueError:
                print('\nPlease input a valid action.')
            else:
                break

        # check if enemy spots the player
        enemy.spot_player(player)

        if action_choice == 1:

            # player strikes at the opponent
            player.deal_damage_to_enemy(enemy)

            # if the player is stealthed they get a free attack
            if enemy.health > 0 and not player.stealth:
                enemy.deal_damage_to_player(player)

            # the player is revealed from stealth after their attack
            if player.stealth:
                print('You are spotted again, and are no longer hidden or invisible.')
                player.stealth = False
     

        if action_choice == 2:
            # make code for spellcasting
            # return True if spell cast, and if True enemy deals damage
            return

        if action_choice == 3:
            # make code for potion consumption
            # if use_potion is true, enemy deals damage
            return

        if action_choice == 4:
            player.attempt_stealth_in_combat(enemy)

        if action_choice == 5:
            flight = player.fleeing_combat(enemy)
            if flight:
                break

    # decide if fight is over, and appropriately reward the player

    combat_succesful = False

    if player.health <= 0:
        print('\nYou have been defeated and faint!')
    if enemy.health <= 0:
        combat_succesful = True
        print('\nYou have defeated your foe and gained ' + str(enemy.xp) + ' XP.')
        if enemy.gold != 0:
            print('You loot ' + str(enemy.gold) + ' gold.')
            player.gold += enemy.gold
        player.current_xp += enemy.xp
    
    return combat_succesful
        


def player_combat_magic(char_sheet, creature, creature_health):
    import random

    attacked = False
    back_to_menu = False

    magic_ability = char_sheet[1][2][1]

    print("\nYou can cast the following spells:")
    i = 1
    for spell in char_sheet[11]:
        print(str(i) + '. ' + spell[0])
        i += 1
    print(str(i) + '. Return')

    spell_choice = None
    while spell_choice not in range(0, i):
        spell_choice = int(input("Which spell would you like to cast?: ")) - 1

    if char_sheet[12] == 0:
        print('\nYou fail to cast the spell, as you are out of mana.')

    if char_sheet[12] > 0:

        if spell_choice in range(0, i - 1) and char_sheet[11][spell_choice][1] != 0:
            player_damage_successes = 0
            char_sheet[12] -= char_sheet[11][spell_choice][3]

            if char_sheet[12] < 0:
                char_sheet[4] += char_sheet[12]
                print('\nYou lack sufficient mana to cast this spell and must use your blood instead.')
                print('You take ' + str(abs(char_sheet[12])) + ' points of damage.')
                char_sheet[12] = 0

            for i in range(1, char_sheet[11][spell_choice][1] + magic_ability):
                roll = random.randint(1, 6)
                if roll > 3:
                    player_damage_successes += 1
            damage_done = max((player_damage_successes - creature[3]), 0)
            creature_health -= damage_done
            print('\nYou ' + char_sheet[11][spell_choice][4] + " dealing " + str(damage_done)
                  + ' amount of damage to it.')
            attacked = True

        if spell_choice in range(0, i - 1) and char_sheet[11][spell_choice][1] == 0:
            char_sheet[12] -= char_sheet[11][spell_choice][3]

            if str(char_sheet[11][spell_choice][4]) == 'inv':
                char_sheet[10] = True
                print('\nYou become invisible, effectively entering stealth.')
            if str(char_sheet[11][spell_choice][4]) == 'rec':
                char_sheet[4] += magic_ability
                print('\nYou magically heal for ' + str(magic_ability) + ' points.')
                if char_sheet[4] > char_sheet[9]:
                    char_sheet[4] = char_sheet[9]
            if str(char_sheet[11][spell_choice][4]) == 'heal':
                char_sheet[4] += magic_ability
                print('\nYou pray and recover ' + str(magic_ability) + ' points of health.')
                if char_sheet[4] > char_sheet[9]:
                    char_sheet[4] = char_sheet[9]

    if spell_choice == i-1:
        back_to_menu = True

    return creature_health, attacked, back_to_menu

