import tkinter as tk
from PIL import Image, ImageTk

class MovieApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie List")

        # Sample movie data (replace this with your own data)
        self.top_trending_movies = [
            {"title": "Trending 1", "image_path": "images/title1.jpg", "details": "Details 1"},
            {"title": "Trending 2", "image_path": "images/title2.jpg", "details": "Details 2"},
            {"title": "Trending 3", "image_path": "images/title1.jpg", "details": "Details 3"},
            # Add more top trending movie data as needed
        ]

        self.upcoming_movies = [
            {"title": "Upcoming 1", "image_path": "images/title1.jpg", "details": "Details 1"},
            {"title": "Upcoming 2", "image_path": "images/title2.jpg", "details": "Details 2"},
            {"title": "Upcoming 3", "image_path": "images/title1.jpg", "details": "Details 3"},
            # Add more upcoming movie data as needed
        ]

        self.recently_booked_movies = [
            {"title": "Booked 1", "image_path": "images/title1.jpg", "details": "Details 1"},
            {"title": "Booked 2", "image_path": "images/title2.jpg", "details": "Details 2"},
            {"title": "Booked 3", "image_path": "images/title1.jpg", "details": "Details 3"},
            # Add more recently booked movie data as needed
        ]

        # Create canvas and scrollbars
        self.canvas = tk.Canvas(root)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(root, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Display movies in each section
        self.display_movies(self.top_trending_movies, 0, "Top Movies")
        self.display_movies(self.upcoming_movies, 1, "Upcoming Movies")
        self.display_movies(self.recently_booked_movies, 2, "Recently Booked Movies")

    def display_movies(self, movies, row, label_text):
        col_width = 150  # Adjust this value to change the horizontal spacing
        row_height = 160
        x_scrollbar = tk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=self.canvas.xview)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Create a frame for each row
        frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, row * row_height), anchor=tk.NW, window=frame)

        # Add label for the section
        label = tk.Label(frame, text=label_text)
        label.grid(row=0, column=0, columnspan=len(movies), pady=5)

        for i, movie in enumerate(movies):
            image = Image.open(movie["image_path"])
            image = image.resize((100, 150), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            # Create a button with the image
            button = tk.Button(frame, image=photo, command=lambda i=i, r=row: self.show_movie_details(i, r))
            button.image = photo  # Keep a reference to avoid garbage collection

            # Add the button to the frame at the specified row and column
            button.grid(row=1, column=i, padx=5)

        # Configure the x-scrollbar to scroll the frame
        frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"), xscrollcommand=x_scrollbar.set)

        # Add space between each row
        self.canvas.create_rectangle(0, (row + 1) * row_height, self.canvas.winfo_width(), (row + 1) * row_height + 10, fill="white")

    def show_movie_details(self, index, row):
        # Replace this with your logic to display movie details
        if row == 0:
            movie = self.top_trending_movies[index]
        elif row == 1:
            movie = self.upcoming_movies[index]
        else:
            movie = self.recently_booked_movies[index]
        print(f"Row: {row}, Title: {movie['title']}\nDetails: {movie['details']}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieApp(root)
    root.mainloop()
