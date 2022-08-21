import json

load_spells = open('jsons/spells.json')
spells = json.load(load_spells)


def character_creation():

    base_attributes = [['Str', 0], ['Dex', 0], ['Wil', 0]]
    character_classes = ['Knight', 'Cleric', 'Ranger',
                  'Druid', 'Mage', 'Warlock',
                  'Assassin', 'Bard', 'Thief']

    def assign_name():
        name = input('\nWhat is your name?: ')
        return name

    def assign_class(class_list):
        print('\nTime to choose a class. This will determine your ability scores and starting gear.')
        i = 1
        for char_class in class_list:
            print(str(i) + '. ' + char_class)
            i += 1
        choice_made = None
        while choice_made not in range(1, 10):
            choice_made = int(input("Class chosen: "))
        return choice_made

    def attribute_allocation(attribute_list, class_list):
        char_class = assign_class(class_list)
        armor = 0
        weapon = None
        if char_class == 1:
            attribute_list[0][1] = 8
            attribute_list[1][1] = 1
            attribute_list[2][1] = 1
            armor = [2, 'Heavy Plate Armor and Shield']
            weapon = ['Longsword', ['swing', 'thrust']]
            spellbook = []
        if char_class == 2:
            attribute_list[0][1] = 6
            attribute_list[1][1] = 1
            attribute_list[2][1] = 3
            armor = [2, 'Enchanted Plate']
            weapon = ['Mace', ['swing', 'slam']]
            spellbook = [spells[7], spells[8]]
        if char_class == 3:
            attribute_list[0][1] = 6
            attribute_list[1][1] = 3
            attribute_list[2][1] = 1
            armor = [2, 'Chainmail']
            weapon = ['Longbow', ['take aim and shoot', 'fire']]
            spellbook = []
        if char_class == 4:
            attribute_list[0][1] = 3
            attribute_list[1][1] = 1
            attribute_list[2][1] = 6
            armor = [1, "Animal Furs"]
            weapon = ['Coiled Branch', ['swing', 'slam']]
            spellbook = [spells[3], spells[4]]
        if char_class == 5:
            attribute_list[0][1] = 1
            attribute_list[1][1] = 1
            attribute_list[2][1] = 8
            armor = [1, "Arcanist's Robe"]
            weapon = ['Staff', ['swing', 'slam']]
            spellbook = [spells[0], spells[1], spells[9]]
        if char_class == 6:
            attribute_list[0][1] = 1
            attribute_list[1][1] = 3
            attribute_list[2][1] = 6
            armor = [1, 'Cultist Clothes']
            weapon = ['Ritual Dagger', ['stab', 'thrust']]
            spellbook = [spells[0], spells[2]]
        if char_class == 7:
            attribute_list[0][1] = 3
            attribute_list[1][1] = 6
            attribute_list[2][1] = 1
            armor = [1.5, 'Black Leather']
            weapon = ['Twin Daggers', ['thrust', 'slice']]
            spellbook = []
        if char_class == 8:
            attribute_list[0][1] = 1
            attribute_list[1][1] = 6
            attribute_list[2][1] = 3
            armor = [1.5, 'Artistic Leathers']
            weapon = ['Rapier', ['thrust', 'flourish with']]
            spellbook = [spells[5], spells[6]]
        if char_class == 9:
            attribute_list[0][1] = 1
            attribute_list[1][1] = 8
            attribute_list[2][1] = 1
            armor = [1.5, 'Leather Armor']
            weapon = ['Shortsword', ['thrust', 'swing']]
            spellbook = []
        return attribute_list, char_class, armor, weapon, spellbook

    def create_char_sheet(name, attribute_list, class_list):
        gold = 30                           # 2
        inventory = []                     # 3
        current_location = 0               # 8
        attributes, char_class, armor, weapon, spell_book = attribute_allocation(attribute_list, class_list)
        # class 5, armor 6, weapons 7, spellbook 11, mana 12, mana_max 13, health_max 9
        health = 10 + 0.5 * max(attributes[0][1], attributes[1][1])   # 4
        mana = 10 + attributes[2][1]
        mana_max = mana
        health_max = health                # 9
        hidden = False                     # 10
        current_xp = 0                     # 14
        level = 1                          # 16
        xp_to_level = 100                  # 15
        dungeons_completed = []
        character_sheet = [name, attribute_list, gold, inventory,
                           health, class_list[char_class-1],
                           armor, weapon,
                           current_location,
                           health_max, hidden,
                           spell_book, mana,
                           mana_max, current_xp,
                           xp_to_level, level,
                           dungeons_completed]
        return character_sheet

    char_name = assign_name()

    char_sheet = json.dumps(create_char_sheet(char_name, base_attributes, character_classes), indent=1)

    with open('characters/' + char_name + '.json', 'w') as outfile:
        outfile.write(char_sheet)

    return char_name
