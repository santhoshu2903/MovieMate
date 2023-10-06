import tkinter as tk
from tkinter import ttk
import sqlite3

# Function to retrieve movie data from the database
def fetch_movies(search_term=""):
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()
    
    # Query to retrieve movie data based on the search term
    query = f"SELECT * FROM movies WHERE name LIKE ?"
    cursor.execute(query, ('%' + search_term + '%',))
    
    movies = cursor.fetchall()
    conn.close()
    return movies

def insert_movies(tree, search_term=""):
    tree.delete(*tree.get_children())  # Clear existing entries
    
    movies = fetch_movies(search_term)
    for movie in movies:
        tree.insert('', 'end', values=movie)

def search_movies():
    search_term = search_entry.get()
    insert_movies(tree, search_term)

# Create a Tkinter window
root = tk.Tk()
root.title("Movie List")

# Create a Treeview widget
tree = ttk.Treeview(root, columns=("Name", "Date", "Time", "Seats", "Price"), show="headings")
tree.heading("Name", text="Movie Name")
tree.heading("Date", text="Date")
tree.heading("Time", text="Time")
tree.heading("Seats", text="Seats")
tree.heading("Price", text="Price")
tree.pack()

# Create a search box
search_label = tk.Label(root, text="Search Movie:")
search_label.pack()
search_entry = tk.Entry(root)
search_entry.pack()
search_button = tk.Button(root, text="Search", command=search_movies)
search_button.pack()

# Insert movie data into the Treeview
insert_movies(tree)

root.mainloop()
