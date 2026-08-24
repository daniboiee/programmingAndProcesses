# WARNING
# This version of the program doesn't work.
# The GUI has not been implemented to a level high enough that it's usable in this version.

# Iteration 2

import tkinter as tk
from tkinter import messagebox
import datetime

# Classes

# Class that holds information about an item
# Example usage: item1 = Item("EQ001", "FX9860GII Calculator", "Calculator")
class Item:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category

    # Example usage: print(item1.get_details())
    def get_details(self):
        return f"{self.id}: {self.name} ({self.category})"

    def find_active_loan(self, loans): # Finds the current loan for an item
        for loan in loans:
            if loan.item == self and loan.return_date is None:
                return loan

        return None

# Class that holds information about one loan
# Example usage: loan1 = Loan(item1, "James", datetime.datetime.now(), datetime.datetime(2026, 8, 31))
class Loan:
    def __init__(self, item, borrower, borrow_date, due_date):
        self.item = item
        self.borrower = borrower
        self.borrow_date = borrow_date
        self.due_date = due_date
        self.return_date = None

    # Example usage: loan1.get_details()
    def get_details(self):
        return (
            f"{self.item.name} borrowed by {self.borrower}, "
            f"due {self.due_date.strftime('%d/%m/%Y')}"
        )

    # Example usage: item1.return_item()
    def return_item(self):
        if self.return_date is not None:
            print("This loan has already been returned.")
            return False

        self.return_date = datetime.datetime.now()
        print("The loan has been successfully returned.")
        return True

# Containers for items and loans
items = []
loans = []

# General utility functions
def clear_screen():
    print("\n" * 40)

def pause():    # Only use in windows/frames to reduce chance of having this happen twice
    input("\nPress Enter to continue...")

def generate_id():  # Finds the first unused ID
    number = 1      # Future version will not reuse deleted item IDs, but I need JSON for that

    while True:
        item_id = f"EQ{number:03d}" # :03d makes the number at least 3 digits, adding 0s if empty spaces

        if not any(item.id == item_id for item in items):
            return item_id

        number += 1

def find_item():    # Checks items[] and returns the item that has the input ID
    if len(items) == 0:
        print("There are currently no items.")
        return None

    print("\nAvailable items:")
    for item in items:
        print(item.get_details())

    item_id = input("\nEnter the ID of the item: ").strip().upper()

    for item in items:
        if item.id == item_id:
            return item

    print("No item with that ID was found.")
    return None

def refresh_item_list():    # Updates the list shown in the main window
    item_list.delete(0, tk.END)

    if len(items) == 0:
        item_list.insert(tk.END, "No items.")

    else:
        for item in items:
            loan = item.find_active_loan(loans)

            if loan is None:
                status = "Available"
            else:
                status = f"Borrowed by {loan.borrower}"

            item_list.insert(
                tk.END,
                f"{item.id} | {item.name} | {item.category} | {status}"
            )


# Windows

def add_item_window(): # Adds items to items[]
    clear_screen()

    print("ADD ITEM\n")

    name = input("Item name: ").strip()
    category = input("Category: ").strip()

    if name == "" or category == "":    # Might be better to check name and category separately when they are input
        print("\nItem name and category cannot be empty.")
        pause()
        return

    item_id = generate_id()

    new_item = Item(item_id, name, category)    # Creates item based on input details
    items.append(new_item)      # Adds item to items[]

    print(f"\nItem successfully added with ID {item_id}.")
    pause()

def edit_item_window():    # Changes details about items
    clear_screen()

    print("EDIT ITEM\n")

    item = find_item()

    if item is None:
        pause()
        return

    print(f"\nEditing: {item.name}")

    new_name = input(f"New name (press Enter to keep '{item.name}'): ").strip()

    new_category = input(f"New category (press Enter to keep '{item.category}'): ").strip()

    if new_name != "":      # In other words, if they just pressed enter, don't change the aspects
        item.name = new_name

    if new_category != "":
        item.category = new_category

    print("\nItem successfully updated.")
    pause()
    
