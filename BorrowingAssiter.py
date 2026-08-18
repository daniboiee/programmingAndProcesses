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