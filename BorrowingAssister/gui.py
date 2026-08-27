# Iteration 3

# This file holds all GUI of the program

import tkinter as tk
from tkinter import messagebox
import datetime

from classes import Item, Loan
import logic


# Colour/font constants

# Colours
BG_COLOUR = "#F2F2F2"
BUTTON_COLOUR = "#D9D9D9"
TEXT_COLOUR = "#222222"

# Fonts
TITLE_FONT = ("Arial", 16, "bold")
NORMAL_FONT = ("Arial", 10)


# Utility functions for GUI-related things

# Applies the standard font and colours to a widget
def style_widget(widget):
    widget.config(
        font=NORMAL_FONT,
        bg=BG_COLOUR,
        fg=TEXT_COLOUR)
    return widget

# Populates the item list with a given set of items (used by both full refresh and search)
def populate_item_list(item_iterable, empty_message):
    item_list.delete(0, tk.END)

    results = list(item_iterable)

    if len(results) == 0:
        item_list.insert(tk.END, empty_message)
        return

    for item in results:
        loan = item.find_active_loan(logic.loans)

        if loan is None:
            status = "Available"
        elif loan.is_overdue():
            status = f"OVERDUE - {loan.borrower}"
        else:
            status = f"Borrowed by {loan.borrower}"

        item_list.insert(
            tk.END,
            f"{item.id} | {shorten_text(item.name)} | {shorten_text(item.category)} | {status}"
        )

# Refreshes the item list shown in the main window
def refresh_item_list():
    populate_item_list(logic.items, "No items.")

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

# Centers a window over the main window
def center_window(window, width, height):
    root.update_idletasks()

    x = root.winfo_x() + (root.winfo_width() - width) // 2
    y = root.winfo_y() + (root.winfo_height() - height) // 2

    window.geometry(
        f"{width}x{height}+{x}+{y}"
    )

# Shortens text for display without changing the actual value
def shorten_text(text, length=35):
    if len(text) > length:
        return text[:length - 3] + "..."

    return text

# Enables or disables item-related buttons
def update_button_states():
    if len(logic.items) == 0:
        edit_button.config(state="disabled")
        delete_button.config(state="disabled")
        borrow_button.config(state="disabled")
        return_button.config(state="disabled")

    else:
        edit_button.config(state="normal")
        delete_button.config(state="normal")
        borrow_button.config(state="normal")
        return_button.config(state="normal")

def search_items():
    search_term = search_entry.get().strip().lower()

    matches = [
        item for item in logic.items
        if search_term in item.id.lower()
        or search_term in item.name.lower()
        or search_term in item.category.lower()
    ]

    populate_item_list(matches, "No matching items.")

def clear_search():
    search_entry.delete(0, tk.END)
    refresh_item_list()


# Windows

# Opens the window used to add a new item
def add_item_window():
    window = tk.Toplevel(root)
    window.title("Add Item")
    window.resizable(False, False)

    center_window(window, 265, 140)

    def add():
        name = name_entry.get().strip().replace("\n", " ").replace("\r", " ")
        category = category_entry.get().strip().replace("\n", " ").replace("\r", " ")
    
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
        refresh_item_list()
        update_button_states()  # If no items existed previously, enable edit, delete, borrow, and return buttons
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

    style_widget(
    tk.Button(window,
        text="Add",
        command=add
    )).grid(row=2, column=0, padx=10, pady=20)

    style_widget(
    tk.Button(window,
        text="Cancel",
        command=window.destroy
    )).grid(row=2, column=1, padx=10, pady=20)

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
        new_name = name_entry.get().strip().replace("\n", " ").replace("\r", " ")
        new_category = category_entry.get().strip().replace("\n", " ").replace("\r", " ")

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

    style_widget(
    tk.Button(window,
        text="Save",
        command=save_changes
    )).grid(row=3, column=0, padx=10, pady=20)

    style_widget(
    tk.Button(window,
        text="Cancel",
        command=window.destroy
    )).grid(row=3, column=1, padx=10, pady=20)

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

    style_widget(
    tk.Button(
        window,
        text="Borrow",
        command=borrow
    )).grid(row=3, column=0, padx=10, pady=20)

    style_widget(
    tk.Button(
        window,
        text="Cancel",
        command=window.destroy
    )).grid(row=3, column=1, padx=10, pady=20)


