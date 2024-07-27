import json
from functions.character_class_functions import Character

load_armors = open('jsons/armors.json')
load_weapons = open('jsons/weapons.json')
load_amulets = open('jsons/amulets.json')
load_rings = open('jsons/rings.json')

armors = json.load(load_armors)
weapons = json.load(load_weapons)
amulets = json.load(load_amulets)
rings = json.load(load_rings)

class Inventory:
    def __init__(self,
        player: Character,
        armors: list,
        weapons: list,
        amulets: list,
        rings: list):

        self.player = player
        self.armors = armors
        self.weapons = weapons
        self.amulets = amulets
        self.rings = rings
