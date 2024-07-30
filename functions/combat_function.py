import random
import time
import json

from colorama import Fore

from functions.character_class_functions import Character
from functions.character_inspection import list_abilities
from functions.creature_class_functions import Creature
from functions.potion_class_functions import use_potions

def combat_time(player: Character, enemy: Creature):
    flight = False
    while enemy.health > 0 and player.health > 0:

        # print some useful statistics
        print(f"\n{Fore.RED}--- COMBAT STATS ---{Fore.RESET}")
        print(f'\n{enemy.name} health: {enemy.health}')
        print(f'Your health: {player.health}')
        print(f'Your mana: {player.mana}')
        print(f"\n{Fore.RED}--- COMBAT ACTIONS ---{Fore.RESET}")
        print("\n1. Attack with a Weapon\n2. Use a spell or ability\n3. Use a Potion\n4. Attempt to Hide\n5. Attempt to Flee")
        # check if enemy spots the player
        if player.stealth:
            enemy.spot_player(player)
        # prompt player action
        while True:
            try:
                action_choice = int(input(f"\n{Fore.YELLOW}What is your choice?: {Fore.RESET}"))
            except ValueError:
                print(f"\n{Fore.RED}Please select a valid option.{Fore.RESET}")
            else:
                break
        match action_choice:
            case 1:
                # player strikes at the opponent
                player.deal_damage_to_enemy(enemy)
                # if the player is stealthed they get a free attack
                if enemy.health > 0 and not player.stealth:
                    enemy.deal_damage_to_player(player)                    # the player is revealed from stealth after their attack
                if player.stealth:
                    print(f"\n{Fore.RED}--- STEALTH CANCELLED ---")
                    print(f'\nYou are spotted again, and are no longer hidden or invisible.{Fore.RESET}')
                    player.stealth = False
            case 2:
                player_abilities(player, enemy)
                if player.stealth:
                    print(f"\n{Fore.RED}--- STEALTH CANCELLED ---")
                    print(f'\nYou are spotted again, and are no longer hidden or invisible.{Fore.RESET}')
                    player.stealth = False
            case 3:
                pot = use_potions(player)
                if pot:
                    print(f'\n{Fore.RED}--- ATTACK OF OPPORTUNITY ---')
                    print(f"\n{enemy.name} tries to attack you while you consume a potion and...{Fore.RESET}")
                    check = random.randint(0, 100)
                    time.sleep(1)
                    if check < 65:
                        print(f"{Fore.GREEN}\n...misses!{Fore.RESET}")
                    else:
                        print(f"{Fore.RED}\n...manages to hit!{Fore.RESET}")
                        enemy.deal_damage_to_player(player)
            case 4:
                player.attempt_stealth_in_combat(enemy)
            case 5:
                flight = player.fleeing_combat(enemy)
                if flight:
                    break
            case _:
                print(f"\n{Fore.RED}Please select a valid option.{Fore.RESET}")

    # decide if fight is over, and appropriately reward the player
    combat_succesful = False

    if player.health <= 0:
        print(f"{Fore.RED}\n--- DEFEAT ---")
        print(f'\nYou have been defeated and faint!{Fore.RESET}')
    elif flight:
        return combat_succesful
    elif enemy.health <= 0:
        combat_succesful = True
        print(f"{Fore.GREEN}\n--- COMBAT SUCCESS ---")
        print(f'\nYou have defeated your foe and gained {enemy.xp} XP.{Fore.RESET}')
        if enemy.gold != 0:
            print(f"{Fore.GREEN}\n--- LOOT ---")
            print(f'\nYou loot {enemy.gold} gold.{Fore.RESET}')
            player.gold += enemy.gold
        player.current_xp += enemy.xp

    return combat_succesful



def player_abilities(player: Character, enemy: Creature):
    load_abilities = open('jsons/abilities.json')
    abilities = json.load(load_abilities)
    ability = list_abilities_combat(player, abilities)
    if ability == 0:
        return 0
    elif ability == "Shield" or ability == "Parry" or ability == "Dodge":
        print(f"\n{Fore.BLUE}--- ABILITY ---{Fore.RESET}")
        print(f"\nYou {random.choice(abilities[ability]["moveset"])}")
        player.deal_damage_to_enemy(enemy)
    elif ability == "God's Abandon" or ability == "Surrounded by Ruins" or ability == "Apotheosis":
        if player.strength >= player.willpower and player.strength >= player.dexterity:
            abilities[ability]["attribute"] = "strength"
        elif player.dexterity >= player.willpower:
            abilities[ability]["attribute"] = "dexterity"
        else:
            abilities[ability]["attribute"] = "willpower"
        parse_ability(player, enemy, ability, abilities)
    else:
        parse_ability(player, enemy, ability, abilities)

def list_abilities_combat(player: Character, abilities: list):
    print(f'\n{Fore.BLUE}--- ABILITIES ---{Fore.RESET}')
    print('You have the following abilities available:')
    i = 1
    for ability in player.abilities:
        print(f'{i}. {Fore.BLUE}{ability}{Fore.RESET} (Cost: {Fore.BLUE}{abilities[ability]["cost"]}{Fore.RESET}, Dmg/Heal: {Fore.RED}{abilities[ability]["cost"]}{Fore.RESET})')
        i += 1
    print(f"{i}. {Fore.RED}Return{Fore.RESET}")
    choice = None
    while choice not in list(range(1, i + 1)):
        while True:
            try:
                choice = int(input(f"\n{Fore.YELLOW}What is your choose?: {Fore.RESET}"))
            except ValueError:
                print(f"\n{Fore.RED}Please select a valid option.{Fore.RESET}")
            else:
                break
        if choice == i:
            print(f"\n{Fore.RED}No ability was chosen.{Fore.RESET}")
            return 0
        if player.mana < abilities[player.abilities[choice - 1]]["cost"]:
            print(f"{Fore.RED}\nYou have insufficient mana to use this ability{Fore.RESET}")
        else:
            return player.abilities[choice - 1]

def parse_ability(player: Character, enemy: Creature, ability: str, abilities: dict):
    enemy_hits = True if random.randint(0, 100) > 60 else False
    is_heal = True if abilities[ability]["type"] == "heal" else False
    if is_heal:
        print(f"\n{Fore.BLUE}--- HEAL ---{Fore.RESET}")
        player.mana = max(player.mana - abilities[ability]["cost"], 0)
        player.health = min(player.max_health, player.health + abilities[ability]["effect"])
        print(f'\nYou {random.choice(abilities[ability]["moveset"])}.')
        print(f'You recover {Fore.RED}{random.choice(abilities[ability]["effect"])}{Fore.RESET} HP.')
    elif not is_heal:
        player.mana = max(player.mana - abilities[ability]["cost"], 0)
        dmg = None
        match abilities[ability]["attribute"]:
            case "strength":
                dmg = random.randint(1, player.strength)
            case "dexterity":
                dmg = random.randint(1, player.dexterity)
            case "willpower":
                dmg = random.randint(1, player.willpower)
        enemy.health -= abilities[ability]["effect"] + dmg
        print(f"\n{Fore.BLUE}--- ABILITY ---{Fore.RESET}")
        print(f'\nYou {random.choice(abilities[ability]["moveset"])} dealing {abilities[ability]["effect"] + dmg} damage.')
    if enemy.health > 0 and enemy_hits:
        enemy.deal_damage_to_player(player)
    if not enemy_hits:
        print(f"\n{Fore.GREEN}--- ENEMY STAGGER ---{Fore.RESET}")
        print(f"\nThe enemy struggles from the attack, and fails to retalliate.")