def delete_item_window():  # Removes items from items[]
    clear_screen()

    print("DELETE ITEM\n")

    item = find_item()

    if item is None:
        pause()
        return

    # Check whether this item already has an active loan
    if item.find_active_loan(loans) is not None:    # Also helps user experience, loans are not forgotten
        print("\nThis item is already borrowed.")
        print("It cannot be deleted until it has been returned.")
        pause()
        return

    confirmation = input(f"\nAre you sure you want to delete {item.name}? (y/n): ").strip().lower()

    if confirmation == "y":
        items.remove(item)
        print("\nItem successfully deleted.")
    else:
        print("\nDeletion cancelled.")

    pause()

def borrow_item_window():
    clear_screen()

    print("BORROW ITEM\n")

    days = 0    # Initialises a value for the while loop
    item = find_item()

    if item is None:
        pause()
        return

    # Check whether this item already has an active loan
    if item.find_active_loan(loans) is not None:
        print("\nThis item is already borrowed.")
        pause()
        return

    borrower = input("Borrower's name: ").strip()

    if borrower == "":
        print("\nBorrower's name cannot be empty.")
        pause()
        return

    while days <= 0:    # Keep asking for a day until a proper number is input
        try:
            days = int(input("Number of days until due: "))

            if days <= 0:
                print("Please enter a positive number.")
                continue

        except ValueError:
            print("Please enter a whole number.")

    borrow_date = datetime.datetime.now()
    due_date = borrow_date + datetime.timedelta(days=days)

    new_loan = Loan(item, borrower, borrow_date, due_date)

    loans.append(new_loan)

    print(
        f"\nItem has been successfully borrowed by {borrower}, "
        f"and will be due on {due_date.strftime('%d/%m/%Y')}."
    )

    pause()

def return_item_window():
    clear_screen()

    print("RETURN ITEM\n")

    item = find_item()

    if item is None:
        pause()
        return

    loan = item.find_active_loan(loans)

    if loan is None:
        print("\nThis item is not currently borrowed.")
        pause()
        return

    print(f"\nItem: {item.name}")
    print(f"Borrowed by: {loan.borrower}")
    print(f"Due date: {loan.due_date.strftime('%d/%m/%Y')}")

    confirmation = input("\nReturn this item? (y/n): ").strip().lower()

    if confirmation == "y":
        loan.return_item()
    else:
        print("Return cancelled.")

    pause()


# Main window

root = tk.Tk()
root.title("Classroom Equipment Tracker")
root.geometry("700x450")


title_label = tk.Label(
    root,
    text="CLASSROOM EQUIPMENT TRACKER",
    font=("Arial", 16)
)

title_label.grid(
    row=0,
    column=0,
    columnspan=2,
    pady=15
)


# List of items
item_list = tk.Listbox(
    root,
    width=80,
    height=15
)

item_list.grid(
    row=1,
    column=0,
    columnspan=2,
    padx=15,
    pady=10
)


# Buttons
tk.Button(root,
    text="Add Item",
    width=15,
    command=add_item_window
).grid(row=2, column=0, padx=5, pady=5)

tk.Button(root,
    text="Edit Item",
    width=15,
    command=edit_item_window
).grid(row=2, column=1, padx=5, pady=5)

tk.Button(root,
    text="Delete Item",
    width=15,
    command=delete_item_window
).grid(row=3, column=0, padx=5, pady=5)

tk.Button(root,
    text="Borrow Item",
    width=15,
    command=borrow_item_window
).grid(row=3, column=1, padx=5, pady=5)

tk.Button(root,
    text="Return Item",
    width=15,
    command=return_item_window
).grid(row=4, column=0, padx=5, pady=5)

tk.Button(root,
    text="Exit",
    width=15,
    command=root.destroy
).grid(row=4, column=1, padx=5, pady=5)

# Initial display
refresh_item_list()

root.mainloop