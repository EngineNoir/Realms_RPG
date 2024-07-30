import random
import json
import time
import os

from colorama import Fore
from functions.inventory_class_functions import Inventory

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
        potions: list,
        armors: list,
        weapons: list,
        amulets: list,
        rings: list,
        # --------------
        eq_armor: dict,
        eq_weapon: dict,
        eq_amulet: dict,
        eq_ring_1: dict,
        eq_ring_2: dict,
        # --------------
        abilities: list,
        abilities_to_learn: list,
        armor_prof: str,
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
        self.potions = potions
        self.armors = armors
        self.weapons = weapons
        self.amulets = amulets
        self.rings = rings

        self.eq_armor = eq_armor
        self.eq_weapon = eq_weapon
        self.eq_amulet = eq_amulet
        self.eq_ring_1 = eq_ring_1
        self.eq_ring_2 = eq_ring_2

        self.armor_prof = armor_prof
        self.abilities = abilities
        self.abilities_to_learn = abilities_to_learn

        self.stealth = False
        self.max_health = max_health
        self.max_mana = max_mana

        self.current_xp = current_xp
        self.xp_to_level = (self.strength + self.dexterity + self.willpower) * 10 + self.level * 20

        self.cleared_dungeons = cleared_dungeons

    def weapon_attack(self):
        # get the right ability and compute total damage potential
        attack_potential =  self.determine_weapon_ability() + self.eq_weapon['damage']
        successes = 0

        # compute your damage output
        for i in range(attack_potential):
            roll = random.randint(1,6)
            if roll >= 4:
                successes += 1

        # crit if outcome >= 4/5*potential
        if successes >= (4/5)*attack_potential:
            successes += self.eq_weapon['damage']

        # need to include the target's defences to set up a "you miss" outcome
        return successes

    def determine_weapon_ability(self):
        # function that accesses a Character value based on weapon ability value
        if self.eq_weapon['ability'] == 'strength':
            return self.strength + round(0.5 * max(self.dexterity, self.willpower))
        elif self.eq_weapon['ability'] == 'dexterity':
            return self.dexterity + round(0.5 * max(self.strength, self.willpower))
        else:
            return self.willpower + round(0.5 * max(self.strength, self.dexterity))

    def deal_damage_to_enemy(self, target):
        # either deal dmg - armor or 0, negative values will heal the enemy (bug!)
        damage_dealt = max(self.weapon_attack() - target.armor, 0)
        output_text = 'You ' + random.choice(self.eq_weapon['moveset'])
        if damage_dealt > 0:
            output_text += f' dealing {damage_dealt} damage to {target.name}.'
            target.health -= damage_dealt
        else:
            fails = ["your attack misses.", "you fail to deal damage.", "the enemy dodges out of the way.", "your attack fails to connect.",
                "you underestimate the opponent's speed and miss."]
            output_text += f' but {random.choice(fails)}'
        print(f"{Fore.BLUE}\n--- YOUR DAMAGE ---")
        print(f"\n{output_text}{Fore.RESET}")

    def attempt_stealth_in_combat(self, target):
        print(f"{Fore.BLUE}\n--- STEALTH ---")
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
            print(f"You succeed in hiding!{Fore.RESET}")
            self.stealth = True
        elif self.stealth:
            print(f'\nYou remain hidden.{Fore.RESET}')
        else:
            print(f"\n{Fore.RED}--- STEALTH FAILED ---")
            print(f"You fail to hide! Your opponent seizes the opportunity and strikes!{Fore.RESET}")
            target.deal_damage_to_player(self)

    def fleeing_combat(self, target):
        print(f"\n{Fore.BLUE}--- FLEE ---")
        print("\nYou attempt to flee and ...")
        # more suspence >:)
        time.sleep(1)
        print("\n...")
        time.sleep(1)
        # see if sprinting > enemy speed, and if you're stealthed, auto-succeed
        is_flee_succesful = False
        flight_skill = max(self.strength, self.dexterity)
        if flight_skill > target.speed:
            print(f"You succesfully escape from your opponent!{Fore.RESET}")
            is_flee_succesful = True
        elif self.stealth:
            print(f"You sneak away succesfully!{Fore.RESET}")
            is_flee_succesful = True
        else:
            print(f"{Fore.RED}You fail to flee succesfully, and your opponent strikes at you!{Fore.RESET}")
            target.deal_damage_to_player(self)
            is_flee_succesful = False
        return is_flee_succesful

    def stealth_in_exploration(self):
        print(f"\n{Fore.BLUE}--- STEALTH ---")
        if self.stealth == False:
            print(f'\nYou move quietly, effectively entering stealth.{Fore.RESET}')
            self.stealth = True
        else:
            print(f'\nYou remain stealthed.{Fore.RESET}')

    def gain_xp(self, xp):
        self.current_xp += xp
        print("\nYou've gained " + str(xp) + " XP.")

    def increase_ability(self):
        ability_chosen = None
        player_choice = None
        while player_choice not in [1,2,3]:
            print(f"\n{Fore.GREEN}--- INCREASE ATTRIBUTE ---{Fore.RESET}")
            print('\nChoose which of the three attributes you wish to increase by 1.'
                    '\n\n1. Strength\n2. Dexterity\n3. Willpower')
            while True:
                try:
                    player_choice = int(input(f'\n{Fore.YELLOW}What is your choice?: {Fore.RESET}'))
                except ValueError:
                    print(f"\n{Fore.RED}Please select a valid option.{Fore.RESET}")
                else:
                    break
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
        if ability_chosen != None:
            print(f"\n{Fore.GREEN}--- SUCCESS ---")
            print(f'\n{ability_chosen.upper} increased by 1.{Fore.RESET}')
        return ability_chosen

    def level_up(self):
        if self.current_xp >= self.xp_to_level:
            print(f"\n{Fore.GREEN}--- LEVEL UP ---{Fore.RESET}")
            print(f'\nYou have {self.current_xp} XP. Do you wish to spend {self.xp_to_level} XP to level up?')
            answer_input = None
            while answer_input not in [1,2]:
                print(f"\n1. Yes\n2. {Fore.RED}No{Fore.RESET}")
                while True:
                    try:
                        answer_input = int(input(f'{Fore.YELLOW}\nWhat is your choice?: {Fore.RESET}'))
                    except ValueError:
                        print(f"\n{Fore.RED}Please select a valid option.{Fore.RESET}")
                    else:
                        break
            match answer_input:
                case 1:
                    increased = self.increase_ability()
                    if increased == None:
                        print(f"\n{Fore.RED}--- LEVEL UP CANCELLED ---")
                        print(f"\nNo ability selected. Exiting level up menu.{Fore.RESET}")
                        time.sleep(1)
                        return 0
                    self.health += 5
                    self.mana += self.willpower
                    self.max_health += 5
                    self.max_mana += self.willpower
                    self.level += 1
                    self.current_xp -= self.xp_to_level
                    self.xp_to_level = (self.strength + self.dexterity + self.willpower) * 10 + self.level * 20
                    self.gain_abilities()
                    print(f"{Fore.GREEN}\n--- SUCCESS ---")
                    print(f'\nYou have successfully leveled up and are now level {self.level}!{Fore.RESET}')
                case 2:
                    print(f"\n{Fore.RED}--- LEVEL UP CANCELLED ---")
                    print(f"\nNo ability selected. Exiting level up menu.{Fore.RESET}")
                    time.sleep(1)
                    return 0
        return 0

    def gain_abilities(self):
        if self.level == 3 and self.abilities_to_learn[0] not in self.abilities:
            self.abilities.append(self.abilities_to_learn[0])
            print(f"\n{Fore.GREEN}--- NEW ABILITY ---{Fore.RESET}")
            print(f"\nYou have learned {Fore.RED}{self.abilities_to_learn[0]}{Fore.RESET}!")
        elif self.level == 7 and self.abilities_to_learn[1] not in self.abilities:
            self.abilities.append(self.abilities_to_learn[1])
            print(f"\n{Fore.GREEN}--- NEW ABILITY ---{Fore.RESET}")
            print(f"\nYou have learned {Fore.RED}{self.abilities_to_learn[1]}{Fore.RESET}!")
        elif self.level == 12 and self.abilities_to_learn[2] not in self.abilities:
            self.abilities.append(self.abilities_to_learn[2])
            print(f"\n{Fore.GREEN}--- NEW ABILITY ---{Fore.RESET}")
            print(f"\nYou have learned {Fore.RED}{self.abilities_to_learn[2]}{Fore.RESET}!")


