import random
import json
import os


class Character:
    def __init__(
        self,
        # --------------
        name: str,
        char_class: str,
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
        amulet: str,
        ring: str,
        # --------------
        spellbook: list,
    ):
        
        self.name = name
        self.char_class = char_class
        
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
        self.debuffs = {'poison': False}


    def set_initial_health(self):
        # need some revamping
        return 10

    def calc_mana(self):
        # need some revamping
        return 5

    def calc_gold(self):
        # uhhh
        return 100

    def get_char_class(self):
        pass

    def add_to_inventory(self, item):
        if len(self.inventory) < 5 and len(self.inventory) >= 0:
            self.inventory.append(item)


def make_character(classes, armors, weapons):
    # need to include try commands in case players input str instead of int or vice versa

    # ask for character's name as a string input
    char_name = str(input("\nWhat is your character's name?: "))
    
    # index over the class names in classes list and present the options
    i = 1
    for char_class in classes:
        print(str(i) + ". " + char_class["class_name"] + ' - ' + char_class["description"])
        i += 1
    
    # makes the player choose a class from the given options
    class_choice = None
    while class_choice not in range(0, len(classes)):
        # we add the minus one because choice number 1 is indexed by 0
        class_choice = int(input('Which class do you choose?: ')) - 1

    chosen_class = classes[class_choice]
    starting_health = 10 + chosen_class["strength"] + 0.5*chosen_class["dexterity"]
    starting_mana = 5 + chosen_class["willpower"]

    starting_weapon = weapons[chosen_class["starter_weapon"]]
    print(starting_weapon)
    starting_armor = armors[chosen_class["starter_armor"]]
    print(starting_armor)

    player_character = Character(char_name, chosen_class["class_name"], chosen_class["strength"], chosen_class["dexterity"],
                        chosen_class["willpower"], starting_health, starting_mana, chosen_class["starter_gold"], [], starting_armor, 
                        starting_weapon, None, None, [])
    
    save_character(player_character)
    print(player_character)
    


def load_character():
    # ask for the character name
    char_name = input("\nWhat is your character's name?: ")
    char_sheet = json.load(open(f'characters/{char_name}.json'))
    # generate a Character class object with the values from the json file
    player_character = Character(char_sheet['name'], char_sheet['char_class'], char_sheet['strength'], char_sheet['dexterity'], 
                        char_sheet['willpower'], char_sheet['health'], char_sheet['mana'], char_sheet['gold'], char_sheet['inventory'], 
                        char_sheet['armor'], char_sheet['weapon'], char_sheet['amulet'], char_sheet['ring'], char_sheet['spellbook'])
    return player_character


def save_character(player_character):
    # create a dictionary from values in player_character (character class object)
    char_dictionary = {'name': player_character.name, 'char_class': player_character.char_class, 'strength': player_character.strength, 
                        'dexterity': player_character.dexterity, 'willpower': player_character.willpower, 'health': player_character.health,
                        'mana': player_character.mana, 'gold': player_character.gold, 'inventory': player_character.inventory, 
                        'armor': player_character.armor, 'weapon': player_character.weapon, 'amulet': player_character.amulet,
                        'ring': player_character.ring, 'spellbook': player_character.spellbook}

    print(char_dictionary)
    # save the dictionary as a json file
    char_sheet_save = json.dumps(char_dictionary, indent=1)
    # export character sheet to the characters directory
    with open(f'characters/{char_dictionary["name"]}' + '.json', 'w') as outfile:
        outfile.write(char_sheet_save)


if __name__ == "__main__":
    
    load_classes = open('./jsons/classes.json')
    load_armors = open('./jsons/armors.json')
    load_weapons = open('./jsons/weapons.json')
    
    armors = json.load(load_weapons)
    weapons = json.load(load_weapons)
    character_classes = json.load(load_classes)

    print(weapons)
    print(character_classes)

