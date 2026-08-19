import datetime

# Class that holds all items and all borrowing information for items
# Example usage: item1 = Item("EQ001", "Casio FX9860GII Graphic Calculator", "Calculator")
class Item:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category
        self.borrower = None
        self.borrow_date = None
        self.due_date = None
        self.is_available = True

    # Example usage: print(item1.get_details())
    def get_details(self):
        return f"{self.id}: {self.name} ({self.category})"

    # Example usage: item1.borrow("James", datetime.datetime(2026, 8, 18))
    def borrow(self, borrower, due_date):
        if not self.is_available:
            print("This item is already borrowed.")
            return

        self.borrower = borrower
        self.borrow_date = datetime.datetime.now()
        self.due_date = due_date
        self.is_available = False
        print(f"Item has been succesfully borrowed by {borrower}, and will be due on {due_date}.")

    # Example usage: item1.return_item()
    def return_item(self):
        if self.is_available:
            print("This item is not currently borrowed.")
            return

        self.borrower = None
        self.borrow_date = None
        self.due_date = None
        self.is_available = True
        print(f"Item has been succesfully returned.")

# Containers for items
items = []

# General utility functions
def clear_screen():
    print("\n" * 40)

def pause():
    input("\nPress Enter to continue...")

def generate_id():
    return f"EQ{len(items) + 1:03d}"

def find_item():
    if len(items) == 0:
        print("There are currently no items.")
        return None

    print("\nAvailable items:")
    for item in items:
        print(item.get_details())

    item_id = input("\nEnter the ID of the item: ").strip()

    for item in items:
        if item.id == item_id:
            return item

    print("No item with that ID was found.")
    return None

# Windows
def add_item():
    print()

def edit_item():
    print()
    
def delete_item():
    print()

def main():
    while choice != 4:
        clear_screen()

        print("CLASSROOM EQUIPMENT TRACKER\n")
        print("1. Add item")
        print("2. Edit item")
        print("3. Delete item")
        print("4. Exit\n")

        choice = input("Select an option: ").strip()

        if choice == "1":
            add_item()

        elif choice == "2":
            edit_item()

        elif choice == "3":
            delete_item()

        elif choice != "4":
            print("Invalid option.")
            pause()