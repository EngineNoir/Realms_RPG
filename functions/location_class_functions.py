import random
import json
import time

from functions.character_class_functions import Character
from functions.combat_function import combat_time
from functions.creature_class_functions import Creature
from functions.boss_class_functions import Boss
from functions.character_inspection import inspect_sheet
from functions.potion_class_functions import use_potions
from functions.inventory_class_functions import Inventory

load_creatures = open('jsons/creatures.json')
creatures = json.load(load_creatures)

load_bosses = open('jsons/bosses.json')
bosses = json.load(load_bosses)


class Location:
    def __init__(
        self,
        # --------------
        name: str,
        rooms_min: int,
        rooms_max: int,
        entry: str,
        rooms: list,
        encounters: list,
        final_room: str,
        boss_death: str,
        final_return: str,
        ):

        self.name = name
        self.rooms_min = rooms_min
        self.rooms_max = rooms_max
        self.current_room = 0
        self.entry = entry
        self.rooms = rooms
        self.encounters = encounters
        self.final_room = final_room
        self.boss_death = boss_death
        self.final_return = final_return

    def explore(self, player: Character, inventory: Inventory):
        number_of_rooms = random.randint(self.rooms_min, self.rooms_max)
        boss = self.generate_boss(bosses)
        print(self.entry)

        while self.current_room < number_of_rooms and player.health > 0:
            print('\nYou may do the following:\n1. Continue Exploring.\n2. Stealth.\n3. Use Magic.\n4. Use a potion'
                    '\n5. Inspect Character Sheet\n6. Leave the Location.')
            player_choice = None
            while player_choice not in list(range(1,7)):
                while True:
                    try:
                        player_choice = int(input('\nWhat would you like to do?: '))
                    except ValueError:
                        print("Please select a valid action.")
                    else:
                        break

                match player_choice:
                    case 1:
                        print(random.choice(self.rooms))
                        if_combat = random.randint(0, 100)
                        if if_combat < 50:
                            enemies = self.generate_enemies(creatures)
                            enemy = random.choice(enemies)
                            print(f"\nYou encounter a(n) {enemy.name}!")
                            self.stealth(player, enemy)
                            if player.health > 0:
                                self.current_room += 1 #need a check for if the combat succeeded
                            else: break
                        else:
                            print(random.choice(self.encounters))
                            if player.health < player.max_health:
                                player.health = min(player.health + 5, player.max_health)
                                print(f"\nYou rest and regain health up to {player.health}HP.")
                            self.current_room += 1
                    case 2:
                        player.stealth_in_exploration()
                    case 3:
                        # TODO
                        return 0
                    case 4:
                        use_potions(player)
                    case 5:
                        inspect_sheet(player, inventory)
                    case 6:
                        print("\nYou trace your path back to the Village.")
                        time.sleep(1)
                        return 0
                    case _:
                        print("\nPlease select a valid action.")

        if self.current_room == number_of_rooms and self.name not in player.cleared_dungeons:
            print(self.final_room)
            if player.stealth:
                print(f"\n{boss.name} notices you. Prepare for combat!")
                player.stealth = False
            combat_outcome = combat_time(player, boss)
            if player.health > 0 and combat_outcome:
                player.cleared_dungeons.append(self.name)
                print(self.boss_death)
                inventory.loot_boss(player, boss)
            else: return 0
        elif self.name in player.cleared_dungeons:
            print(self.final_return)

        return 0

    def stealth(self, player: Character, enemy: Creature):
        if player.stealth == False or enemy.awareness > player.dexterity:
            print("\nYou are spotted by the enemy. Prepare for combat!")
            combat_time(player, enemy)
        elif enemy.awareness <= player.dexterity:
            print(f"\nYou spot a(n) {enemy.name}, but remain hidden.\nDo you wish to: \n1.Ambush {enemy.name}\n2.Sneak away")
            while True:
                try:
                    choice = int(input("\nWhat do you choose?: "))
                except:
                    print("\nYou must select a number!")
                else:
                    break
            match choice:
                case 1:
                    player.deal_damage_to_enemy(enemy)
                    if enemy.health > 0:
                        print("\nYou are no longer stealthed! Prepare for combat!")
                    combat_time(player, enemy)
                case 2:
                    print("\nYou stealth away")
                case _:
                    print("\nInvalid number chosen.")
                    while True:
                        try:
                            choice = int(input("\nWhat do you choose?: "))
                        except:
                            print("\nYou must select a number!")
                        else:
                            break
        return 0


    def generate_boss(self, boss_list: list):
       for boss in boss_list:
          if boss["location"] == self.name:
            b = boss
            boss_class = Boss(b["name"],
                        b["moveset"],
                        b["health"],
                        b["damage_min"],
                        b["damage_max"],
                        b["damage_final"],
                        b["armor"],
                        b["loot"],
                        b["location"],
                        b["gold"],
                        b["xp"],
                        b["awareness"],
                        b["speed"],
                        b["taunts"])
            return boss_class

    def generate_enemies(self, enemy_list: list):
        enemies = []
        for enemy in enemy_list:
            if enemy["location"] == self.name:
                e = enemy
                enemy_class = Creature(e["name"],
                            e["moveset"],
                            e["health"],
                            e["damage_min"],
                            e["damage_max"],
                            e["armor"],
                            e["loot"],
                            e["location"],
                            e["gold"],
                            e["xp"],
                            e["awareness"],
                            e["speed"])
                enemies.append(enemy_class)
        return enemies
