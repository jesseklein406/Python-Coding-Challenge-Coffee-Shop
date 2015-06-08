#!/usr/bin/env python
"""A Class-based model of a coffee shop showing how to manage
the grinding of coffee beans.

The "Shop" class
"""

import random


class Shop(object):
    def __init__(self, money=200):
        self.money = money
        self.shelf = Shelf(self)
        self.grinder = Grinder(self)
    
    def service_grinder(self):
        if self.money - 40 < 0:
            raise ValueError("You are broke")
        else:
            self.money -= 40
            self.grinder.grinds_since_service = 0


class Shelf(object):
    def __init__(self, shop, inventory=15):
        if inventory not in range(16):
            raise ValueError("Must have 15 bags or less")
        else:
            self.shop = shop
            self.inventory = inventory
            self.set_shelves()

    def set_shelves(self):
        self.first_shelf = min(5, self.inventory)
        self.second_shelf = max(min(5, self.inventory - 5), 0)
        self.third_shelf = max(min(5, self.inventory - 10), 0)
    
    def restock(self, quantity=1):
        if self.inventory + quantity > 15:
            raise ValueError("You are over capacity")
        elif self.shop.money - 5 * quantity < 0:
            raise ValueError("You are broke")
        else:
            self.inventory += quantity
            self.shop.money -= 5 * quantity
            self.set_shelves()
    
    def sell(self, quantity=1):
        if self.inventory - quantity < 0:
            raise ValueError("You are out of stock")
        else:
            wants_ground = random.randrange(2)
            if wants_ground:
                self.shop.grinder.grind(quantity)
            self.inventory -= quantity
            self.shop.money += 8 * quantity
            self.set_shelves()


class Grinder(object):
    def __init__(self, shop, grinds_since_service=0):
        self.shop = shop
        self.grinds_since_service = grinds_since_service
    
    def grind(self, quantity=1):
        if self.grinds_since_service >= 20:
            raise ValueError("Grinder needs service")
        else:
            self.grinds_since_service += quantity