# MAKE AND SAVE CHARACTER -----------------------------
def make_character(classes, armors, weapons, amulets, rings):
    # ask for character's name as a string input
    char_name = None
    while True:
        try:
            char_name = str(input(f"\nWhat is your character's name? (enter '{Fore.RED}exit{Fore.RESET}' to terminate): "))
            if char_name == 'exit':
                return 0
        except ValueError:
            print(f"\n{Fore.RED}Please input a valid name.{Fore.RESET}")
        else:
            break

    # index over the class names in classes list and present the options
    print(f'\nPick one of the following classes.')
    i = 1
    for char_class in classes:
        print(f"{i}. {Fore.YELLOW}{char_class["class_name"]}{Fore.RESET}"
            f" (STR: {char_class["strength"]}, DEX {char_class["dexterity"]}, WILL: {char_class["willpower"]}) - "
            f"{char_class["description"]}")
        i += 1

    # makes the player choose a class from the given options
    class_choice = None
    while class_choice not in range(0, len(classes)):
        # we add the minus one because choice number 1 is indexed by 0
        while True:
            try:
                class_choice = int(input(f'\n{Fore.YELLOW}What is your choice?: {Fore.RESET}')) - 1
            except ValueError:
                print(f"\n{Fore.RED}Please select a valid option.{Fore.RESET}")
            else:
                break

    chosen_class = classes[class_choice]
    #compute starting health and mana
    starting_health = 10 + chosen_class["strength"] + 0.5*chosen_class["dexterity"]
    starting_mana = 5 + chosen_class["willpower"]

    # get some starting equipment
    starting_weapon = weapons[chosen_class["starter_weapon"]]
    starting_armor = armors[chosen_class["starter_armor"]]
    starting_amulet = amulets[chosen_class["starter_amulet"]]
    starting_ring_1 = rings[chosen_class["starter_ring_1"]]
    starting_ring_2 = rings[chosen_class["starter_ring_1"]]

    player_character = Character(char_name,
        chosen_class["class_name"],
        1,
        chosen_class["strength"],
        chosen_class["dexterity"],
        chosen_class["willpower"],
        starting_health,
        starting_mana,
        chosen_class["starter_gold"],
        [],
        [],
        [],
        [],
        [],
        starting_armor,
        starting_weapon,
        starting_amulet,
        starting_ring_1,
        starting_ring_2,
        chosen_class["abilities"],
        chosen_class["abilities_to_learn"],
        chosen_class["armor_prof"],
        starting_health,
        starting_mana,
        0,
        100,
        [])

    # save character as json
    save_character(player_character)
    return player_character

