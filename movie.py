import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class MovieTable(tk.Frame):
    def __init__(self, parent, columns, movie_list, on_image_click):
        super().__init__(parent)
        self.parent = parent
        self.tree = ttk.Treeview(self, columns=columns, show='headings', selectmode='browse')

        # Set column headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center', width=100)

        # Add a vertical scrollbar
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        # Pack the treeview and scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # Populate the treeview with movie data
        self.populate_treeview(movie_list)

        # Event handler for treeview selection
        self.tree.bind("<ButtonRelease-1>", self.on_treeview_select)

        # Callback function for image click
        self.on_image_click = on_image_click

    def populate_treeview(self, movie_list):
        for movie in movie_list:
            # Assuming the last column is for images
            values = movie[:-1]
            image_path = movie[-1]
            
            # Open and resize the image
            image = Image.open(image_path)
            image = image.resize((50, 50), Image.ANTIALIAS)

            # Convert the image to PhotoImage
            image = ImageTk.PhotoImage(image)

            # Insert the values and image into the treeview
            item = self.tree.insert("", "end", values=values, image=image)

            # Save a reference to the image to prevent it from being garbage collected
            self.tree.image_references = getattr(self.tree, 'image_references', {})
            self.tree.image_references[item] = image

    def on_treeview_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            # Get the movie details associated with the selected item
            movie_details = self.tree.item(selected_item)["values"]
            # Call the callback function with the movie details
            self.on_image_click(movie_details)

class MovieDetailsFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Label to display movie details
        self.details_label = tk.Label(self, text="", font=("Helvetica", 12))
        self.details_label.pack(padx=10, pady=10)

    def update_details(self, movie_details):
        # Update the label with movie details
        details_text = "\n".join([f"{key}: {value}" for key, value in zip(["Title", "Genre", "Year"], movie_details)])
        self.details_label.config(text=details_text)

def main():
    root = tk.Tk()
    root.title("Movie Table Example")

    # Example movie data (replace with your data)
    columns = ["Title", "Genre", "Year", "Image"]
    movie_list = [
        ("Movie 1", "Action", 2020, "path/to/image1.jpg"),
        ("Movie 2", "Comedy", 2021, "path/to/image2.jpg"),
        ("Movie 3", "Drama", 2019, "path/to/image3.jpg"),
    ]

    # Create MovieDetailsFrame
    details_frame = MovieDetailsFrame(root)
    details_frame.pack(side="right", fill="both", expand=True)

    # Callback function for image click
    def on_image_click(movie_details):
        details_frame.update_details(movie_details)

    # Create and pack the MovieTable
    movie_table = MovieTable(root, columns, movie_list, on_image_click)
    movie_table.pack(fill="both", expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()
