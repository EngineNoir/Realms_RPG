import random
import time
from functions.potion_functions import use_potions


def combat_time(char_sheet, creature):
    # player: 5 is health, 7 is armor, 8 is weapons
    # creature: 3 is armor, 4 is attack

    creature_health = random.randint(creature[1], creature[2])
    creature_health_max = creature_health
    combat_ability = max(char_sheet[1][0][1], char_sheet[1][1][1])

    spoken_once = False
    spoken_twice = False
    spoken_thrice = False

    while creature_health > 0 and char_sheet[4] > 0:

        # if boss fight
        if len(creature) == 12:
            if not spoken_once:
                print(creature[10][0])
                spoken_once = True
            if not spoken_twice and creature_health_max/4 < creature_health <= creature_health_max/2:
                print(creature[10][1])
                spoken_twice = True
            if not spoken_thrice and creature_health <= creature_health_max/4:
                print(creature[10][2])
                creature[4] = creature[11]
                spoken_thrice = True

        print('\n' + creature[0] + "'s health: " + str(creature_health))
        print('Your health: ' + str(char_sheet[4]))
        print('Your mana: ' + str(char_sheet[12]))
        print("1. Attack with a Weapon\n2. Cast a Spell\n3. Use a Potion\n4. Attempt to Hide\n5. Attempt to Flee")
        action_choice = int(input("What do you choose to do?: "))

        if action_choice == 1:
            creature_damage_successes = 0
            for i in range(1, creature[4] + 1):
                roll = random.randint(1, 6)
                if roll > 3:
                    creature_damage_successes += 1

            player_damage_successes = 0
            for i in range(1, combat_ability + 1):
                roll = random.randint(1, 6)
                if roll > 3:
                    player_damage_successes += 1
            player_damage_total = (player_damage_successes - creature[3])
            creature_health -= max(player_damage_total, 0)
            combat_action = random.choice(char_sheet[7][1])
            if player_damage_total > 0:
                print('\nYou ' + combat_action + ' with your ' + char_sheet[7][0] + ' dealing '
                    + str(player_damage_total) + ' damage to ' + creature[0] + '.')
            else:
                fails = ["Your attack misses.", "You fail to deal damage.", "The enemy dodges out of the way."]
                print('\n' + random.choice(fails))

            if char_sheet[10]:
                print('You are spotted again, and are no longer hidden or invisible.')

            if creature_health > 0:
                creature_deals_damage(char_sheet, creature)  # creature deals damage
            char_sheet[10] = False

        if action_choice == 2:
            creature_health, attacked, back_to_menu = player_combat_magic(char_sheet, creature, creature_health)
            if not back_to_menu:
                creature_deals_damage(char_sheet, creature)
            if attacked and char_sheet[10]:
                char_sheet[10] = False
                print('You are no longer hidden.')

        if action_choice == 3:
            if use_potions(char_sheet):
                creature_deals_damage(char_sheet, creature)

        if action_choice == 4:
            sneaking_function(char_sheet, creature)
            creature_deals_damage(char_sheet, creature)  # it deals damage

        if action_choice == 5:
            print('\nYou attempt to flee and...')
            time.sleep(1)
            if fleeing_combat(char_sheet, creature):
                print('You successfully get away!')
                is_combat_success = False
                break
            else:
                print('You fail to escape!')
                creature_deals_damage(char_sheet, creature)
    time.sleep(1)

    if char_sheet[4] <= 0:
        print('\nYou have been defeated and faint!')
        is_combat_success = False
    if creature_health <= 0:
        print('\nYou have defeated your foe and gained ' + str(creature[8]) + ' XP.')
        if creature[9] != 0:
            print('You loot ' + str(creature[9]) + ' gold.')
            char_sheet[2] += creature[9]
        char_sheet[14] += creature[8]
        is_combat_success = True

    return is_combat_success


def creature_deals_damage(char_sheet, creature):
    import random

    creature_damage_successes = 0

    for i in range(1, creature[4]):
        roll = random.randint(1, 6)
        if roll > 3:
            creature_damage_successes += 1

    if creature_damage_successes <= char_sheet[6][0] and not char_sheet[10]:
        misses = ["which fails to break through your defences.", "missing its attack.",
                  "failing to connect the attack.", "unable to land the attack.",
                  "but you dodge away in time.", "barely missing you."]
        print('\n' + creature[0] + ' ' + random.choice(creature[7]) + ' ' + random.choice(misses))

    if creature_damage_successes > char_sheet[6][0] and not char_sheet[10]:
        new_damage = (creature_damage_successes - char_sheet[6][0])
        char_sheet[4] -= max(new_damage, 0)
        print('\n' + creature[0] + ' ' + random.choice(creature[7]) + ' dealing ' + str(new_damage) + ' damage to you.')


def sneaking_function(char_sheet, creature):

    sneak_line = '\nYou attempt to sneak and ...'
    time.sleep(1)
    successful_sneaks = 0

    for i in range(1, char_sheet[1][1][1] + 1):
        dice_roll = random.randint(1, 6)
        if dice_roll > 3:
            successful_sneaks += 1

    if not char_sheet[10]:
        if successful_sneaks > creature[6]:
            sneak_line += 'You succeed!'
            char_sheet[10] = True
        else:
            sneak_line += 'You fail!'
        print(sneak_line)
    else:
        print('\nYou remain hidden.')


def fleeing_combat(char_sheet, creature):

    flee_ability = max(char_sheet[1][0][1], char_sheet[1][1][1])
    flee_value = 0

    for i in range(1, flee_ability + 1):
        roll = random.randint(1, 6)
        if roll > 3:
            flee_value += 1

    if flee_value >= creature[6]:
        flee_possible = True
    elif char_sheet[10]:
        flee_possible = True
    else:
        flee_possible = False

    return flee_possible


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

