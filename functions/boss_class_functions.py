import random

from functions.character_class_functions import Character

class Boss:
    def __init__(
        self,
        # --------------
        name: str,
        moveset: list,
        health: int,
        health_max: int,
        damage_min: int,
        damage_max: int,
        damage_final: int,
        armor: int,
        loot: list,
        location: str,
        gold: int,
        xp: int,
        awareness: int,
        speed: int,
        taunts: list
        ):
        
        self.name = name
        self.moveset = moveset
        self.health = health
        self.health_max = health_max
        self.damage_min = damage_min 
        self.damage_max = damage_max
        self.damage_final = damage_final
        self.armor = armor
        self.loot = loot
        self.location = location
        self.gold = gold
        self.xp = xp
        self.awareness = awareness   
        self.speed = speed   
        self.taunts = taunts


    def taunt_player(self):
        spoken_once = False
        spoken_twice = False

        if self.health < 0.75*self.health_max and not spoken_once:
            print(self.taunts[1])
            spoken_once = True
        if spoken_once and not spoken_twice and self.health < 0.33*self.health_max:
            print(self.taunts[2])
            spoken_twice = True


    def compute_damage(self):
        if self.health > 0.33*self.health_max:
            damage = self.damage_max
        else:
            damage = self.damage_final
        return random.randint(self.damage_min, damage) 

    def deal_damage_to_player(self, target: Character):
        self.taunt_player()
        damage_dealt = max(self.compute_damage() - target.armor['defence'], 0) 
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