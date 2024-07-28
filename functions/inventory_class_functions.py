import json
import random

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
            print('\n1. List Equipped Items'
                '\n2. List and Equip items from inventory'
                '\n3. Return')
            while True:
                try:
                    choice = int(input("\nWhat do you select?: "))
                except ValueError:
                    print("Not a valid choice!")
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
                    print("Please select a valid choice.")

    def list_equipped(self, player):
        print("\n--- Currently equipped ---")
        print(f"Weapon: {player.eq_weapon["weapon_name"]} "
            f"(Dmg: {player.eq_weapon["damage"]})")
        print(f'Armor: {player.eq_armor["armor_name"]} '
            f'({player.eq_armor["weight"]}, '
            f'Def: {player.eq_armor["defence"]})')
        print(f'Amulet: {player.eq_amulet["name"]} '
                f'(Add {player.eq_amulet["effect"]} to '
                    f'{player.eq_amulet["stat"] or None})')
        print(f'Ring 1: {player.eq_ring_1["name"]} '
                f'(Add {player.eq_ring_1["effect"]} to '
                    f'{player.eq_ring_1["stat"] or None})')
        print(f'Ring 2: {player.eq_ring_2["name"]} '
                f'(Add {player.eq_ring_2["effect"]} to '
                    f'{player.eq_ring_2["stat"] or None})')
        print("--------------------------")

    def list_inventory(self, player):
        print("\n--- Your inventory contains the following ---")
        print("Weapons:")
        for weapon in player.weapons:
            print("- " + weapon + f" (Dmg: {self.weapons[weapon]["damage"]})")
        print("Armors:")
        for armor in player.armors:
            print("- " + armor + f" ({self.armors[armor]["weight"]}, "
                    f"Def: {self.armors[armor]["defence"]})")
        print("Amulets:")
        for amulet in player.amulets:
            print("- " + amulet + f" (Add {self.amulets[amulet]["effect"]} to "
                            f"{self.amulets[amulet]["stat"]})")
        print("Rings:")
        for ring in player.rings:
            print("- " + ring + f" (Add {self.rings[ring]["effect"]} to "
                            f"{self.rings[ring]["stat"]})")
        print("---------------------------------------------")
        choice = None
        while choice != 2:
            while True:
                try:
                    choice = int(input("\n1. Equip item\n2. Return\n\n"
                        "What is your choice?: "))
                except ValueError:
                    print("\nPlease select a valid choice.")
                else:
                    break
            match choice:
                case 1:
                    self.equip_item(player)
                case 2:
                    return 0
                case _:
                    print("Please select a valid action.")

    def equip_item(self, player):
        print("\nWhat would you like to equip?")
        print("1. Weapon\n2. Armor\n3. Amulet\n4. Ring\n5. Return")
        choice = None
        while choice not in list(range(1,6)):
            while True:
                try:
                    choice = int(input("\nWhat do you choose?: "))
                except ValueError:
                    print("Please select a valid input.")
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
                    print("\nPlease select a valid action.")

    def equip_weapon(self, player):
        print("\nWhich weapon to equip?")
        i = 1
        for weapon in player.weapons:
            print(f"{i}. " + weapon + f" (Dmg: {self.weapons[weapon]["damage"]})")
            i += 1
        print(f"{i}. Return")
        choice = None
        while choice not in list(range(1,i + 1)):
            while True:
                try:
                    choice = int(input("\nWeapon to equip: "))
                except ValueError:
                    print("\nPlease select a valid input.")
                else:
                    break
            if choice == i:
                print("\nNo weapon chosen.")
                return 0
            else:
                chosen_weapon = player.weapons[choice - 1]
                player.weapons.append(player.eq_weapon["weapon_name"])
                player.weapons.remove(chosen_weapon)
                player.eq_weapon = self.weapons[chosen_weapon]
                print(f"\nEquipped {chosen_weapon}.")
        return 0

    def equip_armor(self, player):
        print("\nWhich armor to equip?")
        i = 1
        for armor in player.armors:
            print(f"{i}. " + armor +
                f" ({self.armors[armor]["weight"]}, "
                f"Def: {self.armors[armor]["defence"]})")
            i += 1
        print(f"{i}. Return")
        choice = None
        while choice not in list(range(1,i + 1)):
            while True:
                try:
                    choice = int(input("\nArmor to equip: "))
                except ValueError:
                    print("\nPlease select a valid input.")
                else:
                    break
            if choice == i:
                print("\nNo armor chosen.")
                return 0
            elif self.armors[player.armors[choice - 1]]["weight"] != player.armor_prof:
                print("\nYou are not proficient in this type of armor.")
                choice = None
            else:
                chosen_armor = player.armors[choice - 1]
                player.armors.append(player.eq_armor["armor_name"])
                player.armors.remove(chosen_armor)
                player.eq_armor = self.armors[chosen_armor]
                print(f"\nEquipped {chosen_armor}.")
        return 0

    def equip_amulet(self, player):
        print("\nWhich amulet to equip?")
        i = 1
        for amulet in player.amulets:
            print(f"{i}. " + amulet +
                f" (Add {self.amulets[amulet]["effect"]} "
                f"to {self.amulets[amulet]["stat"]})")
            i += 1
        print(f"{i}. Return")
        choice = None
        while choice not in list(range(1,i + 1)):
            while True:
                try:
                    choice = int(input("\nAmulet to equip: "))
                except ValueError:
                    print("\nPlease select a valid input.")
                else:
                    break
            if choice == i:
                print("\nNo amulet chosen.")
                return 0
            else:
                chosen_amulet = player.amulets[choice - 1]
                self.stat_change(player, player.eq_amulet, self.amulets[chosen_amulet])
                player.amulets.append(player.eq_amulet["name"])
                player.amulets.remove(chosen_amulet)
                player.eq_amulet = self.amulets[chosen_amulet]
                print(f"\nEquipped {chosen_amulet}.")
        return 0

    def equip_ring(self, player):
        print("\nWhich ring to equip?")
        i = 1
        for ring in player.rings:
            print(f"{i}. " + ring +
                f" (Add {self.rings[ring]["effect"]} "
                f"to {self.rings[ring]["stat"]})")
            i += 1
        print(f"{i}. Return")
        choice = None
        while choice not in list(range(1,i + 1)):
            while True:
                try:
                    choice = int(input("\nRing to equip: "))
                except ValueError:
                    print("\nPlease select a valid input.")
                else:
                    break
            if choice == i:
                print("\nNo ring chosen.")
                return 0
            else:
                chosen_ring = player.rings[choice - 1]
                choice2 = None
                print(f"1. {player.eq_ring_1["name"]} "
                    f"(Add {player.eq_ring_1["effect"]} to {player.eq_ring_1["stat"]})"
                    f"\n2. {player.eq_ring_2["name"]}"
                    f"(Add {player.eq_ring_2["effect"]} to {player.eq_ring_2["stat"]})"
                    f"\n3. Return")
                while choice2 not in [1, 2, 3]:
                    while True:
                        try:
                            choice2 = int(input("\nWhich ring would you like to swap?: "))
                        except ValueError:
                            print("Please choose a valid input.")
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
                            print("No ring was swapped out.")
                            return 0
                        case _:
                            print("Please select a valid choice.")
                player.rings.remove(chosen_ring)
                print(f"\nEquipped {chosen_ring}.")
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
            print(f"You loot {item}!")
            if item in self.amulets:
                player.amulets.append(item)
            elif item in self.rings:
                player.rings.append(item)
            elif item in self.armors:
                player.armors.append(item)
            else:
                player.weapons.append(item)
        return 0
