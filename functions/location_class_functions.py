import random
import json
import time

from colorama import Fore

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
        print(f"\n{Fore.BLUE}--- ENTERED LOCATION ---{Fore.RESET}")
        print(self.entry)

        while self.current_room < number_of_rooms and player.health > 0:
            print(f"\n{Fore.BLUE}--- EXPLORE ---{Fore.RESET}")
            print('\n1. Continue Exploring.\n2. Stealth.\n3. Use a potion'
                f'\n4. Inspect Character Sheet\n5. {Fore.RED}Leave the Location{Fore.RESET}')
            player_choice = None
            while player_choice not in list(range(1,6)):
                while True:
                    try:
                        player_choice = int(input(f'\n{Fore.YELLOW}What would you like to do?: {Fore.RESET}'))
                    except ValueError:
                        print(f"\n{Fore.RED}Please select a valid option.{Fore.RESET}")
                    else:
                        break

                match player_choice:
                    case 1:
                        print(f"\n{Fore.BLUE}--- LOCATION DESCRIPTION ---{Fore.RESET}")
                        print(random.choice(self.rooms))
                        if_combat = random.randint(0, 100)
                        if if_combat < 50:
                            enemies = self.generate_enemies(creatures)
                            enemy = random.choice(enemies)
                            print(f"\n{Fore.RED}--- ENEMY ENCOUNTER ---")
                            print(f"\nYou encounter a(n) {enemy.name}!{Fore.RESET}")
                            self.stealth(player, enemy)
                            if player.health > 0:
                                self.current_room += 1 #need a check for if the combat succeeded
                            else: break
                        else:
                            print(f"\n{Fore.GREEN}--- LOCATION ENCOUNTER ---{Fore.RESET}")
                            print(random.choice(self.encounters))
                            if player.health < player.max_health:
                                player.health = min(player.health + 5, player.max_health)
                                print(f"\n{Fore.GREEN}You regain health up to {Fore.RED}{player.health}{Fore.GREEN} HP.{Fore.RESET}")
                            if player.mana < player.max_mana:
                                player.mana = min(player.mana + 5, player.max_mana)
                                print(f"\n{Fore.GREEN}You regain mana up to {Fore.BLUE}{player.mana}{Fore.RESET} MP.{Fore.RESET}")
                            self.current_room += 1
                    case 2:
                        player.stealth_in_exploration()
                    case 3:
                        use_potions(player)
                    case 4:
                        inspect_sheet(player, inventory)
                    case 5:
                        print(f"\n{Fore.BLUE}You trace your path back to the Village.{Fore.RESET}")
                        time.sleep(1)
                        return 0
                    case _:
                        print(f"\n{Fore.RED}Please select a valid option.{Fore.RESET}")

        if self.current_room == number_of_rooms and self.name not in player.cleared_dungeons:
            print(f"\n{Fore.RED}--- BOSS ENCOUNTER ---{Fore.RESET}")
            print(self.final_room)
            if player.stealth:
                print(f"\n{Fore.RED}--- STEALTH CANCELLED ---")
                print(f"\n{boss.name} notices you. Prepare for combat!{Fore.RESET}")
                player.stealth = False
            combat_outcome = combat_time(player, boss)
            if player.health > 0 and combat_outcome:
                player.cleared_dungeons.append(self.name)
                print(f"\n{Fore.GREEN}--- VICTORY ---")
                print(f"{self.boss_death}{Fore.RESET}")
                inventory.loot_boss(player, boss)
            else: return 0
        elif self.name in player.cleared_dungeons:
            print(self.final_return)

        return 0

    def stealth(self, player: Character, enemy: Creature):
        if player.stealth == False:
            combat_time(player, enemy)
        elif enemy.awareness > player.dexterity:
            print(f"{Fore.RED}\n--- STEALTH CANCELLED ---")
            print(f"\nYou are spotted by the enemy! Prepare for combat!{Fore.RESET}")
            combat_time(player, enemy)
        elif enemy.awareness <= player.dexterity:
            print(f"\n{Fore.RED}--- ENEMY SPOTTED ---")
            print(f"\nYou spot a(n) {enemy.name}, but remain hidden.{Fore.RESET}\n1. Ambush {enemy.name} (start combat)\n2. Sneak away")
            while True:
                try:
                    choice = int(input(f"\n{Fore.YELLOW}What do you choose?: {Fore.RESET}"))
                except:
                    print(f"\n{Fore.RED}Please select a valid option.{Fore.RESET}")
                else:
                    break
            match choice:
                case 1:
                    player.deal_damage_to_enemy(enemy)
                    if enemy.health > 0:
                        print(f"{Fore.RED}\n--- STEALTH CANCELLED ---")
                        print(f"\nYou are no longer stealthed! Prepare for combat!{Fore.RESET}")
                    combat_time(player, enemy)
                case 2:
                    print(f"\n{Fore.GREEN}You stealth away{Fore.RESET}")
                case _:
                    print(f"\n{Fore.RED}Please select a valid option.{Fore.RESET}")
                    while True:
                        try:
                            choice = int(input(f"\n{Fore.YELLOW}What do you choose?: {Fore.YELLOW}"))
                        except:
                            print(f"\n{Fore.RED}Please select a valid option.{Fore.RESET}")
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
