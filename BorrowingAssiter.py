import datetime

class Item:
    def __init__(self, id, name, category, borrower, borrow_date, due_date, is_available):
        self.id = id
        self.name = name
        # etc
        # maybe is_available is decided by the existence of a due and borrow date?

    def get_details(self):
        print("")

    def borrow(self):
        if self.is_available == False:
            print("")
            return
        self.borrow_date = datetime.datetime.now()
        # probably should make it so you can pick whether you want the date to be .now()
        self.is_available == False

    def return_item(self):
        if self.is_avilable:
            print("")
            return
        # reset borrower borrow date and due date
        self.is_available = True

        

now = datetime.datetime.now()
print(now)