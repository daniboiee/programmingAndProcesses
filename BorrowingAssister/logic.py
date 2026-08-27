# Iteration 3

# This file holds the logic of the program

import datetime
from classes import Item, Loan

# Containers for items and loans
items = []
loans = []


# General utility functions

# Generates the first unused equipment ID
def generate_id():
    number = 1      # Future version will not reuse deleted item IDs, but I need JSON for that

    while True:
        item_id = f"EQ{number:03d}" # Formats the number as a (minimum) three-digit ID, e.g. EQ001, EQ002, EQ010, EQ1234

        if not any(item.id == item_id for item in items):
            return item_id

        number += 1

# Finds and returns an item using its ID
def find_item_by_id(item_id):
    for item in items:
        if item.id == item_id:
            return item

    return None