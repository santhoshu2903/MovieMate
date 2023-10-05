import tkinter as tk
from tkinter import ttk

def get_selected_time():
    selected_hour = hour_combobox.get()
    selected_minute = minute_combobox.get()
    selected_ampm = ampm_combobox.get()
    selected_time = f"{selected_hour}:{selected_minute} {selected_ampm}"
    time_label.config(text=f"Selected Time: {selected_time}")

root = tk.Tk()
root.title("Custom Time Input Example")

# Create Comboboxes for hours, minutes, and AM/PM selection
hour_combobox = ttk.Combobox(root, values=["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"])
hour_combobox.set("01")  # Set the default hour
hour_combobox.config(width=5)
hour_combobox.pack(side='left')

minute_combobox = ttk.Combobox(root, values=["00", "15", "30", "45"])
minute_combobox.set("00")  # Set the default minute
minute_combobox.config(width=5)
minute_combobox.pack(side='left')

ampm_combobox = ttk.Combobox(root, values=["AM", "PM"])
ampm_combobox.set("AM")  # Set the default AM/PM
ampm_combobox.config(width=5)
ampm_combobox.pack(side='left')

# Create a button to get the selected time
get_time_button = tk.Button(root, text="Get Selected Time", command=get_selected_time)
get_time_button.pack(pady=10)

# Create a label to display the selected time
time_label = tk.Label(root, text="", font=("Arial", 12))
time_label.pack(pady=10)

root.mainloop()
