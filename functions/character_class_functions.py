import random
import json
import time
import os

class Character:
    def __init__(
        self,
        # --------------
        name: str,
        char_class: str,
        level: int,
        # --------------
        strength: int,
        dexterity: int,
        willpower: int,
        # --------------
        health: int,
        mana: int,
        # --------------
        gold: int,
        inventory: list,
        armor: dict,
        weapon: dict,
        amulet,
        ring,
        # --------------
        spellbook: list,
        # --------------
        max_health: int,
        max_mana: int,
        # --------------
        current_xp: int,
        xp_to_level: int,
        # --------------
        cleared_dungeons: list
    ):

        self.name = name
        self.char_class = char_class
        self.level = level

        self.strength = strength
        self.dexterity = dexterity
        self.willpower = willpower

        self.health = health
        self.mana = mana

        self.gold = gold
        self.inventory = inventory
        self.armor = armor
        self.weapon = weapon
        self.amulet = amulet
        self.ring = ring

        self.spellbook = spellbook

        self.stealth = False
        self.max_health = max_health
        self.max_mana = max_mana
        self.debuffs = {'poison': False}

        self.current_xp = current_xp
        self.xp_to_level = (self.strength + self.dexterity + self.willpower) * 10 + self.level * 20

        self.cleared_dungeons = cleared_dungeons

    def weapon_attack(self):
        # get the right ability and compute total damage potential
        attack_potential =  self.determine_weapon_ability() + self.weapon['damage']
        successes = 0

        # compute your damage output
        for i in range(attack_potential):
            roll = random.randint(1,6)
            if roll >= 4:
                successes += 1

        # crit if outcome >= 4/5*potential
        if successes >= (4/5)*attack_potential:
            successes += self.weapon['damage']

        # need to include the target's defences to set up a "you miss" outcome
        return successes

    def determine_weapon_ability(self):
        # function that accesses a Character value based on weapon ability value
        if self.weapon['ability'] == 'strength':
            return self.strength
        elif self.weapon['ability'] == 'dexterity':
            return self.dexterity
        else:
            return self.willpower

    def deal_damage_to_enemy(self, target):
        # either deal dmg - armor or 0, negative values will heal the enemy (bug!)
        damage_dealt = max(self.weapon_attack() - target.armor, 0)
        output_text = '\nYou ' + random.choice(self.weapon['moveset'])
        if damage_dealt > 0:
            output_text += ' dealing ' + str(damage_dealt) + ' damage to ' + target.name + '.'
            target.health -= damage_dealt
        else:
            fails = ["your attack misses.", "you fail to deal damage.", "the enemy dodges out of the way.", "your attack fails to connect.",
                "you underestimate the opponent's speed and miss."]
            output_text += ' but ' + random.choice(fails)
        print(output_text)

    def attempt_stealth_in_combat(self, target):
        print("\nYou attempt to stealth and ...")
        # add some tension
        time.sleep(1)
        print("\n...")
        time.sleep(1)
        # compute if dex roll > enemy awareness, and check if not already stealthing
        successes = 0
        for i in range(1, self.dexterity):
            roll = random.randint(1, 6)
            if roll >= 4:
                successes += 1
        if successes >= target.awareness and not self.stealth:
            print("You succeed in hiding!")
            self.stealth = True
        elif self.stealth:
            print('\nYou remain hidden.')
        else:
            print("You fail to hide! Your opponent seizes the opportunity and strikes!")
            target.deal_damage_to_player(self)

    def fleeing_combat(self, target):
        print("\nYou attempt to flee and ...")
        # more suspence >:)
        time.sleep(1)
        print("\n...")
        time.sleep(1)
        # see if sprinting > enemy speed, and if you're stealthed, auto-succeed
        is_flee_succesful = False
        flight_skill = max(self.strength, self.dexterity)
        if flight_skill > target.speed:
            print("You succesfully escape from your opponent!")
            is_flee_succesful = True
        elif self.stealth:
            print("You sneak away succesfully!")
            is_flee_succesful = True
        else:
            print("You fail to sneak away, and your opponent strikes at you!")
            target.deal_damage_to_player(self)
            is_flee_succesful = False
        return is_flee_succesful

    def stealth_in_exploration(self):
        if self.stealth == False:
            print('\nYou move quietly, effectively entering stealth.')
            self.stealth = True
        else:
            print('\nYou remain stealthed.')

    def gain_xp(self, xp):
        self.current_xp += xp
        print("\nYou've gained " + str(xp) + " XP.")

    def increase_ability(self):
        ability_chosen = None
        player_choice = int(input('\nChoose which of the three abilities you wish to increase by 1.'
                                                '\n1. Strength\n2. Dexterity\n3. Willpower\nAttribute to improve: '))
        match player_choice:
            case 1:
                self.strength += 1
                ability_chosen = "Strength"
            case 2:
                self.dexterity += 1
                ability_chosen = "Dexterity"
            case 3:
                self.willpower += 1
                ability_chosen = "Willpower"
            case _:
                print('\nInvalid selection.')
        if ability_chosen != None:
            print(f'\nYou have increased your ' + str(ability_chosen) + ' by 1.')
        return ability_chosen

    def level_up(self):
        if self.current_xp >= self.xp_to_level:
            print('\nYou have ' + str(self.current_xp) + ' XP. Do you wish to spend ' + str(self.xp_to_level) + ' XP to level up?')
            answer_input = int(input('1. Yes\n2. No\nSpend XP and level up?: '))
            match answer_input:
                case 1:
                    increased = self.increase_ability()
                    if increased == None:
                        print("\nNo ability selected. Exiting level up menu.")
                        time.sleep(1)
                        return 0
                    self.health += 5
                    self.mana += self.willpower
                    self.max_health += 5
                    self.max_mana += self.willpower
                    self.level += 1
                    self.current_xp -= self.xp_to_level
                    self.xp_to_level = (self.strength + self.dexterity + self.willpower) * 10 + self.level * 20
                    print('\nYou have successfully leveled up and are now level ' + str(self.level) +
                            '. Congratulations!')
                case 2:
                    return 0
                case _:
                    print('\nPlease input a valid response.')
                    answer_input = int(input('1. Yes\n2. No\nSpend XP and level up?: '))
        return 0


