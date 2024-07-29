import random

from colorama import Fore
from functions.character_class_functions import Character
from functions.creature_class_functions import Creature

class Boss(Creature):
    def __init__(
        self,
        # --------------
        name: str,
        moveset: list,
        health: int,
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

        super().__init__(name, moveset, health, damage_min, damage_max, armor, loot, location, gold, xp,awareness, speed)
        self.health_max = health
        self.damage_final = damage_final
        self.taunts = taunts
        self.stage = 1


    def taunt_player(self):
        if self.health < 0.75*self.health_max and self.stage == 1:
            print(f"{Fore.RED}\n--- PHASE 2 ---")
            print(self.taunts[1] + f'{Fore.RESET}')
            self.stage = 2
        if self.stage == 2 and self.health < 0.5*self.health_max:
            print(f"{Fore.RED}\n--- PHASE 3 ---")
            print(self.taunts[2] + f'{Fore.RESET}')
            self.stage = 3


    def compute_damage(self):
        damage = self.damage_max
        if self.stage == 3:
            damage = self.damage_final
        return random.randint(self.damage_min, damage)

    def deal_damage_to_player(self, target: Character):
        self.taunt_player()
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
        print(f"\n{Fore.RED}--- BOSS DAMAGE ---")
        print(output_text + f"{Fore.RESET}")
