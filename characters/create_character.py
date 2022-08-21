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
    char_name = "Testman" #input('\nWhat is your characters name?: ')
    load_char = open(f'{char_name}.json')
    char_sheet = json.load(load_char)

    print(char_sheet["name"])

    argument_input = ""
    for attribute in char_sheet.values():
            argument_input += str(attribute)
