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

# Saves all items, loans, and the next available ID to the JSON file
def save_data():
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

    with open("BorrowingAssister/data.json", "w") as file:
        json.dump(data, file, indent=4)

# Loads items and loans from the JSON file when the program starts
def load_data():
    global next_id

    try:
        with open("BorrowingAssister/data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        return  # No file exists yet, so the program starts with empty lists

    items.clear()
    loans.clear()

    next_id = data.get("next_id", 1)

    # Recreate Item objects from the saved dictionaries
    for item_data in data.get("items", []):
        item = Item(
            item_data["id"],
            item_data["name"],
            item_data["category"]
        )

        items.append(item)

    # Recreate Loan objects from the saved dictionaries
    for loan_data in data.get("loans", []):
        item = find_item_by_id(loan_data["item_id"])

        if item is None:
            continue

        borrow_date = datetime.datetime.fromisoformat(
            loan_data["borrow_date"]
        )

        due_date = datetime.datetime.fromisoformat(
            loan_data["due_date"]
        )

        if loan_data["return_date"] is None:
            return_date = None
        else:
            return_date = datetime.datetime.fromisoformat(
                loan_data["return_date"]
            )

        loan = Loan(
            item,
            loan_data["borrower"],
            borrow_date,
            due_date
        )

        loan.return_date = return_date

        loans.append(loan)