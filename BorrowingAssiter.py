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

def pause():    # Only use in windows to reduce chance of having this happen twice
    input("\nPress Enter to continue...")

def generate_id():
    return f"EQ{len(items) + 1:03d}"    # :03d makes the number at least 3 digits, adding 0s if empty spaces

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
def add_item():
    clear_screen()

    print("ADD ITEM\n")

    name = input("Item name: ").strip()
    category = input("Category: ").strip()

    if name == "" or category == "":
        print("\nItem name and category cannot be empty.")
        pause()
        return

    item_id = generate_id()

    new_item = Item(item_id, name, category)
    items.append(new_item)

    print(f"\nItem successfully added with ID {item_id}.")
    pause()

def edit_item():
    clear_screen()

    print("EDIT ITEM\n")

    item = find_item()

    if item is None:
        pause()
        return

    print(f"\nEditing: {item.name}")

    new_name = input(f"New name (press Enter to keep '{item.name}'): ").strip()

    new_category = input(f"New category (press Enter to keep '{item.category}'): ").strip()

    if new_name != "":
        item.name = new_name

    if new_category != "":
        item.category = new_category

    print("\nItem successfully updated.")
    pause()
    
def delete_item():
    clear_screen()

    print("DELETE ITEM\n")

    item = find_item()

    if item is None:
        pause()
        return

    if not item.is_available:
        print("\nThis item is currently borrowed.")
        print("It cannot be deleted until it has been returned.")
        pause()
        return

    confirmation = input(
        f"\nAre you sure you want to delete {item.name}? (y/n): "
    ).strip().lower()

    if confirmation == "y":
        items.remove(item)
        print("\nItem successfully deleted.")
    else:
        print("\nDeletion cancelled.")

    pause()

def main():
    choice = None
    while choice != "4":
        clear_screen()

        print("CLASSROOM EQUIPMENT TRACKER\n")
        print("1. Add item")
        print("2. Edit item")
        print("3. Delete item")
        print("4. Exit\n")

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

        elif choice != "4":
            print("Invalid option.")
            pause()

main()