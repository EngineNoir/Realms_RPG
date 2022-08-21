import math
import random


def inspect_sheet(char_sheet):
    print('\n-----------------')
    print('Name: ' + char_sheet[0])
    print('Class: ' + str(char_sheet[5]))
    print('Level: ' + str(char_sheet[16]))
    print('Current XP: ' + str(char_sheet[14]))
    print('XP until next level: ' + str(char_sheet[15]))
    print('\nHealth: ' + str(char_sheet[4]) + ' (Max: ' + str(char_sheet[9]) + ').')
    print('Mana: ' + str(char_sheet[12]) + ' (Max: ' + str(char_sheet[13]) + ').')
    for attribute in char_sheet[1]:
        print(attribute[0] + ': ' + str(attribute[1]))
    print('\nWeapon: ' + char_sheet[7][0] + '\nArmor: ' + char_sheet[6][1] + ' (Armor: ' + str(char_sheet[6][0]) + ').')
    print('Gold: ' + str(char_sheet[2]))
    print('Inventory: ' + str(char_sheet[3]))
    print('Spells: ')
    for spell in char_sheet[11]:
        print(' - ' + spell[0] + ': ' + spell[2])
        bottom_text = '    Cost: ' + str(spell[3]) + ' mana'
        if spell[1] != 0:
            bottom_text += ', Damage: 1-' + str(spell[1]) + '.'
        print(bottom_text)
    print('-----------------')
    if char_sheet[14] >= char_sheet[15]:
        ask_to_level = int(input('\nYou have enough XP to level up. Do you wish to do that?\n'
                                 '1. Yes\n2. No\nChoice: '))
        if ask_to_level == 1:
            level_up(char_sheet)


def level_up(char_sheet):
    current_xp = char_sheet[14]
    xp_to_level = char_sheet[15]

    print('\nYou have ' + str(current_xp) + ' XP. Do you wish to spend ' + str(xp_to_level) + ' XP to level up?')
    answer_input = None
    while answer_input not in [1, 2]:
        answer_input = int(input('1. Yes\n2. No\nSpend XP and level up?: '))
        if answer_input == 1:
            answer_input_2 = None
            while answer_input_2 not in [1, 2, 3]:
                answer_input_2 = int(input('\nChoose which of the three attributes you wish to increase by 1.'
                                           '\n1. Strength\n2. Dexterity\n3. Willpower\nAttribute to improve: '))
                print(answer_input_2)
                answer_input_3 = None
                while answer_input_3 not in [1, 2, 3]:
                    if answer_input_2 == 1:
                        print('\nStrength + 1')
                    elif answer_input_2 == 2:
                        print('\nDexterity + 1')
                    elif answer_input_2 == 3:
                        print('\nWillpower + 1')
                    answer_input_3 = int(input('Are you sure you wish to increase this attribute?\n1. '
                                               'Yes\n2. No\nConfirm changes?: '))
                    if answer_input_3 == 1:
                        health_increase = 3 + random.randint(1, 5)
                        mana_increase = random.randint(1, 5) + math.floor(char_sheet[1][2][1]/2)

                        char_sheet[16] += 1                # increase level
                        char_sheet[9] += health_increase   # increase health
                        char_sheet[13] += mana_increase    # increase mana
                        if answer_input_2 == 1:
                            char_sheet[1][0][1] += 1
                        elif answer_input_2 == 2:
                            char_sheet[1][1][1] += 1
                        elif answer_input_2 == 3:
                            char_sheet[1][2][1] += 1

                        char_sheet[14] -= char_sheet[15]
                        char_sheet[15] *= 2
                        print('\nYou have successfully leveled up and are now level ' + str(char_sheet[16]) +
                              '. Congratulations!')
                        print('Health + ' + str(health_increase) + ', Mana + ' + str(mana_increase) + '.')