# Non-windows (don't have TopLevel)

# Deletes the selected item after checking that it is not currently borrowed
def on_delete_click():
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
        refresh_item_list()
        update_button_states()  # If no items exist anymore, disable edit, delete, borrow, and return buttons
        logic.save_data()

        messagebox.showinfo(
            "Deleted",
            "Item successfully deleted.",
            parent=root
        )

        refresh_item_list()

# Returns the selected item after confirming its loan
def on_return_click(): 
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
        f"Item: {shorten_text(item.name, 50)}\n"
        f"Borrowed by: {loan.borrower}\n"
        f"Due: {loan.due_date.strftime('%d/%m/%Y')}\n\n"
        f"Return this item?",
        parent=root
    )

    if confirmation:
        logic.return_item(item)
        logic.save_data()

        messagebox.showinfo(
            "Returned",
            "The item has been successfully returned.",
            parent=root
        )
        refresh_item_list()


# Main window

def start_gui():
    global root, item_list, search_entry
    global edit_button, delete_button, borrow_button, return_button

    root = tk.Tk()
    root.title("Equipment Tracker")
    root.geometry("520x490")
    root.resizable(False, False)

    # Displays the title of the application
    title_label = tk.Label(root,
        text="Equipment Tracker",
        font=TITLE_FONT,
        bg=BG_COLOUR,
        fg=TEXT_COLOUR
    )

    title_label.grid(
        row=0,
        column=0,
        columnspan=2,
        pady=15
    )

    # Search bar
    search_frame = tk.Frame(root)
    search_frame.grid(
        row=1, 
        column=0, 
        columnspan=2, 
        pady=(0, 10)
    )

    search_entry = tk.Entry(search_frame, width=40)
    search_entry.grid(row=0, column=0, padx=5)
    search_entry.bind("<Return>", lambda event: search_items())   # Enter key triggers search

    style_widget(
    tk.Button(search_frame,
        text="Search",
        command=search_items
    )).grid(row=0, column=1, padx=5)

    style_widget(
    tk.Button(search_frame, 
        text="Clear", 
        command=clear_search
    )).grid(row=0, column=2, padx=5)

    # Displays the list of equipment items and their current status
    item_list = tk.Listbox(root,
        width=80,
        height=15
    )
    item_list.grid(row=2, column=0, columnspan=2, padx=15, pady=10)


    # Buttons
    
    add_item = style_widget(
        tk.Button(root,
        text="Add Item",
        width=15,
        command=add_item_window))
    add_item.grid(row=3, column=0, padx=5, pady=5)

    edit_button = style_widget(
        tk.Button(root,
        text="Edit Item",
        width=15,
        command=edit_item_window))
    edit_button.grid(row=3, column=1, padx=5, pady=5)

    delete_button = style_widget(
        tk.Button(root,
        text="Delete Item",
        width=15,
        command=on_delete_click))
    delete_button.grid(row=4, column=0, padx=5, pady=5)

    borrow_button = style_widget(
        tk.Button(root,
        text="Borrow Item",
        width=15,
        command=borrow_item_window))
    borrow_button.grid(row=4, column=1, padx=5, pady=5)

    return_button = style_widget(
        tk.Button(root,
        text="Return Item",
        width=15,
        command=on_return_click))
    return_button.grid(row=5, column=0, padx=5, pady=5)

    # Exit button
    style_widget(tk.Button(root,
        text="Exit",
        width=15,
        command=root.destroy,
        font=NORMAL_FONT,
        bg=BG_COLOUR,
        fg=TEXT_COLOUR
    )).grid(row=5, column=1, padx=5, pady=5)

    # Displays current list of items on program start
    refresh_item_list()
    # Button states are enabled or disabled based on whether list is empty
    update_button_states()

    root.mainloop()