import random
import time



def explore(char_sheet, locations, creatures, bosses):
    print("\nYou may explore the following places:")
    for i in range(0, len(locations)):
        print(str(i+1) + '. ' + locations[i][0])
    print(str(len(locations)+1) + '. Return')
    player_choice = None
    while player_choice not in range(0, len(locations)+1):
        player_choice = int(input("Where do you wish to go?: "))-1
        if player_choice in range(0, len(locations)):
            location_exploration(char_sheet, locations[player_choice], creatures, bosses[player_choice])
        if player_choice == len(locations):
            print('\nReturning to menu.')
            time.sleep(1)
            break
    char_sheet[10] = False


def location_exploration(char_sheet, location, creatures, boss):
    print(location[6][0])

    # dungeon length and movement
    location_length = random.randint(location[2], location[3])
    exploration_counter = 0

    while exploration_counter < location_length and char_sheet[4] > 0:
        action = exploration_player_actions(char_sheet, location, creatures)
        if action == 1:
            print(random.choice(location[4]))
            exploration_counter += 1
        elif action == 6:
            break

    if exploration_counter == location_length:
        print(location[5][0])
        if location[1] not in char_sheet[17]:
            if combat_time(char_sheet, boss):
                print(location[8][0])
                char_sheet[17].append(location[1])
                print('\nYou return to Hubberton City.')
        else:
            print(location[8][1])


def exploration_player_actions(char_sheet, location, creatures):
    # populate dungeon
    location_creatures = []
    for creature in creatures:
        if creature[5] == location[1]:
            location_creatures.append(creature)

    player_choice = None

    if char_sheet[4] > 0:
        print('\nYou may do the following:\n1. Continue Exploring.\n2. Stealth.\n3. Use Magic.\n4. Use a potion'
              '\n5. Inspect Character Sheet\n6. Leave the Location.')

    while player_choice not in [1, 2, 3, 4, 5, 6] and char_sheet[4] > 0:
        player_choice = int(input('What would you like to do?: '))
        if player_choice == 1:
            print('\nYou explore further in this location...')

            if_fight = random.randint(1, 100)
            if if_fight > 50:
                spawn_creature = random.choice(location_creatures)
                print("\nYou encounter " + spawn_creature[0] + "!")
                if char_sheet[10] and max(char_sheet[1][1][1], char_sheet[1][2][1]) > spawn_creature[6]:
                    print(
                        '\nYou remain hidden, and may ambush ' + spawn_creature[0] + '.\n1. Ambush.\n2. Stealth past.')
                    player_choice = None
                    while player_choice not in [1, 2]:
                        player_choice = int(input("What do you do?: "))
                        if player_choice == 1:
                            print('\nYou ambush your foe!')
                            combat_time(char_sheet, spawn_creature)
                        if player_choice == 2:
                            print('\nYou sneak past ' + spawn_creature[0] + '.')
                elif char_sheet[10] and max(char_sheet[1][1][1], char_sheet[1][2][1]) <= spawn_creature[6]:
                    print('You are spotted and ready yourself for a fight!')
                    char_sheet[10] = False
                    combat_time(char_sheet, spawn_creature)
                elif not char_sheet[10]:
                    print('You prepare for a fight!')
                    combat_time(char_sheet, spawn_creature)
            else:
                print(random.choice(location[7]))

        if player_choice == 2:
            if char_sheet[10]:
                print('\nYou remain hidden.')
            elif not char_sheet[10] and (char_sheet[5] != 'Mage' or char_sheet[1][1][1] >= 4):
                char_sheet[10] = True
                print('\nYou are mindful to remain hidden and continue in stealth.')
            elif not char_sheet[10] and char_sheet[5] == 'Mage':
                print('\nYou struggle to be unseen, but know that you can achieve invisibility through magic.')
                if char_sheet[12] >= char_sheet[11][0][3]:
                    char_sheet[12] -= char_sheet[11][0][3]
                    print('You become invisible, effectively entering stealth.')
                    char_sheet[10] = True
                elif char_sheet[12] < char_sheet[11][0][3]:
                    print('It seems however that you lack the mana to do so.')
            break
        if player_choice == 3:
            exploration_magic(char_sheet)
            break
        if player_choice == 4:
            use_potions(char_sheet)
            break
        if player_choice == 5:
            inspect_sheet(char_sheet)
        if player_choice == 6:
            print('\nYou choose to leave this location, perhaps to return another time.')

    return player_choice


def exploration_magic(char_sheet):
    magic_ability = char_sheet[1][2][1]

    print("\nYou can cast the following spells:")
    for i in range(0, len(char_sheet[11])):
        print(str(i + 1) + '. ' + char_sheet[11][i][0])
    print(str(len(char_sheet[11]) + 1) + '. Return')
    spell_choice = None
    while spell_choice not in range(0, len(char_sheet[11]) + 1):
        spell_choice = int(input("Which spell would you like to cast?: ")) - 1
        if spell_choice == len(char_sheet[11]):
            break
        if char_sheet[11][spell_choice][1] != 0:
            print('\nYou cannot cast combat spells outside of combat.')
            break
        if spell_choice in range(0, len(char_sheet[11])):
            if char_sheet[12] == 0:
                print('\nYou fail to cast the spell, as you are out of mana.')

            if char_sheet[12] > 0:

                if spell_choice in range(0, len(char_sheet[11])):

                    if str(char_sheet[11][spell_choice][4]) == 'inv':
                        if not char_sheet[10]:
                            char_sheet[10] = True
                            print('\nYou become invisible, effectively entering stealth.')
                        elif char_sheet[10]:
                            print('\nYou are already invisible, and thus require no further expense to remain so.')
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

            char_sheet[12] -= char_sheet[11][spell_choice][3]

            if char_sheet[12] < 0:
                char_sheet[4] += char_sheet[12]
                print('\nYou lack sufficient mana to cast this spell and must use your blood instead.')
                print('You take ' + str(abs(char_sheet[12])) + ' points of damage.')
                char_sheet[12] = 0
