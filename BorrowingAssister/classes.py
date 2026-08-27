# Final version

# This file holds the two custom classes for this program

import datetime

# Class that holds information about an item
class Item:
    # Example usage: item1 = Item("EQ001", "FX9860GII Calculator", "Calculator")
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category

    # Finds and returns the item's current loan if it is borrowed
    def find_active_loan(self, loans):
        for loan in loans:
            if loan.item == self:
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

    # Checks whether this loan is currently overdue
    def is_overdue(self):
        return datetime.datetime.now() > self.due_date