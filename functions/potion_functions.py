import json

load_consumables = open('jsons/consumables.json')
consumables = json.load(load_consumables)


def shopping_for_potions(char_sheet):

    print('\nYou enter a potion store, and see the following selection:\n1. Lesser Health Potion (10g)'
          '\n2. Health Potion (50g)\n3. Greater Health Potion (200g)\n4. Lesser Mana Potion (10g)\n5. Mana Potion (50g)'
          '\n6. Greater Mana Potion (200g)\n7. Return')
    player_choice = None
    while player_choice not in [0, 1, 2, 3, 4, 5, 6]:
        player_choice = int(input("\nYour gold: " + str(char_sheet[2]) + "\nWhat would you like to buy?: ")) - 1
        if player_choice == 6:
            break
        if len(char_sheet[3]) == 5:
            print('\nYour inventory is full.')
        if char_sheet[2] < consumables[player_choice][2]:
            print('\nYou lack the gold to purchase this potion.')
        if char_sheet[2] >= consumables[player_choice][2] and len(char_sheet[3]) < 5:
            print('\n' + consumables[player_choice][0] + ' is added to your inventory.')
            char_sheet[2] -= consumables[player_choice][2]
            char_sheet[3].append(consumables[player_choice][0])


def use_potions(char_sheet):
    did_drink = False

    print('\nYou have the following potions in your inventory: ')
    for i in range(0, len(char_sheet[3])):
        print(str(i + 1) + '. ' + char_sheet[3][i])
    print(str(len(char_sheet[3]) + 1) + '. Return')
    player_choice = None
    while player_choice not in range(0, len(char_sheet[3]) + 1):
        player_choice = int(input("What is your choice?: ")) - 1
        if player_choice == len(char_sheet[3]):
            break
        else:
            potion_name = char_sheet[3][player_choice]
            the_consumable = []
            old_health = char_sheet[4]
            old_mana = char_sheet[12]
            for potion in consumables:
                if potion_name == potion[0]:
                    the_consumable.append(potion)
            if "Health" in the_consumable[0][0]:
                char_sheet[4] += the_consumable[0][1]
                if char_sheet[4] > char_sheet[9]:
                    char_sheet[4] = char_sheet[9]
                health_difference = char_sheet[4] - old_health
                print('\nYou drink ' + the_consumable[0][0] + ' and regain ' + str(health_difference) + ' health.')
            elif "Mana" in the_consumable[0][0]:
                char_sheet[12] += the_consumable[0][1]
                if char_sheet[12] > char_sheet[13]:
                    char_sheet[12] = char_sheet[13]
                mana_difference = char_sheet[12] - old_mana
                print('\nYou drink ' + the_consumable[0][0] + ' and regain ' + str(health_difference) + ' mana.')
            char_sheet[3].remove(char_sheet[3][player_choice])
            did_drink = True
    return did_drink