def make_character(classes, armors, weapons):
    # ask for character's name as a string input
    char_name = None
    while True:
        try:
            char_name = str(input("\nWhat is your character's name?: "))
        except ValueError:
            print("\nPlease input a valid name.")
            continue
        else:
            break

    # index over the class names in classes list and present the options
    print('\nPick one of the following classes.')
    i = 1
    for char_class in classes:
        print(str(i) + ". " + char_class["class_name"] + ' - ' + char_class["description"])
        i += 1

    # makes the player choose a class from the given options
    class_choice = None
    while class_choice not in range(0, len(classes)):
        # we add the minus one because choice number 1 is indexed by 0
        while True:
            try:
                class_choice = int(input('\nWhich class do you choose?: ')) - 1
            except ValueError:
                print('\nPlease select a valid input.')
            else:
                break

    chosen_class = classes[class_choice]
    #compute starting health and mana
    starting_health = 10 + chosen_class["strength"] + 0.5*chosen_class["dexterity"]
    starting_mana = 5 + chosen_class["willpower"]

    # get some starting equipment
    starting_weapon = weapons[chosen_class["starter_weapon"]]
    starting_armor = armors[chosen_class["starter_armor"]]

    player_character = Character(char_name, chosen_class["class_name"], 1, chosen_class["strength"], chosen_class["dexterity"],
                        chosen_class["willpower"], starting_health, starting_mana, chosen_class["starter_gold"], [], starting_armor,
                        starting_weapon, None, None, [], starting_health, starting_mana, 0, 100, [])

    # save character as json
    save_character(player_character)
    return player_character

def load_character():
    # ask for the character name
    while True:
        try:
            char_name = input("\nWhat is your character's name?: ")
        except ValueError:
            print('\nPlease input a valid character name.')
        try:
            char_sheet = json.load(open(f'characters/{char_name}.json'))
        except FileNotFoundError:
            print('\nPlease input an existing character name.')
        else:
            break

    # generate a Character class object with the values from the json file
    player_character = Character(char_sheet['name'],
                                char_sheet['char_class'],
                                char_sheet["level"],
                                char_sheet['strength'],
                                char_sheet['dexterity'],
                                char_sheet['willpower'],
                                char_sheet['health'],
                                char_sheet['mana'],
                                char_sheet['gold'],
                                char_sheet['inventory'],
                                char_sheet['armor'],
                                char_sheet['weapon'],
                                char_sheet['amulet'],
                                char_sheet['ring'],
                                char_sheet['spellbook'],
                                char_sheet['max_health'],
                                char_sheet['max_mana'],
                                char_sheet['current_xp'],
                                char_sheet['xp_to_level'],
                                char_sheet['cleared_dungeons'])
    return player_character


def save_character(player_character):
    # create a dictionary from values in player_character (character class object)
    char_dictionary = {'name': player_character.name,
                        'char_class': player_character.char_class,
                        'level': player_character.level,
                        'strength': player_character.strength,
                        'dexterity': player_character.dexterity,
                        'willpower': player_character.willpower,
                        'health': player_character.health,
                        'mana': player_character.mana,
                        'gold': player_character.gold,
                        'inventory': player_character.inventory,
                        'armor': player_character.armor,
                        'weapon': player_character.weapon,
                        'amulet': player_character.amulet,
                        'ring': player_character.ring,
                        'spellbook': player_character.spellbook,
                        'stealth': False,
                        'max_health': player_character.max_health,
                        'max_mana': player_character.max_mana,
                        'debuffs': {'poison': False},
                        'current_xp': player_character.current_xp,
                        'xp_to_level': player_character.xp_to_level,
                        'cleared_dungeons': player_character.cleared_dungeons}

    # save the dictionary as a json file
    char_sheet_save = json.dumps(char_dictionary, indent=1)
    # export character sheet to the characters directory
    # for this to work you have to be in the projects top level directory
    if not os.path.isdir('characters'): os.mkdir('characters')
    with open(f'characters/{char_dictionary["name"]}' + '.json', 'w') as outfile:
        outfile.write(char_sheet_save)
