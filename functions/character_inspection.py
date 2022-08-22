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

    print('\nWeapon: ' + player.weapon['weapon_name'] + '\nArmor: ' + player.armor['armor_name'] + 
            ' (Armor: ' + str(player.armor['defence']) + ').')
    print('Gold: ' + str(player.gold))
    print('Inventory: ' + str(player.inventory))
    print('Spells: ' + str(player.spellbook))
    print('-----------------')
    
    if player.current_xp >= player.xp_to_level:
        player.level_up()