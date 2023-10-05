import tkinter as tk
from tkcalendar import DateEntry

def get_selected_date():
    selected_date = cal.get_date()
    date_entry.delete(0, tk.END)  # Clear the current entry text
    date_entry.insert(0, selected_date)

root = tk.Tk()
root.title("Calendar Entry Example")

date_entry = DateEntry(root, width=12, background="darkblue", foreground="white", date_pattern="dd/MM/yyyy")
date_entry.pack(padx=10, pady=10)

calendar_button = tk.Button(root, text="Calendar", command=get_selected_date)
calendar_button.pack(pady=10)

root.mainloop()
