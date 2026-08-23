# Iteration 2

import datetime

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


# Windows
def add_item(): # Adds items to items[]
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

def edit_item():    # Changes details about items
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
    
def delete_item():  # Removes items from items[]
    clear_screen()

    print("DELETE ITEM\n")

    item = find_item()

    if item is None:
        pause()
        return

    # To avoid problems with loans pointing to non-existent items in the future
    if not item.is_available:   # Also helps user experience, loans are not forgotten
        print("\nThis item is currently borrowed.")
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

def borrow_item():
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

    while days > 0:    # Keep asking for a day until a proper number is input
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

def return_item():
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


def main():
    choice = None
    while choice != "7":
        clear_screen()

        print("CLASSROOM EQUIPMENT TRACKER\n")
        print("1. Add item")
        print("2. Edit item")
        print("3. Delete item")
        print("4. Borrow item")
        print("5. Return item")
        print("6. Save (not working)")
        print("7. Exit\n")

        choice = input("Select an option: ").strip()

        if choice == "1":
            add_item()
            continue
        elif choice == "2":
            edit_item()
            continue
        elif choice == "3":
            delete_item()
            continue
        elif choice == "4":
            borrow_item()
            continue
        elif choice == "5":
            return_item()
            continue
        elif choice != "7":
            print("Invalid option.")
            pause()

main()