def load_character():
    # ask for the character name
    print(f"\n{Fore.GREEN}--- LOAD CHARACTER ---{Fore.RESET}")
    while True:
        try:
            char_name = input(f"\nWhat is your character's name? (enter '{Fore.RED}exit{Fore.RESET}'to terminate): ")
            if char_name == 'exit':
                return None
        except ValueError:
            print(f'\n{Fore.RED}Please input a valid character name.{Fore.RESET}')
        try:
            char_sheet = json.load(open(f'characters/{char_name}.json'))
        except FileNotFoundError:
            print(f"\nPlease input an existing character name. Input '{Fore.RED}exit{Fore.RESET}' to terminate.")
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
                                char_sheet['potions'],
                                char_sheet['armors'],
                                char_sheet['weapons'],
                                char_sheet['amulets'],
                                char_sheet['rings'],
                                char_sheet['eq_armor'],
                                char_sheet['eq_weapon'],
                                char_sheet['eq_amulet'],
                                char_sheet['eq_ring_1'],
                                char_sheet['eq_ring_2'],
                                char_sheet['abilities'],
                                char_sheet['abilities_to_learn'],
                                char_sheet['armor_prof'],
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
                        'potions': player_character.potions,
                        'armors': player_character.armors,
                        'weapons': player_character.weapons,
                        'amulets': player_character.amulets,
                        'rings': player_character.rings,
                        'eq_armor': player_character.eq_armor,
                        'eq_weapon': player_character.eq_weapon,
                        'eq_amulet': player_character.eq_amulet,
                        'eq_ring_1': player_character.eq_ring_1,
                        'eq_ring_2': player_character.eq_ring_2,
                        'abilities': player_character.abilities,
                        'abilities_to_learn': player_character.abilities_to_learn,
                        'armor_prof': player_character.armor_prof,
                        'stealth': False,
                        'max_health': player_character.max_health,
                        'max_mana': player_character.max_mana,
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
