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
        armor: str,
        weapon: str,
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

    def get_char_class(self, char_class):
        pass

    def add_to_inventory(self, item):
        if len(self.inventory) < 5 and len(self.inventory) >= 0:
            self.inventory.append(item)



def load_character():
    # ask for the character name
    char_name = input("\nWhat is your character's name?: )
    char_sheet = json.load(open(f'{char_name}.json'))
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

    # save the dictionary as a json file
    char_sheet_save = json.dumps(char_dictionary, indent=1)
    with open(f'{char_dictionary["name"]}' + '.json', 'w') as outfile:
        outfile.write(char_sheet_save)



if __name__ == "__main__":
    # print(Character(
    #     "Henk",
    #     "Knight",
    #     1,
    #     2,
    #     3,
    #     4,
    #     5,
    #     6,
    #     [],
    #     "shit",
    #     "shit",
    #     "shit",
    #     "shit",
    #     []
    #     ).char_class)


