#!/usr/bin/env python
"""A Class-based model of a coffee shop showing how to manage
the grinding of coffee beans.

The "Shop" class makes a new coffee shop object.
The "Shelf" class makes a shelf object for a shop.
The "Grinder" class makes a grinder object for a shop.
"""

import random


class Shop(object):
    """A class that creates coffee shop objects to contain a shelf and grinder
    
    Attributes:
    money -- integer of how many dollars you have to spend
    shelf -- the Shelf object within the shop
    grinder -- the Grinder object within the shop
    Methods:
    service_grinder -- spend 40 dollars to service grinder
    """
    def __init__(self, money=200):
        """Create a new Shop object
        
        Keyword arguments:
        money -- starting integer dollars, default is 200
        """
        self.money = money
        self.shelf = Shelf(self)   # automatically creates its own shelf
        self.grinder = Grinder(self)   # and grinder as well
    
    def service_grinder(self):
        """Zero out grinder's grinds_since_service
        
        Input no arguments
        """
        if self.money - 40 < 0:
            raise ValueError("You are broke")
        else:
            self.money -= 40
            self.grinder.grinds_since_service = 0


class Shelf(object):
    """A class that creates shelf object for a shop
    
    Attributes:
    shop -- the shop that the shelf belongs to
    inventory -- the total number of bags of coffee on the shelf
    first_shelf -- the number of bags on the first shelf
    second_shelf -- the number of bags on the second shelf
    third_shelf -- the number of bags on the third shelf
    Methods:
    set_shelves -- place the inventory on the three shelves
    restock -- buy a quantity of wholesale coffee bags for the shelf
    sell -- make a sale to a customer
    """
    def __init__(self, shop, inventory=15):
        """Create a new Shelf object
        
        Positional arguments:
        shop -- the shop object that this shelf belongs to
        Keyword arguments:
        inventory -- the integer number of bags of coffee to start out, default is 15
        """
        if inventory not in range(16):   # shelf is capped at 15
            raise ValueError("Must have 15 bags or less")
        else:
            self.shop = shop
            self.inventory = inventory
            self.set_shelves()

    def set_shelves(self):
        """Convert inventory to shelf quantities

        Input no arguments
        """
        self.first_shelf = min(5, self.inventory)   # first shelf is bottom shelf
        self.second_shelf = max(min(5, self.inventory - 5), 0)   # upper shelves get the remainder
        self.third_shelf = max(min(5, self.inventory - 10), 0)
    
    def restock(self, quantity=1):
        """Buy a quantity of wholesale coffee bags for 5 dollars each

        Keyword arguments:
        quantity -- integer number of coffee bags to buy, default is 1
        """
        if self.inventory + quantity > 15:   # shelf is capped at 15
            raise ValueError("You are over capacity")
        elif self.shop.money - 5 * quantity < 0:
            raise ValueError("You are broke")
        else:
            self.inventory += quantity
            self.shop.money -= 5 * quantity
            self.set_shelves()
    
    def sell(self, quantity=1):
        """Make a sale to a customer for 8 dollars a bag. About half of
        the customers will randomly want ground coffee.

        Keyword arguments:
        quantity -- integer number of coffee bags to sell, default is 1
        """
        if self.inventory - quantity < 0:
            raise ValueError("You are out of stock")
        else:
            wants_ground = random.randrange(2)   # randomly choose 0 or 1
            if wants_ground:
                self.shop.grinder.grind(quantity)   # utilizes store's grinder
            self.inventory -= quantity
            self.shop.money += 8 * quantity
            self.set_shelves()


class Grinder(object):
    """A class that creates coffee grinder object for a shop
    
    Attributes:
    shop -- the shop that the grinder belongs to
    grinds_since_service -- the number of grinds since last service
    Methods:
    grind -- grind sold coffee and add to grinds_since_service
    """
    def __init__(self, shop):
        """Create a new Grinder object

        Positional arguments:
        shop -- the shop object that this grinder belongs to
        """
        self.shop = shop
        self.grinds_since_service = 0
    
    def grind(self, quantity=1):
        """Grind a customer's coffee and add to grinds_since_service.
        A grinder will stop working after 20 grinds without servicing.

        Keyword arguments:
        quantity -- integer number of coffee bags to grind, default is 1
        """
        if self.grinds_since_service >= 20:   # do not complete sale for grind requests
            raise ValueError("Grinder needs service")
        else:
            self.grinds_since_service += quantity