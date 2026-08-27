# Iteration 3

# This file holds all GUI of the program

import tkinter as tk
from tkinter import messagebox
import datetime

from classes import Item, Loan
import logic

# Utility functions for GUI-related things

# Refreshes the item list shown in the main window
def refresh_item_list():
    item_list.delete(0, tk.END)

    if len(logic.items) == 0:
        item_list.insert(tk.END, "No items.")

    else:
        for item in logic.items:
            loan = item.find_active_loan(logic.loans)

            if loan is None:
                status = "Available"
            else:
                status = f"Borrowed by {loan.borrower}"

            item_list.insert(
                tk.END,
                f"{item.id} | {item.name} | {item.category} | {status}"
            )

# Returns the item currently selected in the list
def get_selected_item():
    selection = item_list.curselection()

    if not selection:
        messagebox.showwarning("No item selected", "Please select an item.", parent=root)
        return None

    selected_text = item_list.get(selection[0])

    if selected_text == "No items.":
        return None

    item_id = selected_text.split(" | ")[0] # Accesses the ID data stored in the string

    return logic.find_item_by_id(item_id)

# Centres a window over the main window
def center_window(window, width, height):
    root.update_idletasks()

    x = root.winfo_x() + (root.winfo_width() - width) // 2
    y = root.winfo_y() + (root.winfo_height() - height) // 2

    window.geometry(
        f"{width}x{height}+{x}+{y}"
    )


# Windows

# Opens the window used to add a new item
def add_item_window():
    window = tk.Toplevel(root)
    window.title("Add Item")
    window.resizable(False, False)

    center_window(window, 265, 140)

    def add():
        name = name_entry.get().strip()
        category = category_entry.get().strip()
    
        if name == "":
            messagebox.showerror(
                "Invalid input",
                "Item name cannot be empty.",
                parent=window
            )
            return
    
        if category == "":
            messagebox.showerror(
                "Invalid input",
                "Category cannot be empty.",
                parent=window
            )
            return
    
        item_id = logic.generate_id()
    
        new_item = Item(item_id, name, category)
        logic.items.append(new_item)
        logic.save_data()
    
        messagebox.showinfo(
            "Item added",
            f"Item successfully added with ID {item_id}.",
            parent=window
        )
    
        refresh_item_list()
        window.destroy()

    tk.Label(window, text="Item Name").grid(
        row=0, column=0, padx=10, pady=10, sticky="w"
    )

    name_entry = tk.Entry(window, width=25)
    name_entry.grid(
        row=0, column=1, padx=10, pady=10
    )

    tk.Label(window, text="Category").grid(
        row=1, column=0, padx=10, pady=10, sticky="w"
    )

    category_entry = tk.Entry(window, width=25)
    category_entry.grid(
        row=1, column=1, padx=10, pady=10
    )

    tk.Button(window,
        text="Add",
        command=add
    ).grid(row=2, column=0, padx=10, pady=20)

    tk.Button(window,
        text="Cancel",
        command=window.destroy
    ).grid(row=2, column=1, padx=10, pady=20)

# Opens the window used to edit an existing item
def edit_item_window():
    item = get_selected_item()

    if item is None:
        return

    window = tk.Toplevel(root)
    window.title("Edit Item")
    window.resizable(False, False)

    center_window(window, 290, 190)

    def save_changes():
        new_name = name_entry.get().strip()
        new_category = category_entry.get().strip()

        if new_name == "":
            messagebox.showerror(
                "Invalid input",
                "Item name cannot be empty.",
                parent=window
            )
            return

        if new_category == "":
            messagebox.showerror(
                "Invalid input",
                "Category cannot be empty.",
                parent=window
            )
            return

        item.name = new_name
        item.category = new_category
        logic.save_data()

        messagebox.showinfo(
            "Updated",
            "Item successfully updated.",
            parent=window
        )

        refresh_item_list()
        window.destroy()
        
    tk.Label(window, text=f"Editing: {item.name}").grid(
        row=0, column=0, columnspan=2, pady=10
    )

    tk.Label(window, text="New Name").grid(
        row=1, column=0, padx=10, pady=10, sticky="w"
    )

    name_entry = tk.Entry(window, width=25)
    name_entry.insert(0, item.name)
    name_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(window, text="New Category").grid(
        row=2, column=0, padx=10, pady=10, sticky="w"
    )

    category_entry = tk.Entry(window, width=25)
    category_entry.insert(0, item.category)
    category_entry.grid(row=2, column=1, padx=10, pady=10)

    tk.Button(window,
        text="Save",
        command=save_changes
    ).grid(row=3, column=0, padx=10, pady=20)

    tk.Button(window,
        text="Cancel",
        command=window.destroy
    ).grid(row=3, column=1, padx=10, pady=20)

