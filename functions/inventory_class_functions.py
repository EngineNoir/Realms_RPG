import json
import random

from colorama import Fore

class Inventory:
    def __init__(self,
        armors: dict,
        weapons: dict,
        amulets: dict,
        rings: dict):

        self.armors = armors
        self.weapons = weapons
        self.amulets = amulets
        self.rings = rings

    def equipment_functions(self, player):
        choice = None
        while choice != 3:
            print(f"\n{Fore.GREEN}--- EQUIPMENT OPTIONS ---{Fore.RESET}")
            print(f'\n1. List Equipped Items'
                f'\n2. List and Equip items from inventory'
                f'\n3. {Fore.RED}Return{Fore.RESET}')
            while True:
                try:
                    choice = int(input(f"\n{Fore.YELLOW}What is your choice?: {Fore.RESET}"))
                except ValueError:
                    print(f"\n{Fore.RED}Please select a valid option.{Fore.RESET}")
                else:
                    break
            match choice:
                case 1:
                    self.list_equipped(player)
                case 2:
                    self.list_inventory(player)
                case 3:
                    return 0
                case _:
                    print(f"\n{Fore.RED}Please select a valid option.{Fore.RESET}")

    def list_equipped(self, player):
        print(f"\n{Fore.GREEN}--- EQUIPPED ---{Fore.RESET}")
        print(f'Weapon: {Fore.RED}{player.eq_weapon["weapon_name"]}{Fore.RESET} '
            f'(Dmg: {Fore.RED}{player.eq_weapon["damage"]}{Fore.RESET}, {Fore.RED}{player.eq_weapon["ability"]}{Fore.RESET} scaling)')
        print(f'Armor: {Fore.RED}{player.eq_armor["armor_name"]}{Fore.RESET} '
            f'(Def: {Fore.RED}{player.eq_armor["defence"]}{Fore.RESET}, {Fore.RED}{player.eq_armor["weight"]}{Fore.RESET})')
        print(f'Amulet: {Fore.RED}{player.eq_amulet["name"]}{Fore.RESET} '
            f'(Add {Fore.RED}{player.eq_amulet["effect"]}{Fore.RESET} to '
                    f'{Fore.RED}{player.eq_amulet["stat"] or None}{Fore.RESET})')
        print(f'Ring 1: {Fore.RED}{player.eq_ring_1["name"]}{Fore.RESET} '
            f'(Add {Fore.RED}{player.eq_ring_1["effect"]}{Fore.RESET} to '
                    f'{Fore.RED}{player.eq_ring_1["stat"] or None}{Fore.RESET})')
        print(f'Ring 2: {Fore.RED}{player.eq_ring_2["name"]}{Fore.RESET} '
            f'(Add {Fore.RED}{player.eq_ring_2["effect"]}{Fore.RESET} to '
                    f'{Fore.RED}{player.eq_ring_2["stat"] or None}{Fore.RESET})')

    def list_inventory(self, player):
        choice = None
        while choice != 2:
            print(f"{Fore.GREEN}\n--- INVENTORY ---{Fore.RESET}")
            print("Weapons:")
            for weapon in player.weapons:
                print(f'- {Fore.RED}{weapon} {Fore.RESET}(Dmg: {Fore.RED}{self.weapons[weapon]["damage"]}{Fore.RESET},'
                    f' {Fore.RED}{self.weapons[weapon]["ability"]}{Fore.RESET} scaling)')
            print("Armors:")
            for armor in player.armors:
                print(f'- {Fore.RED}{armor} {Fore.RESET}(Def: {Fore.RED}{self.armors[armor]["defence"]}{Fore.RESET},'
                    f' {Fore.RED}{self.armors[armor]["weight"]}{Fore.RESET})')
            print("Amulets:")
            for amulet in player.amulets:
                print(f'- {Fore.RED}{amulet} {Fore.RESET}(Add {Fore.RED}{self.amulets[amulet]["effect"]}{Fore.RESET} to '
                                f'{Fore.RED}{self.amulets[amulet]["stat"]}{Fore.RESET})')
            print("Rings:")
            for ring in player.rings:
                print(f'- {Fore.RED}{ring} {Fore.RESET}(Add {Fore.RED}{self.rings[ring]["effect"]}{Fore.RESET} to '
                                f'{Fore.RED}{self.rings[ring]["stat"]}{Fore.RESET})')
            print(f"\n1. Equip item\n2. {Fore.RED}Return{Fore.RESET}")
            while True:
                try:
                    choice = int(input(f"\n{Fore.YELLOW}What is your choice?: {Fore.RESET}"))
                except ValueError:
                    print(f"\n{Fore.RED}Please select a valid option.{Fore.RESET}")
                else:
                    break
            match choice:
                case 1:
                    self.equip_item(player)
                case 2:
                    return 0
                case _:
                    print(f"\n{Fore.RED}Please select a valid option.{Fore.RESET}")

    def equip_item(self, player):
        print(f"\n{Fore.GREEN}--- EQUIP ---{Fore.RESET}")
        print("\nWhat would you like to equip?")
        print(f'1. Weapon\n2. Armor\n3. Amulet\n4. Ring\n5. {Fore.RED}Return{Fore.RESET}')
        choice = None
        while choice not in list(range(1,6)):
            while True:
                try:
                    choice = int(input(f"\n{Fore.YELLOW}What do you choose?: {Fore.RESET}"))
                except ValueError:
                    print(f"\n{Fore.RED}Please select a valid option.{Fore.RESET}")
                else:
                    break
            match choice:
                case 1:
                    self.equip_weapon(player)
                case 2:
                    self.equip_armor(player)
                case 3:
                    self.equip_amulet(player)
                case 4:
                    self.equip_ring(player)
                case 5:
                    return 0
                case _:
                    print(f"\n{Fore.RED}Please select a valid option.{Fore.RESET}")

    def equip_weapon(self, player):
        print(f"\n{Fore.GREEN}--- WEAPONS ---{Fore.RESET}")
        i = 1
        for weapon in player.weapons:
            print(f"{i}. {Fore.RED}{weapon}{Fore.RESET} (Dmg: "
                f'{Fore.RED}{self.weapons[weapon]["damage"]}{Fore.RESET}, {Fore.RED}{self.weapons[weapon]["ability"]}{Fore.RESET} scaling)')
            i += 1
        print(f"{i}. {Fore.RED}Return{Fore.RESET}")
        choice = None
        while choice not in list(range(1,i + 1)):
            while True:
                try:
                    choice = int(input(f"\n{Fore.YELLOW}What is your choice?: {Fore.RESET}"))
                except ValueError:
                    print(f"\n{Fore.RED}Please select a valid option.{Fore.RESET}")
                else:
                    break
            if choice == i:
                print(f"\n{Fore.RED}No weapon chosen.{Fore.RESET}")
                return 0
            else:
                chosen_weapon = player.weapons[choice - 1]
                player.weapons.append(player.eq_weapon["weapon_name"])
                player.weapons.remove(chosen_weapon)
                player.eq_weapon = self.weapons[chosen_weapon]
                print(f"\n{Fore.GREEN}--- EQUIP SUCCESS ---")
                print(f"\nEquipped {Fore.RED}{chosen_weapon}{Fore.GREEN}.{Fore.RESET}")
        return 0

    def equip_armor(self, player):
        print(f"\n{Fore.GREEN}--- ARMOR ---{Fore.RESET}")
        i = 1
        for armor in player.armors:
            print(f"{i}. {Fore.RED}{armor}{Fore.RESET}"
                f' (Def: {Fore.RED}{self.armors[armor]["defence"]}{Fore.RESET}, {Fore.RED}{self.armors[armor]["weight"]}{Fore.RESET})')
            i += 1
        print(f"{i}. {Fore.RED}Return{Fore.RESET}")
        choice = None
        while choice not in list(range(1,i + 1)):
            while True:
                try:
                    choice = int(input(f"\n{Fore.YELLOW}What is your choice?: {Fore.RESET}"))
                except ValueError:
                    print(f"\n{Fore.RED}Please select a valid option.{Fore.RESET}")
                else:
                    break
            if choice == i:
                print(f"\n{Fore.RED}No armor chosen.{Fore.RESET}")
                return 0
            elif self.armors[player.armors[choice - 1]]["weight"] != player.armor_prof:
                print(f"\n{Fore.RED}You are not proficient in this type of armor.{Fore.RESET}")
                choice = None
            else:
                chosen_armor = player.armors[choice - 1]
                player.armors.append(player.eq_armor["armor_name"])
                player.armors.remove(chosen_armor)
                player.eq_armor = self.armors[chosen_armor]
                print(f"\n{Fore.GREEN}--- EQUIP SUCCESS ---")
                print(f"\nEquipped {Fore.RED}{chosen_armor}{Fore.GREEN}.{Fore.RESET}")
        return 0

    def equip_amulet(self, player):
        print(f"\n{Fore.GREEN}--- AMULETS ---{Fore.RESET}")
        i = 1
        for amulet in player.amulets:
            print(f'{i}. {Fore.RED}{amulet} {Fore.RESET}(Add {Fore.RED}{self.amulets[amulet]["effect"]}{Fore.RESET} '
                f'to {Fore.RED}{self.amulets[amulet]["stat"]}{Fore.RESET})')
            i += 1
        print(f"{i}. {Fore.RED}Return{Fore.RESET}")
        choice = None
        while choice not in list(range(1,i + 1)):
            while True:
                try:
                    choice = int(input(f"\n{Fore.YELLOW}What is your choice: {Fore.RESET}"))
                except ValueError:
                    print(f"\n{Fore.RED}Please select a valid option.{Fore.RESET}")
                else:
                    break
            if choice == i:
                print(f"\n{Fore.RED}No amulet chosen.{Fore.RESET}")
                return 0
            else:
                chosen_amulet = player.amulets[choice - 1]
                self.stat_change(player, player.eq_amulet, self.amulets[chosen_amulet])
                player.amulets.append(player.eq_amulet["name"])
                player.amulets.remove(chosen_amulet)
                player.eq_amulet = self.amulets[chosen_amulet]
                print(f"\n{Fore.GREEN}--- EQUIP SUCCESS ---")
                print(f"\nEquipped {Fore.RED}{chosen_amulet}{Fore.GREEN}.{Fore.RESET}")
        return 0

    def equip_ring(self, player):
        print(f"\n{Fore.GREEN}--- RINGS ---{Fore.RESET}")
        i = 1
        for ring in player.rings:
            print(f'{i}. {Fore.RED}{ring}{Fore.RESET} (Add {Fore.RED}{self.rings[ring]["effect"]} '
                f'{Fore.RESET}to {Fore.RED}{self.rings[ring]["stat"]}{Fore.RESET})')
            i += 1
        print(f"{i}. {Fore.RED}Return{Fore.RESET}")
        choice = None
        while choice not in list(range(1,i + 1)):
            while True:
                try:
                    choice = int(input(f"\n{Fore.YELLOW}What is your choice?: {Fore.RESET}"))
                except ValueError:
                    print(f"\n{Fore.RED}Please select a valid option.{Fore.RESET}")
                else:
                    break
            if choice == i:
                print(f"{Fore.RED}\nNo ring chosen.{Fore.RESET}")
                return 0
            else:
                chosen_ring = player.rings[choice - 1]
                choice2 = None
                print(f"\n{Fore.GREEN}--- REPLACE RING ---{Fore.RESET}")
                print(f'\n1. {Fore.RED}{player.eq_ring_1["name"]} {Fore.RESET}'
                    f'(Add {Fore.RED}{player.eq_ring_1["effect"]}{Fore.RESET} to {Fore.RED}{player.eq_ring_1["stat"]}{Fore.RESET})'
                    f'\n2. {Fore.RED}{player.eq_ring_2["name"]} {Fore.RESET}'
                    f'(Add {Fore.RED}{player.eq_ring_2["effect"]}{Fore.RESET} to {Fore.RED}{player.eq_ring_2["stat"]}{Fore.RESET})'
                    f'\n3. {Fore.RED}Return{Fore.RESET}')
                while choice2 not in [1, 2, 3]:
                    while True:
                        try:
                            choice2 = int(input(f"\n{Fore.YELLOW}What is your choice?: {Fore.RESET}"))
                        except ValueError:
                            print(f"\n{Fore.RED}Please select a valid option.{Fore.RESET}")
                        else:
                            break
                    match choice2:
                        case 1:
                            self.stat_change(player, player.eq_ring_1, self.rings[chosen_ring])
                            player.rings.append(player.eq_ring_1["name"])
                            player.eq_ring_1 = self.rings[chosen_ring]
                        case 2:
                            self.stat_change(player, player.eq_ring_2, self.rings[chosen_ring])
                            player.rings.append(player.eq_ring_2["name"])
                            player.eq_ring_2 = self.rings[chosen_ring]
                        case 3:
                            print(f"{Fore.RED}\nNo ring was swapped out.{Fore.RESET}")
                            return 0
                        case _:
                            print(f"\n{Fore.RED}Please select a valid option.{Fore.RESET}")
                player.rings.remove(chosen_ring)
                print(f"\n{Fore.GREEN}--- EQUIP SUCCESS ---")
                print(f"\nEquipped {Fore.RED}{chosen_ring}{Fore.GREEN}.{Fore.RESET}")
        return 0

    def stat_change(self, player, old_item, new_item):
        for i in range(0, len(old_item["stat"])):
            match old_item["stat"][i]:
                case "Strength":
                    player.strength -= old_item["effect"][i]
                case "Dexterity":
                    player.dexterity -= old_item["effect"][i]
                case "Willpower":
                    player.willpower -= old_item["effect"][i]
                case _:
                    continue
        for i in range(0, len(new_item["stat"])):
            match new_item["stat"][i]:
                case "Strength":
                    player.strength += new_item["effect"][i]
                case "Dexterity":
                    player.dexterity += new_item["effect"][i]
                case "Willpower":
                    player.willpower += new_item["effect"][i]
                case _:
                   continue

    def loot_boss(self, player, boss):
        for item in boss.loot:
            print(f"\nYou loot {Fore.RED}{item}{Fore.RESET}!")
            if item in self.amulets:
                player.amulets.append(item)
            elif item in self.rings:
                player.rings.append(item)
            elif item in self.armors:
                player.armors.append(item)
            else:
                player.weapons.append(item)
        return 0
