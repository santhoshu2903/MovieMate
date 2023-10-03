import tkinter as tk

def perform_search():
    search_query = search_entry.get()
    # Replace this with your search logic and get a list of results
    # For this example, we'll use a dummy list of results
    results = ["Result 1", "Result 2", "Result 3"]

    # Clear previous results
    results_listbox.delete(0, tk.END)

    # Display new search results in the Listbox
    for result in results:
        results_listbox.insert(tk.END, result)

def on_result_click(event):
    # Get the selected item from the Listbox
    selected_index = results_listbox.curselection()

    if selected_index:
        selected_item = results_listbox.get(selected_index[0])
        result_label.config(text=f"Selected: {selected_item}")
        result_label.pack(padx=10, pady=10)  # Display the result label when a result is clicked

# Create the main window
root = tk.Tk()
root.title("Clickable Search Results")

# Create a label for the search bar
search_label = tk.Label(root, text="Search:")
search_label.pack(padx=10, pady=10)

# Create an Entry widget for the search input
search_entry = tk.Entry(root, width=40)
search_entry.pack(padx=10, pady=10)

# Create a Button widget for performing the search
search_button = tk.Button(root, text="Search", command=perform_search)
search_button.pack(padx=10, pady=10)

# Create a Listbox widget to display search results
results_listbox = tk.Listbox(root, width=40, height=10)
results_listbox.pack(padx=10, pady=10)

# Bind a function to handle result clicks
results_listbox.bind("<ButtonRelease-1>", on_result_click)

# Create a label to display the selected result (initially hidden)
result_label = tk.Label(root, text="", font=("Arial", 12))

# Run the main loop
root.mainloop()
