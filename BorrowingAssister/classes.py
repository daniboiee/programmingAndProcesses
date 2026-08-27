# Iteration 3

# This file holds the two custom classes for this program

import datetime

# Class that holds information about an item
class Item:
    # Example usage: item1 = Item("EQ001", "FX9860GII Calculator", "Calculator")
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category

    # Returns the item's details as a formatted string
    def get_details(self):
        return f"{self.id}: {self.name} ({self.category})"

    # Finds and returns the item's current loan if it is borrowed
    def find_active_loan(self, loans):
        for loan in loans:
            if loan.item == self and loan.return_date is None:
                return loan

        return None

# Class that holds information about the loan of an item
class Loan:
    # Example usage: loan1 = Loan(item1, "James", datetime.datetime.now(), datetime.datetime(2026, 8, 31))
    def __init__(self, item, borrower, borrow_date, due_date):
        self.item = item
        self.borrower = borrower
        self.borrow_date = borrow_date
        self.due_date = due_date
        self.return_date = None

    # Returns the loan's details as a formatted string
    def get_details(self):
        return (
            f"{self.item.name} borrowed by {self.borrower}, "
            f"due {self.due_date.strftime('%d/%m/%Y')}"
        )

    # Records the item as returned and prevents it from being returned twice
    def return_item(self):
        if self.return_date is not None:
            return False

        self.return_date = datetime.datetime.now()
        return True