import json
from functions.character_class_functions import Character

load_consumables = open('jsons/consumables.json')
consumables = json.load(load_consumables)

class Potion():
    def __init__(self,
                 name: str,
                 stat: str,
                 rec: int,
                 val: int
                 ):
                self.name = name
                self.stat = stat
                self.rec = rec
                self.val = val

def __str__(self):
    return self.name

def generate_potions(consumables):
    potions = []
    for potion in consumables:
        pot = Potion(potion["potion_name"], potion["stat"], potion["recover"], potion["value"])
        potions.append(pot)
    return potions

def shopping_for_potions(player: Character):
    print('\nYou enter a potion store, and see the following selection:\n1. Lesser Health Potion (10g)'
          '\n2. Health Potion (50g)\n3. Greater Health Potion (200g)\n4. Lesser Mana Potion (10g)\n5. Mana Potion (50g)'
          '\n6. Greater Mana Potion (200g)\n7. Return')
    potions = generate_potions(consumables)
    player_choice = None
    while True:
        while True:
            try:
                player_choice = int(input("\nYour gold: " + str(player.gold) + ".\nWhat would you like to buy?: "))
            except ValueError:
                print("\nPlease select a valid number!")
            else:
                break
        if player_choice == 7:
            print("\nYou leave the potions store.")
            return 0
        pot = potions[player_choice - 1]
        if player.gold < pot.val:
            print("\nUnfortunately, you cannot afford this item right now.")
        elif pot.name in player.potions:
            print("\nYou already have this item, and cannot carry more.")
        else:
            print("\nYou succesfully purchase this item.")
            print(f"\n{pot.name} has been added to your inventory.")
            player.potions.append(pot.name)
            player.gold -= pot.val
        print('\nYou have the following selection:\n1. Lesser Health Potion (10g)'
                  '\n2. Health Potion (50g)\n3. Greater Health Potion (200g)\n4. Lesser Mana Potion (10g)\n5. Mana Potion (50g)'
                  '\n6. Greater Mana Potion (200g)\n7. Return')
    return 0


def use_potions(player: Character):
    potions = generate_potions(consumables)
    did_drink = False
    i = 1
    # prints all the potions
    print('\nYou have the following in your inventory: ')
    for potion in player.potions:
        print(str(i) + '. ' + potion)
        i += 1
    print(str(i) + '. Return')
    #
    player_choice = None
    while player_choice not in range(0, len(player.potions) + 1):
        player_choice = int(input("What is your choice?: ")) - 1
        if player_choice == len(player.potions):
            return did_drink
        else:
            pot = None
            for potion in potions:
               if potion.name == player.potions[player_choice]:
                   pot = potion
            if pot.stat == 'health':
                player.health = min(player.health + pot.rec, player.max_health)
                print(f"\nYou consume the {pot.name} bringing your health up to {player.health}.")
            else:
                player.mana = min(player.mana + pot.rec, player.max_mana)
                print(f"\nYou consume the {pot.name} bringing your mana up to {player.mana}.")
            player.potions.remove(pot.name)
            did_drink = True
    return did_drink
