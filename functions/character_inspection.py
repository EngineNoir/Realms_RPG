# inspect sheet new

def inspect_sheet(player):
    print('\n-----------------')
    print('Name: ' + player.name)
    print('Class: ' + player.char_class)
    print('Level: ' + str(player.level))
    print('Current XP: ' + str(player.current_xp))
    print('XP until next level: ' + str(player.xp_to_level))

    print('\nHealth: ' + str(player.health) + ' (Max: ' + str(player.max_health) + ').')
    print('Mana: ' + str(player.mana) + ' (Max: ' + str(player.max_mana) + ').')
    print('Strength: ' + str(player.strength))
    print('Dexterity: ' + str(player.dexterity))
    print('Willpower: ' + str(player.willpower))

    print('\nWeapon: ' + player.eq_weapon['weapon_name'] +
            '\nArmor: ' + player.eq_armor['armor_name'] +
            ' (Def: ' + str(player.eq_armor['defence']) + ').')
    print('Amulet: ' + player.eq_amulet["name"])
    print('Ring 1: ' + player.eq_ring_1["name"])
    print('Ring 2: ' + player.eq_ring_2["name"])
    print('Gold: ' + str(player.gold))
    print('Potions: ' + str(player.potions))
    print('Abilities: ' + str(player.abilities))
    print('-----------------')

    # level option if there's enough XP
    choice = None
    print("1. Equip Something\n2. Unequip Something\n3. Level Up\n4. Return")
    while choice == None or choice not in list(range(1,5)):
        while True:
            try:
                choice = int(input("\nWhat is your choice?: "))
            except ValueError:
                print("\nPlease select a valid input")
            else:
                break
        match choice:
            case 1:
                list_and_equip(player)
                return 0
            case 2:
                list_and_unequip(player)
                return 0
            case 3:
                if player.current_xp >= player.xp_to_level:
                    player.level_up()
                    return 0
                else:
                    print("\nYou do not have enough XP to level.")
            case 4:
                return 0

def list_and_equip(player):
    #TODO
    return 0

def list_and_unequip(player):
    #TODO
    return 0