# Opens the window used to borrow an item
def borrow_item_window():
    item = get_selected_item()

    if item is None:
        return

    if item.find_active_loan(logic.loans) is not None:
        messagebox.showerror(
            "Cannot borrow",
            "This item is already borrowed.",
            parent=root
        )
        return

    window = tk.Toplevel(root)
    window.title("Borrow Item")
    window.resizable(False, False)

    center_window(window, 295, 180)

    def borrow():
        borrower = borrower_entry.get().strip()

        if borrower == "":
            messagebox.showerror(
                "Invalid input",
                "Borrower's name cannot be empty.",
                parent=window
            )
            return

        try:
            days = int(days_entry.get())

            if days <= 0:
                raise ValueError
            
        except ValueError:
            messagebox.showerror(
                "Invalid input",
                "Days must be a positive whole number.",
                parent=window
            )
            return
        
        try:
            borrow_date = datetime.datetime.now()
            due_date = borrow_date + datetime.timedelta(days=days)

        except OverflowError:
            messagebox.showerror(
                "Invalid input",
                "Input value is too large.",
                parent=window
            )
            return

        new_loan = Loan(
            item,
            borrower,
            borrow_date,
            due_date
        )

        logic.loans.append(new_loan)
        logic.save_data()

        messagebox.showinfo(
            "Borrowed",
            f"{item.name} has been borrowed by {borrower}.\n"
            f"Due: {due_date.strftime('%d/%m/%Y')}",
            parent=window
        )

        refresh_item_list()
        window.destroy()
        
    tk.Label(window,
        text=f"Borrowing: {item.name}"
    ).grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(window, text="Borrower's name").grid(
        row=1, column=0, padx=10, pady=10, sticky="w"
    )

    borrower_entry = tk.Entry(window, width=25)
    borrower_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(window, text="Days until due").grid(
        row=2, column=0, padx=10, pady=10, sticky="w"
    )

    days_entry = tk.Entry(window, width=25)
    days_entry.grid(row=2, column=1, padx=10, pady=10)

    tk.Button(
        window,
        text="Borrow",
        command=borrow
    ).grid(row=3, column=0, padx=10, pady=20)

    tk.Button(
        window,
        text="Cancel",
        command=window.destroy
    ).grid(row=3, column=1, padx=10, pady=20)


# Non-windows (don't have TopLevel)

# Deletes the selected item after checking that it is not currently borrowed
def delete_item():
    item = get_selected_item()

    if item is None:
        return

    if item.find_active_loan(logic.loans) is not None:
        messagebox.showerror(
            "Cannot delete",
            "This item is currently borrowed.",
            parent=root
        )
        return

    confirmation = messagebox.askyesno(
        "Delete Item",
        f"Are you sure you want to delete {item.name}?",
        parent=root
    )

    if confirmation:
        logic.items.remove(item)
        logic.save_data()

        messagebox.showinfo(
            "Deleted",
            "Item successfully deleted.",
            parent=root
        )

        refresh_item_list()

# Returns the selected item after confirming its loan
def return_item(): 
    item = get_selected_item()

    if item is None:
        return

    loan = item.find_active_loan(logic.loans)

    if loan is None:
        messagebox.showerror(
            "Cannot return",
            "This item is not currently borrowed.",
            parent=root
        )
        return

    confirmation = messagebox.askyesno(
        "Return Item",
        f"Item: {item.name}\n"
        f"Borrowed by: {loan.borrower}\n"
        f"Due: {loan.due_date.strftime('%d/%m/%Y')}\n\n"
        f"Return this item?",
        parent=root
    )

    if confirmation:
        loan.return_item()
        logic.save_data()

        messagebox.showinfo(
            "Returned",
            "The loan has been successfully returned.",
            parent=root
        )

        refresh_item_list()


# Main window

def start_gui():
    global root, item_list
    root = tk.Tk()
    root.title("Equipment Tracker")
    root.geometry("520x450")
    root.resizable(False, False)

    # Displays the title of the application
    title_label = tk.Label(root,
        text="Equipment Tracker",
        font=("Arial", 16)
    )

    title_label.grid(
        row=0,
        column=0,
        columnspan=2,
        pady=15
    )

    # Displays the list of equipment items and their current status
    item_list = tk.Listbox(root,
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
        command=delete_item
    ).grid(row=3, column=0, padx=5, pady=5)

    tk.Button(root,
        text="Borrow Item",
        width=15,
        command=borrow_item_window
    ).grid(row=3, column=1, padx=5, pady=5)

    tk.Button(root,
        text="Return Item",
        width=15,
        command=return_item
    ).grid(row=4, column=0, padx=5, pady=5)

    tk.Button(root,
        text="Exit",
        width=15,
        command=root.destroy
    ).grid(row=4, column=1, padx=5, pady=5)

    # Displays current list of items on program start
    refresh_item_list()

    root.mainloop()