# Iteration 3

# This file holds the logic of the program

import json
import datetime

from classes import Item, Loan

# Containers for items and loans
items = []
loans = []
next_id = 1

# General utility functions

# Generates a permanently unique ID for a new item
def generate_id():
    global next_id

    item_id = f"EQ{next_id:03d}"

    next_id += 1

    return item_id

# Finds and returns an item using its ID
def find_item_by_id(item_id):
    for item in items:
        if item.id == item_id:
            return item

    return None

def save_data():    # Saves all items, loans, and the next available ID to the JSON file
    data = {
        "next_id": next_id,
        "items": [],
        "loans": []
    }

    # Convert each Item object into a dictionary that JSON can store
    for item in items:
        data["items"].append({
            "id": item.id,
            "name": item.name,
            "category": item.category
        })

    # Convert each Loan object into a dictionary that JSON can store
    for loan in loans:
        data["loans"].append({
            "item_id": loan.item.id,
            "borrower": loan.borrower,
            "borrow_date": loan.borrow_date.isoformat(),
            "due_date": loan.due_date.isoformat(),
            "return_date": (
                loan.return_date.isoformat()
                if loan.return_date is not None
                else None
            )
        })

    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)