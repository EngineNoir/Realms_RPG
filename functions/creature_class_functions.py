import random

from functions.character_class_functions import Character

class Creature:
    def __init__(
        self,
        # --------------
        name: str,
        moveset: list,
        health: int,
        damage_min: int,
        damage_max: int,
        armor: int,
        loot: list,
        location: str,
        gold: int,
        xp: int,
        awareness: int,
        speed: int
        ):

        self.name = name
        self.moveset = moveset
        self.health = health
        self.damage_min = damage_min
        self.damage_max = damage_max
        self.armor = armor
        self.loot = loot
        self.location = location
        self.gold = gold
        self.xp = xp
        self.awareness = awareness
        self.speed = speed
        self.is_boss = False

    def compute_damage(self):
        return random.randint(self.damage_min, self.damage_max)

    def deal_damage_to_player(self, target: Character):
        damage_dealt = max(self.compute_damage() - target.eq_armor['defence'], 0)
        output_text = self.name + ' ' + random.choice(self.moveset) + ' '
        misses = ["which fails to break through your defences.", "missing its attack.",
                  "failing to connect the attack.", "unable to land the attack.",
                  "but you dodge away in time.", "barely missing you."]
        if damage_dealt > 0:
            output_text += 'dealing ' + str(damage_dealt) + ' damage.'
            target.health -= damage_dealt
        else:
            output_text += random.choice(misses)
        print(output_text)

    def spot_player(self, target: Character):
        if self.awareness >= target.dexterity:
            print('You are spotted!')
            target.stealth = False
