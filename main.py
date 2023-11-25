import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from fpdf import FPDF
from tkcalendar import Calendar, DateEntry
from tkinter import filedialog
from tkinter import font
import mysql.connector
from datetime import datetime
from time import strftime
from PIL import Image, ImageTk
import sv_ttk
import random
from ttkthemes import ThemedTk
import pyqrcode
from fpdf import FPDF
from datetime import datetime
# users_db_path=os.path.join(os.getcwd(), "users.db")
# bookings_db_path=os.path.join(os.getcwd(), "bookings.db")
# movies_db_path=os.path.join(os.getcwd(), "movies.db")

mysql_database = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'port': 3306,
    'database': 'showtime'
}


def init_db():
    # Connect to the MySQL server
    conn = mysql.connector.connect(**mysql_database)
    cursor = conn.cursor()
    


    # Create the 'movies' table
    cursor.execute("""CREATE TABLE IF NOT EXISTS movies (
        movie_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        release_date DATE NOT NULL,
        trending boolean default 0,
        date DATE NOT NULL,
        time TIME NOT NULL,
        seats INT NOT NULL,
        price FLOAT NOT NULL,
        movie_image_path VARCHAR(255)
    );""")

    # Create the 'users' table
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255),
        firstname VARCHAR(255),
        lastname VARCHAR(255),
        role VARCHAR(255) default "user",
        password VARCHAR(255),
        gmail VARCHAR(255)
    );""")

        # Create the 'bookings' table
    cursor.execute("""CREATE TABLE IF NOT EXISTS bookings (
        booking_id INT AUTO_INCREMENT PRIMARY KEY,
        movie_id INT NOT NULL,
        user_id INT NOT NULL default 0,
        agent_mail VARCHAR(255),
        username VARCHAR(255),
        gmail VARCHAR(255),
        no_of_seats INT NOT NULL,
        total_price FLOAT NOT NULL,
        foreign key (movie_id) references movies(movie_id),
        foreign key (user_id) references users(user_id)
    );""")

    # Commit and close the connection
    conn.commit()
    conn.close()



class ShowTime:
    def __init__(self):
        super().__init__()
        self.root=ThemedTk(theme="adapta")
        self.root.title("Welcome to CMU Movie ticket management system")
        self.root.geometry("800x600")
        self.show_homepage()
        # sv_ttk.set_theme("light")
        self.trending_movie=[]
        self.all_movies=[]
        self.upcoming_movies=[]
        self.extract_movies()

        # # Create a custom style for the Treeview
        self.style = ttk.Style()
        # self.style.theme_use("alt")
        self.style.configure("Treeview",
                        font=("Helvetica", 12),
                        rowheight=25,  # Adjust row height as needed
                        fieldbackground="lightgray")  # Background color

        # Add column lines
        self.style.layout("Treeview.Heading", [
            ("Treeheading.cell", {'sticky': 'nswe'}),
            ("Treeheading.border", {'sticky': 'nswe', 'children': [
                ("Treeheading.padding", {'sticky': 'nswe', 'children': [
                    ("Treeheading.image", {'side': 'right', 'sticky': ''}),
                    ("Treeheading.text", {'sticky': 'nswe'}),
                ]}),
            ]}),
        ])


    def extract_movies(self):
        #extract movies from database into all movies
        # Connect to the MySQL server
        conn = mysql.connector.connect(**mysql_database)
        cursor = conn.cursor()
        #get all movies
        cursor.execute("SELECT * FROM movies")
        self.all_movies=cursor.fetchall()
        #get trending movies from movie trending column
        cursor.execute("SELECT * FROM movies WHERE trending=1")
        self.trending_movie=cursor.fetchall()
        #get upcomming movies from movie id's from release date greater than today  
        self.upcoming_movies=[]
        for movie in self.all_movies:
            # print(movie[2],type(movie[2]))
            # print(datetime.today().strftime('%Y-%m-%d'),type(datetime.today().date()))
            if movie[2]>datetime.today().date():
                self.upcoming_movies.append(movie)

        # print("all movies",self.all_movies)
        # print("trending movies",self.trending_movie)
        # print("upcomming movies",self.upcomming_movies)
        #close connection
        conn.close()


    def show_homepage(self):
        self.clear_content()
        self.homepage=tk.Frame(self.root)
        self.homepage.config(bg="white")
        self.homepage.pack(fill="both", expand=True)
        self.homepage.grid_rowconfigure(0, weight=1)
        self.homepage.grid_columnconfigure(0, weight=1)

        self.homepage_label=tk.Label(self.homepage, text="Start Booking, It's", font=("Arial", 20))
        self.homepage_label.config(bg="white")
        self.homepage_label.pack(pady=20)

        #display showtime image
        self.showtime_image=Image.open("images/showtime.jpg")
        self.showtime_image=self.showtime_image.resize((600, 400), Image.LANCZOS)
        self.showtime_image=ImageTk.PhotoImage(self.showtime_image)
        self.showtime_image_label=tk.Label(self.homepage, image=self.showtime_image)
        self.showtime_image_label.pack()


        self.homepage_button=tk.Button(self.homepage, text="Start", font=("Arial", 15), command=self.login_page)
        self.homepage_button.pack(pady=20)


    def login_page(self):
        self.clear_content()
        self.loginpage=tk.Frame(self.root)
        self.loginpage.pack(fill="both", expand=True)
        self.loginpage.grid_rowconfigure(0, weight=1)
        self.loginpage.grid_columnconfigure(0, weight=1)

        self.loginpage_label=tk.Label(self.loginpage, text="Login", font=("Arial", 20))
        self.loginpage_label.pack(pady=20)

        self.loginpage_username_label=tk.Label(self.loginpage, text="Username", font=("Arial", 15))
        self.loginpage_username_label.pack(pady=10)

        self.loginpage_username_entry=tk.Entry(self.loginpage, font=("Arial", 15))
        self.loginpage_username_entry.pack(pady=10)

        self.loginpage_password_label=tk.Label(self.loginpage, text="Password", font=("Arial", 15))
        self.loginpage_password_label.pack(pady=10)

        self.loginpage_password_entry=tk.Entry(self.loginpage, font=("Arial", 15), show="*")
        self.loginpage_password_entry.pack(pady=10)

        self.loginpage_button=tk.Button(self.loginpage, text="Login", font=("Arial", 15), command=self.loginUser)
        self.loginpage_button.pack(pady=10)

        self.loginpage_back_button=tk.Button(self.loginpage, text="Back", font=("Arial", 15), command=self.show_homepage)
        self.loginpage_back_button.pack(pady=10)

        #trouble siging in button
        self.loginpage_trouble_signing_in_button=tk.Button(self.loginpage, text="Reset Password !", font=("Arial", 15), command=self.trouble_signing_in)
        self.loginpage_trouble_signing_in_button.pack(pady=10)



        self.create_account_button=tk.Button(self.loginpage, text="Not a User??..SIGN UP", font=("Arial", 15), command=self.create_account)
        self.create_account_button.pack(pady=10)


    def trouble_signing_in(self):
        self.clear_content()
        #password reset page
        self.troublesigninginpage=tk.Frame(self.root)
        self.troublesigninginpage.pack(fill="both", expand=True)

        self.troublesigninginpage.grid_rowconfigure(0, weight=1)
        self.troublesigninginpage.grid_columnconfigure(0, weight=1)

        self.troublesigninginpage_label=tk.Label(self.troublesigninginpage, text="Reset Password", font=("Arial", 20))
        self.troublesigninginpage_label.pack(pady=20)

        self.troublesigninginpage_username_label=tk.Label(self.troublesigninginpage, text="Username", font=("Arial", 15))
        self.troublesigninginpage_username_label.pack(pady=10)

        self.troublesigninginpage_username_entry=tk.Entry(self.troublesigninginpage, font=("Arial", 15))
        self.troublesigninginpage_username_entry.pack(pady=10)

        #gmail entry
        self.troublesigninginpage_gmail_label=tk.Label(self.troublesigninginpage, text="Email", font=("Arial", 15))
        self.troublesigninginpage_gmail_label.pack(pady=10)

        self.troublesigninginpage_gmail_entry=tk.Entry(self.troublesigninginpage, font=("Arial", 15))
        self.troublesigninginpage_gmail_entry.pack(pady=10)

        #verify username and email button
        self.troublesigninginpage_verify_button=tk.Button(self.troublesigninginpage, text="Verify", font=("Arial", 15), command=self.verify_user)
        self.troublesigninginpage_verify_button.pack(pady=10)

        #enter new password label
        self.troublesigninginpage_new_password_label=tk.Label(self.troublesigninginpage, text="Enter New Password", font=("Arial", 15))
        self.troublesigninginpage_new_password_label.pack(pady=10)

        #enter new password entry
        self.troublesigninginpage_new_password_entry=tk.Entry(self.troublesigninginpage, font=("Arial", 15), show="*")
        self.troublesigninginpage_new_password_entry.pack(pady=10)

        #confirm new password label
        self.troublesigninginpage_confirm_new_password_label=tk.Label(self.troublesigninginpage, text="Confirm New Password", font=("Arial", 15))
        self.troublesigninginpage_confirm_new_password_label.pack(pady=10)

        #confirm new password entry
        self.troublesigninginpage_confirm_new_password_entry=tk.Entry(self.troublesigninginpage, font=("Arial", 15), show="*")
        self.troublesigninginpage_confirm_new_password_entry.pack(pady=10)

        #change password button
        self.troublesigninginpage_change_password_button=tk.Button(self.troublesigninginpage, text="Change Password", font=("Arial", 15), command=self.change_password)
        self.troublesigninginpage_change_password_button.pack(pady=10)

        #disable password entry
        self.troublesigninginpage_new_password_entry.config(state="disabled")
        self.troublesigninginpage_confirm_new_password_entry.config(state="disabled")


        #back button
        self.troublesigninginpage_back_button=tk.Button(self.troublesigninginpage, text="Back", font=("Arial", 15), command=self.login_page)
        self.troublesigninginpage_back_button.pack(pady=10)


    def create_account(self):
        self.clear_content()
        self.root.geometry("800x700")
        self.createaccountpage=tk.Frame(self.root)
        self.createaccountpage.pack(fill="both", expand=True)
        self.createaccountpage.grid_rowconfigure(0, weight=1)
        self.createaccountpage.grid_columnconfigure(0, weight=1)

        self.createaccountpage_label=tk.Label(self.createaccountpage, text="Create Account", font=("Arial", 20))
        self.createaccountpage_label.pack(pady=20)

        self.createaccountpage_username_label=tk.Label(self.createaccountpage, text="Username", font=("Arial", 15))
        self.createaccountpage_username_label.pack(pady=10)

        self.createaccountpage_username_entry=tk.Entry(self.createaccountpage, font=("Arial", 15))
        self.createaccountpage_username_entry.pack(pady=10) 

        self.createaccountpage_firstname_label=tk.Label(self.createaccountpage, text="Firstname", font=("Arial", 15))
        self.createaccountpage_firstname_label.pack(pady=10)

        self.createaccountpage_firstname_entry=tk.Entry(self.createaccountpage, font=("Arial", 15))
        self.createaccountpage_firstname_entry.pack(pady=10)

        self.createaccountpage_lastname_label=tk.Label(self.createaccountpage, text="Lastname", font=("Arial", 15))
        self.createaccountpage_lastname_label.pack(pady=10)

        self.createaccountpage_lastname_entry=tk.Entry(self.createaccountpage, font=("Arial", 15))
        self.createaccountpage_lastname_entry.pack(pady=10)

        self.createaccountpage_password_label=tk.Label(self.createaccountpage, text="Password", font=("Arial", 15))
        self.createaccountpage_password_label.pack(pady=10)

        self.createaccountpage_password_entry=tk.Entry(self.createaccountpage, font=("Arial", 15), show="*")
        self.createaccountpage_password_entry.pack(pady=10)


        self.createaccountpage_gmail_label=tk.Label(self.createaccountpage, text="Email", font=("Arial", 15))
        self.createaccountpage_gmail_label.pack(pady=10)

        self.createaccountpage_gmail_entry=tk.Entry(self.createaccountpage, font=("Arial", 15))
        self.createaccountpage_gmail_entry.pack(pady=10)

        self.createaccountpage_button=tk.Button(self.createaccountpage, text="Create Account", font=("Arial", 15), command=self.registerUser)
        self.createaccountpage_button.pack(pady=10)

        self.createaccountpage_back_button=tk.Button(self.createaccountpage, text="Back", font=("Arial", 15), command=self.login_page)
        self.createaccountpage_back_button.pack(pady=10)


    def show_mainpage(self):
        self.clear_content()
        self.mainpage=tk.Frame(self.root)
        self.mainpage.pack(fill="both", expand=True)
        self.mainpage.grid_rowconfigure(0, weight=1)
        self.mainpage.grid_columnconfigure(0, weight=1)

        self.mainpage_label=tk.Label(self.mainpage, text="Main Page", font=("Arial", 20))
        self.mainpage_label.pack(pady=20)


        self.mainpage_button=tk.Button(self.mainpage, text="Start", font=("Arial", 15), command=self.login_page)
        self.mainpage_button.pack(pady=20)

    def admin_page(self):
        self.clear_content()
        self.root.geometry("1000x700")
        self.adminpage=tk.Frame(self.root)
        self.adminpage.pack(fill="both", expand=True)
        
        self.adminpage.grid_rowconfigure(1, weight=1)
        self.adminpage.grid_columnconfigure(1, weight=1)

        self.adminpage_label=tk.Label(self.adminpage, text="Admin Page", font=("Arial", 20))
        self.adminpage_label.pack()
        # self.adminpage_label.pack(pady=20)

        #notebook tabs
        self.adminpage_notebook=ttk.Notebook(self.adminpage)
        self.adminpage_notebook.pack(fill="both", expand=True)

        #movies details tab
        self.adminpage_movies_details_tab=tk.Frame(self.adminpage_notebook)
        self.adminpage_notebook.add(self.adminpage_movies_details_tab, text="Movies Details")

        #movie details tab
        self.adminpage_movies_details_tab.grid_rowconfigure(1, weight=1)
        self.adminpage_movies_details_tab.grid_columnconfigure(0, weight=1)

        #notebook inside movie details tab
        self.adminpage_movies_details_notebook=ttk.Notebook(self.adminpage_movies_details_tab)
        self.adminpage_movies_details_notebook.grid(row=1, column=0, columnspan=4, pady=0,sticky='nsew')

        #top trending movies tab
        self.adminpage_top_trending_movies_tab=tk.Frame(self.adminpage_movies_details_notebook)
        self.adminpage_movies_details_notebook.add(self.adminpage_top_trending_movies_tab, text="Top Trending Movies")

        #trending movies tab movies image canvas
        self.adminpage_top_trending_movies_tab_movies_image_canvas=tk.Canvas(self.adminpage_top_trending_movies_tab)
        self.adminpage_top_trending_movies_tab_movies_image_canvas.pack(fill="both", expand=True)

        #trending movies tab movies image scrollbar
        self.adminpage_top_trending_movies_tab_movies_image_scrollbar=tk.Scrollbar(self.adminpage_top_trending_movies_tab, orient=tk.VERTICAL, command=self.adminpage_top_trending_movies_tab_movies_image_canvas.xview)
        self.adminpage_top_trending_movies_tab_movies_image_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        #configure canvas
        self.adminpage_top_trending_movies_tab_movies_image_canvas.configure(yscrollcommand=self.adminpage_top_trending_movies_tab_movies_image_scrollbar.set)
        self.adminpage_top_trending_movies_tab_movies_image_canvas.bind('<Configure>', lambda e: self.adminpage_top_trending_movies_tab_movies_image_canvas.configure(scrollregion=self.adminpage_top_trending_movies_tab_movies_image_canvas.bbox("all")))

        #create another frame inside canvas
        self.adminpage_top_trending_movies_tab_movies_image_canvas_frame=tk.Frame(self.adminpage_top_trending_movies_tab_movies_image_canvas)
        self.adminpage_top_trending_movies_tab_movies_image_canvas.create_window((0, 0), window=self.adminpage_top_trending_movies_tab_movies_image_canvas_frame, anchor="nw")

        #get movies id from trending movies list
        # Connect to the MySQL server
        current_trending_movies=self.trending_movie
        #iterate one by one from all movies and display images
        # print(current_trending_movies)
        current_i=0
        for i, movie in enumerate(current_trending_movies):
            try:
                print(movie)
                #display movie image as button
                movie=list(movie)
                movie_object = movie
                # print(movie)
                movie = {
                    "movie_id": movie[0],
                    "movie_name": movie[1],
                    "release_date": movie[2],
                    "movie_date": movie[4],
                    "movie_time": movie[5],
                    "movie_seats": movie[6],
                    "movie_price": movie[7],
                    "movie_image_path": movie[8]   
                }
                # print(movie)
                # print(movie["movie_image_path"])
                image = Image.open(movie["movie_image_path"])
                image = image.resize((150, 200), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                row = i // 6
                col = i % 6

                admin_top_trending_movies_button = tk.Button(self.adminpage_top_trending_movies_tab_movies_image_canvas_frame, image=photo, command=lambda movie=movie: self.show_movie_details(movie))
                admin_top_trending_movies_button.image = photo
                admin_top_trending_movies_button.grid(row=row, column=col, padx=5, pady=5)
                current_i=i 
                # print(i)
            except:
                pass

        #finally add add movie image
        #add movie image
        image = Image.open("images/add_movie.png")
        image = image.resize((150, 200), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        # print("current_i",current_i)
        current_i+=1
        row = current_i // 6
        col = current_i % 6

        admin_top_trending_movies_button = tk.Button(self.adminpage_top_trending_movies_tab_movies_image_canvas_frame, image=photo, command=self.trending_add_movie_page)
        admin_top_trending_movies_button.image = photo
        admin_top_trending_movies_button.grid(row=row, column=col, padx=5, pady=5)


        #upcoming movies tab
        self.adminpage_upcoming_movies_tab=tk.Frame(self.adminpage_movies_details_notebook)
        self.adminpage_movies_details_notebook.add(self.adminpage_upcoming_movies_tab, text="Upcoming Movies")

        #upcoming movies tab movies image canvas
        self.adminpage_upcoming_movies_tab_movies_image_canvas=tk.Canvas(self.adminpage_upcoming_movies_tab)
        self.adminpage_upcoming_movies_tab_movies_image_canvas.pack(fill="both", expand=True)

        #upcoming movies tab movies image scrollbar
        self.adminpage_upcoming_movies_tab_movies_image_scrollbar=tk.Scrollbar(self.adminpage_upcoming_movies_tab, orient=tk.VERTICAL, command=self.adminpage_upcoming_movies_tab_movies_image_canvas.xview)
        self.adminpage_upcoming_movies_tab_movies_image_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        #configure canvas
        self.adminpage_upcoming_movies_tab_movies_image_canvas.configure(yscrollcommand=self.adminpage_upcoming_movies_tab_movies_image_scrollbar.set)
        self.adminpage_upcoming_movies_tab_movies_image_canvas.bind('<Configure>', lambda e: self.adminpage_upcoming_movies_tab_movies_image_canvas.configure(scrollregion=self.adminpage_upcoming_movies_tab_movies_image_canvas.bbox("all")))

        #create another frame inside canvas
        self.adminpage_upcoming_movies_tab_movies_image_canvas_frame=tk.Frame(self.adminpage_upcoming_movies_tab_movies_image_canvas)
        self.adminpage_upcoming_movies_tab_movies_image_canvas.create_window((0, 0), window=self.adminpage_upcoming_movies_tab_movies_image_canvas_frame, anchor="nw")

        #get movies id from upcoming movies list
        # Connect to the MySQL server
        current_upcoming_movies=self.upcoming_movies
        #iterate one by one from all movies and display images
        # print(current_upcoming_movies)
        for i, movie in enumerate(current_upcoming_movies):
            #display movie image as button
            movie=list(movie)
            # print(movie)
            movie = {
                    "movie_id": movie[0],
                    "movie_name": movie[1],
                    "release_date": movie[2],
                    "movie_date": movie[4],
                    "movie_time": movie[5],
                    "movie_seats": movie[6],
                    "movie_price": movie[7],
                    "movie_image_path": movie[8]   
                }
            # print(movie)
            # print(movie["movie_image_path"])
            image = Image.open(movie["movie_image_path"])
            image = image.resize((150, 200), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            row = i // 6  # integer division to get row number
            col = i % 6 # modulo operator to get column number

            admin_upcoming_movies_button = tk.Button(self.adminpage_upcoming_movies_tab_movies_image_canvas_frame, image=photo, command=lambda movie=movie: self.show_movie_details(movie))
            admin_upcoming_movies_button.image = photo
            admin_upcoming_movies_button.grid(row=row, column=col, padx=5, pady=5)


        #all movies tab
        self.adminpage_all_movies_tab=tk.Frame(self.adminpage_movies_details_notebook)
        self.adminpage_movies_details_notebook.add(self.adminpage_all_movies_tab, text="All Movies")

        #set all movies tab as default tab
        self.adminpage_movies_details_notebook.select(self.adminpage_all_movies_tab)


        #all movies tab movies image canvas
        self.adminpage_all_movies_tab_movies_image_canvas=tk.Canvas(self.adminpage_all_movies_tab)
        self.adminpage_all_movies_tab_movies_image_canvas.pack(fill="both", expand=True)

        #all movies tab movies image scrollbar
        self.adminpage_all_movies_tab_movies_image_scrollbar=tk.Scrollbar(self.adminpage_all_movies_tab, orient=tk.VERTICAL, command=self.adminpage_all_movies_tab_movies_image_canvas.xview)
        self.adminpage_all_movies_tab_movies_image_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        #configure canvas
        self.adminpage_all_movies_tab_movies_image_canvas.configure(yscrollcommand=self.adminpage_all_movies_tab_movies_image_scrollbar.set)
        self.adminpage_all_movies_tab_movies_image_canvas.bind('<Configure>', lambda e: self.adminpage_all_movies_tab_movies_image_canvas.configure(scrollregion=self.adminpage_all_movies_tab_movies_image_canvas.bbox("all")))

        #create another frame inside canvas
        self.adminpage_all_movies_tab_movies_image_canvas_frame=tk.Frame(self.adminpage_all_movies_tab_movies_image_canvas)
        self.adminpage_all_movies_tab_movies_image_canvas.create_window((0, 0), window=self.adminpage_all_movies_tab_movies_image_canvas_frame, anchor="nw")

        # Connect to the MySQL server
        all_movies=self.all_movies
        # print(all_movies)
        #iterate one by one from all movies and display images
        for i, movie in enumerate(self.all_movies):
            #display movie image as button
            movie=list(movie)
            # print(movie)
            movie = {
                    "movie_id": movie[0],
                    "movie_name": movie[1],
                    "release_date": movie[2],
                    "movie_date": movie[4],
                    "movie_time": movie[5],
                    "movie_seats": movie[6],
                    "movie_price": movie[7],
                    "movie_image_path": movie[8]   
                }
            # print(movie)
            # print(movie["movie_image_path"])
            image = Image.open(movie["movie_image_path"])
            image = image.resize((150, 200), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            row = i // 6  # integer division to get row number
            col = i % 6 # modulo operator to get column number

            admin_all_movies_button = tk.Button(self.adminpage_all_movies_tab_movies_image_canvas_frame, image=photo, command=lambda movie=movie: self.show_movie_details(movie))
            admin_all_movies_button.image = photo
            admin_all_movies_button.grid(row=row, column=col, padx=5, pady=5)
        

        #book movie tab 
        self.adminpage_book_movie_tab=tk.Frame(self.adminpage_notebook)
        self.adminpage_notebook.add(self.adminpage_book_movie_tab, text="Book Movie")

        #book movie tab
        self.adminpage_book_movie_tab.grid_rowconfigure(1, weight=1)
        self.adminpage_book_movie_tab.grid_columnconfigure(0, weight=1)

        #notebook inside book movie tab
        self.adminpage_book_movie_notebook=ttk.Notebook(self.adminpage_book_movie_tab)
        self.adminpage_book_movie_notebook.grid(row=1, column=0, columnspan=4, pady=0,sticky='nsew')

        #top trending movies tab
        self.adminpage_book_movie_top_trending_movies_tab=tk.Frame(self.adminpage_book_movie_notebook)
        self.adminpage_book_movie_notebook.add(self.adminpage_book_movie_top_trending_movies_tab, text="Top Trending Movies")

        #recently booked movies tab
        self.adminpage_book_movie_recently_booked_movies_tab=tk.Frame(self.adminpage_book_movie_notebook)
        self.adminpage_book_movie_notebook.add(self.adminpage_book_movie_recently_booked_movies_tab, text="Recently Booked Movies")

        #recently booked movies tab movies image canvas
        self.adminpage_book_movie_recently_booked_movies_tab_movies_image_canvas=tk.Canvas(self.adminpage_book_movie_recently_booked_movies_tab)
        self.adminpage_book_movie_recently_booked_movies_tab_movies_image_canvas.pack(fill="both", expand=True)

        #recently booked movies tab movies image scrollbar
        self.adminpage_book_movie_recently_booked_movies_tab_movies_image_scrollbar=tk.Scrollbar(self.adminpage_book_movie_recently_booked_movies_tab, orient=tk.VERTICAL, command=self.adminpage_book_movie_recently_booked_movies_tab_movies_image_canvas.xview)
        self.adminpage_book_movie_recently_booked_movies_tab_movies_image_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        #configure canvas
        self.adminpage_book_movie_recently_booked_movies_tab_movies_image_canvas.configure(yscrollcommand=self.adminpage_book_movie_recently_booked_movies_tab_movies_image_scrollbar.set)
        self.adminpage_book_movie_recently_booked_movies_tab_movies_image_canvas.bind('<Configure>', lambda e: self.adminpage_book_movie_recently_booked_movies_tab_movies_image_canvas.configure(scrollregion=self.adminpage_book_movie_recently_booked_movies_tab_movies_image_canvas.bbox("all")))

        #create another frame inside canvas
        self.adminpage_book_movie_recently_booked_movies_tab_movies_image_canvas_frame=tk.Frame(self.adminpage_book_movie_recently_booked_movies_tab_movies_image_canvas)
        self.adminpage_book_movie_recently_booked_movies_tab_movies_image_canvas.create_window((0, 0), window=self.adminpage_book_movie_recently_booked_movies_tab_movies_image_canvas_frame, anchor="nw")

        #get bookings from database where agent mail is current user mail
        # Connect to the MySQL server
        conn = mysql.connector.connect(**mysql_database)
        cursor = conn.cursor()
        #get all bookings
        cursor.execute("SELECT * FROM bookings WHERE agent_mail=%s",(self.current_user_gmail,))
        current_recently_booked_movies=cursor.fetchall()
        # print(current_recently_booked_movies)
        #iterate one by one from all movies and display images
        for i, booking in enumerate(current_recently_booked_movies):
            movie_id=booking[1]
            # print(movie_id)
            #get movie details from movie id
            cursor.execute("SELECT * FROM movies WHERE movie_id=%s",(movie_id,))
            movie=cursor.fetchone()
            # print(movie)
            #display movie image as button
            movie=list(movie)
            # print(movie)
            movie = {
                    "movie_id": movie[0],
                    "movie_name": movie[1],
                    "release_date": movie[2],
                    "movie_date": movie[4],
                    "movie_time": movie[5],
                    "movie_seats": movie[6],
                    "movie_price": movie[7],
                    "movie_image_path": movie[8]   
                }
            # print(movie)
            # print(movie["movie_image_path"])
            image = Image.open(movie["movie_image_path"])
            image = image.resize((150, 200), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            row = i // 6  # integer division to get row number
            col = i % 6 # modulo operator to get column number

            admin_recently_booked_movies_button = tk.Button(self.adminpage_book_movie_recently_booked_movies_tab_movies_image_canvas_frame, image=photo, command=lambda movie=movie: self.book_movie(movie["movie_id"],tab="recently_booked_movies"))
            admin_recently_booked_movies_button.image = photo
            admin_recently_booked_movies_button.grid(row=row, column=col, padx=5, pady=5)

            #display no of seats booked under image
            admin_recently_booked_movies_label=tk.Label(self.adminpage_book_movie_recently_booked_movies_tab_movies_image_canvas_frame, text="Seats Booked: "+str(booking[6]), font=("Arial", 10))
            admin_recently_booked_movies_label.grid(row=row+1, column=col, padx=5, pady=5)


        #all movies tab
        self.adminpage_book_movie_all_movies_tab=tk.Frame(self.adminpage_book_movie_notebook)
        self.adminpage_book_movie_notebook.add(self.adminpage_book_movie_all_movies_tab, text="All Movies")

        #upcoming movies tab
        self.adminpage_book_movie_upcoming_movies_tab=tk.Frame(self.adminpage_book_movie_notebook)
        self.adminpage_book_movie_notebook.add(self.adminpage_book_movie_upcoming_movies_tab, text="Upcoming Movies")

        #set trending movies tab as default tab
        self.adminpage_book_movie_notebook.select(self.adminpage_book_movie_top_trending_movies_tab)


        #top trending movies tab movies image canvas
        self.adminpage_book_movie_top_trending_movies_tab_movies_image_canvas=tk.Canvas(self.adminpage_book_movie_top_trending_movies_tab)
        self.adminpage_book_movie_top_trending_movies_tab_movies_image_canvas.pack(fill="both", expand=True)

        #top trending movies tab movies image scrollbar
        self.adminpage_book_movie_top_trending_movies_tab_movies_image_scrollbar=tk.Scrollbar(self.adminpage_book_movie_top_trending_movies_tab, orient=tk.VERTICAL, command=self.adminpage_book_movie_top_trending_movies_tab_movies_image_canvas.xview)
        self.adminpage_book_movie_top_trending_movies_tab_movies_image_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        #configure canvas
        self.adminpage_book_movie_top_trending_movies_tab_movies_image_canvas.configure(yscrollcommand=self.adminpage_book_movie_top_trending_movies_tab_movies_image_scrollbar.set)
        self.adminpage_book_movie_top_trending_movies_tab_movies_image_canvas.bind('<Configure>', lambda e: self.adminpage_book_movie_top_trending_movies_tab_movies_image_canvas.configure(scrollregion=self.adminpage_book_movie_top_trending_movies_tab_movies_image_canvas.bbox("all")))

        #create another frame inside canvas
        self.adminpage_book_movie_top_trending_movies_tab_movies_image_canvas_frame=tk.Frame(self.adminpage_book_movie_top_trending_movies_tab_movies_image_canvas)
        self.adminpage_book_movie_top_trending_movies_tab_movies_image_canvas.create_window((0, 0), window=self.adminpage_book_movie_top_trending_movies_tab_movies_image_canvas_frame, anchor="nw")

        #get movies from database and display images
        # Connect to the MySQL server
        # self.display_top_trending_movies()
        current_trending_movies=self.trending_movie
        #iterate one by one from all movies and display images
        # print(current_trending_movies)
        for i, movie in enumerate(current_trending_movies):
            #display movie image as button
            movie=list(movie)
            # print(movie)
            movie = {
                    "movie_id": movie[0],
                    "movie_name": movie[1],
                    "release_date": movie[2],
                    "movie_date": movie[4],
                    "movie_time": movie[5],
                    "movie_seats": movie[6],
                    "movie_price": movie[7],
                    "movie_image_path": movie[8]   
                }
            # print(movie)
            # print(movie["movie_image_path"])
            image = Image.open(movie["movie_image_path"])
            image = image.resize((150, 200), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            row = i // 6
            col = i % 6

            admin_top_trending_movies_button = tk.Button(self.adminpage_book_movie_top_trending_movies_tab_movies_image_canvas_frame, image=photo, command=lambda movie=movie: self.book_movie(movie["movie_id"],tab="top_trending_movies"))
            admin_top_trending_movies_button.image = photo

            admin_top_trending_movies_button.grid(row=row, column=col, padx=5, pady=5)

        #get movies from database and display images
        # Connect to the MySQL server
        # self.display_recently_booked_movies()


        #all movies tab movies image canvas
        self.adminpage_book_movie_all_movies_tab_movies_image_canvas=tk.Canvas(self.adminpage_book_movie_all_movies_tab)
        self.adminpage_book_movie_all_movies_tab_movies_image_canvas.pack(fill="both", expand=True)

        #all movies tab movies image scrollbar
        self.adminpage_book_movie_all_movies_tab_movies_image_scrollbar=tk.Scrollbar(self.adminpage_book_movie_all_movies_tab, orient=tk.VERTICAL, command=self.adminpage_book_movie_all_movies_tab_movies_image_canvas.xview)
        self.adminpage_book_movie_all_movies_tab_movies_image_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        #configure canvas
        self.adminpage_book_movie_all_movies_tab_movies_image_canvas.configure(yscrollcommand=self.adminpage_book_movie_all_movies_tab_movies_image_scrollbar.set)
        self.adminpage_book_movie_all_movies_tab_movies_image_canvas.bind('<Configure>', lambda e: self.adminpage_book_movie_all_movies_tab_movies_image_canvas.configure(scrollregion=self.adminpage_book_movie_all_movies_tab_movies_image_canvas.bbox("all")))

        #create another frame inside canvas
        self.adminpage_book_movie_all_movies_tab_movies_image_canvas_frame=tk.Frame(self.adminpage_book_movie_all_movies_tab_movies_image_canvas)
        self.adminpage_book_movie_all_movies_tab_movies_image_canvas.create_window((0, 0), window=self.adminpage_book_movie_all_movies_tab_movies_image_canvas_frame, anchor="nw")

        #get movies from database and display images
        # Connect to the MySQL server
        self.all_movies=self.get_all_movies()
        #iterate one by one from all movies and display images
        for i, movie in enumerate(self.all_movies):
            #display movie image as button
            movie=list(movie)
            movie = {
                    "movie_id": movie[0],
                    "movie_name": movie[1],
                    "release_date": movie[2],
                    "movie_date": movie[4],
                    "movie_time": movie[5],
                    "movie_seats": movie[6],
                    "movie_price": movie[7],
                    "movie_image_path": movie[8]   
                }
            # print(movie)
            # print(movie["movie_image_path"])
            image = Image.open(movie["movie_image_path"])
            image = image.resize((150, 200), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            row = i // 6  # integer division to get row number
            col = i % 6 # modulo operator to get column number
            tab="all_movies"

            admin_all_movies_button = tk.Button(self.adminpage_book_movie_all_movies_tab_movies_image_canvas_frame, image=photo, command=lambda movie=movie: self.book_movie(movie["movie_id"],tab))
            admin_all_movies_button.image = photo
            admin_all_movies_button.grid(row=row, column=col, padx=5, pady=5)

        #upcoming movies tab movies image canvas
        self.adminpage_book_movie_upcoming_movies_tab_movies_image_canvas=tk.Canvas(self.adminpage_book_movie_upcoming_movies_tab)
        self.adminpage_book_movie_upcoming_movies_tab_movies_image_canvas.pack(fill="both", expand=True)

        #upcoming movies tab movies image scrollbar
        self.adminpage_book_movie_upcoming_movies_tab_movies_image_scrollbar=tk.Scrollbar(self.adminpage_book_movie_upcoming_movies_tab, orient=tk.VERTICAL, command=self.adminpage_book_movie_upcoming_movies_tab_movies_image_canvas.xview)
        self.adminpage_book_movie_upcoming_movies_tab_movies_image_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        #configure canvas
        self.adminpage_book_movie_upcoming_movies_tab_movies_image_canvas.configure(yscrollcommand=self.adminpage_book_movie_upcoming_movies_tab_movies_image_scrollbar.set)
        self.adminpage_book_movie_upcoming_movies_tab_movies_image_canvas.bind('<Configure>', lambda e: self.adminpage_book_movie_upcoming_movies_tab_movies_image_canvas.configure(scrollregion=self.adminpage_book_movie_upcoming_movies_tab_movies_image_canvas.bbox("all")))

        #create another frame inside canvas
        self.adminpage_book_movie_upcoming_movies_tab_movies_image_canvas_frame=tk.Frame(self.adminpage_book_movie_upcoming_movies_tab_movies_image_canvas)
        self.adminpage_book_movie_upcoming_movies_tab_movies_image_canvas.create_window((0, 0), window=self.adminpage_book_movie_upcoming_movies_tab_movies_image_canvas_frame, anchor="nw")

        #get movies from database and display images
        for i,movie in enumerate(self.upcoming_movies):
            #display movie image as button
            movie=list(movie)
            movie = {
                    "movie_id": movie[0],
                    "movie_name": movie[1],
                    "release_date": movie[2],
                    "movie_date": movie[4],
                    "movie_time": movie[5],
                    "movie_seats": movie[6],
                    "movie_price": movie[7],
                    "movie_image_path": movie[8]   
                }
            # print(movie)
            # print(movie["movie_image_path"])
            image = Image.open(movie["movie_image_path"])
            image = image.resize((150, 200), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            row = i // 6
            col = i % 6

            admin_upcoming_movies_button = tk.Button(self.adminpage_book_movie_upcoming_movies_tab_movies_image_canvas_frame, image=photo)
            admin_upcoming_movies_button.image = photo
            admin_upcoming_movies_button.grid(row=row, column=col, padx=5, pady=5)

        #trending movies tab movies image canvas
        




        #add movie tab
        self.adminpage_add_movie_tab=tk.Frame(self.adminpage_notebook)
        self.adminpage_notebook.add(self.adminpage_add_movie_tab, text="Add Movie")

        #movie reports tab
        self.adminpage_reports_tab=tk.Frame(self.adminpage_notebook)
        self.adminpage_notebook.add(self.adminpage_reports_tab, text="Movie Reports")

        #movie reports frame
        # self.adminpage_reports_tab.grid_rowconfigure(1, weight=1)
        # self.adminpage_reports_tab.grid_columnconfigure(0, weight=1)

        #treeview of movie reports
        self.adminpage_reports_tab_treeview=ttk.Treeview(self.adminpage_reports_tab,columns=("movie_name", "release_date", "movie_date", "movie_time", "movie_seats", "movie_price"),show="headings")
        self.adminpage_reports_tab_treeview.pack(fill="both", expand=True)
        #treeview scrollbar
        # self.adminpage_reports_tab_treeview_scrollbar=tk.Scrollbar(self.adminpage_reports_tab, orient=tk.VERTICAL, command=self.adminpage_reports_tab_treeview.yview)
        # self.adminpage_reports_tab_treeview_scrollbar.pack(side=tk.LEFT, fill=tk.Y)


        #treeview columns

        #treeview headings
        self.adminpage_reports_tab_treeview.heading("#1", text="Movie Name")
        self.adminpage_reports_tab_treeview.heading("#2", text="Release Date")
        self.adminpage_reports_tab_treeview.heading("#3", text="Show Date")
        self.adminpage_reports_tab_treeview.heading("#4", text="Show Time")
        self.adminpage_reports_tab_treeview.heading("#5", text="Available Seats")
        self.adminpage_reports_tab_treeview.heading("#6", text="Show Price")

        #treeview column width
        self.adminpage_reports_tab_treeview.column("#1", width=100, anchor="center")
        self.adminpage_reports_tab_treeview.column("#2", width=100, anchor="center")
        self.adminpage_reports_tab_treeview.column("#3", width=100,anchor="center")
        self.adminpage_reports_tab_treeview.column("#4", width=100,anchor="center")
        self.adminpage_reports_tab_treeview.column("#5", width=100,anchor="center")
        self.adminpage_reports_tab_treeview.column("#6", width=100,anchor="center")

        #treeview data
        # Connect to the MySQL server
        conn = mysql.connector.connect(**mysql_database)
        cursor = conn.cursor()
        #get all bookings
        cursor.execute("SELECT * FROM movies")
        current_reports=cursor.fetchall()
        # print(current_reports)
        #iterate one by one from all movies and display images
        for i, movie in enumerate(current_reports):
            #display movie image as button
            movie=list(movie)
            # print(movie)
            movie = {
                    "movie_id": movie[0],
                    "movie_name": movie[1],
                    "release_date": movie[2],
                    "movie_date": movie[4],
                    "movie_time": movie[5],
                    "movie_seats": movie[6],
                    "movie_price": movie[7],
                    "movie_image_path": movie[8]   
                }
            # print(movie)
            # print(movie["movie_image_path"])
            self.adminpage_reports_tab_treeview.insert('', 'end', values=(movie["movie_name"], movie["release_date"], movie["movie_date"], movie["movie_time"], movie["movie_seats"], movie["movie_price"]))

        #print as pdf button
        self.adminpage_reports_tab_print_as_pdf_button=tk.Button(self.adminpage_reports_tab, text="Print as PDF", font=("Arial", 15), command=self.movie_reports_print_as_pdf)
        self.adminpage_reports_tab_print_as_pdf_button.pack(pady=10)

        #bookings reports tab
        self.adminpage_bookings_reports_tab=tk.Frame(self.adminpage_notebook)
        self.adminpage_notebook.add(self.adminpage_bookings_reports_tab, text="Bookings Reports")

        #bookings reports frame
        self.adminpage_bookings_reports_tab.grid_columnconfigure(0, weight=1)
        
        #treeview of bookings reports
        self.adminpage_bookings_reports_tab_treeview=ttk.Treeview(self.adminpage_bookings_reports_tab,columns=("Movie Name","Show Date","Name","Gmail","Seats Booked","Total Price"),show="headings")
        self.adminpage_bookings_reports_tab_treeview.pack(fill="both", expand=True)

        #treeview headings
        self.adminpage_bookings_reports_tab_treeview.heading("#1", text="Movie Name")
        self.adminpage_bookings_reports_tab_treeview.heading("#2", text="Show Date")
        self.adminpage_bookings_reports_tab_treeview.heading("#3", text="Name")
        self.adminpage_bookings_reports_tab_treeview.heading("#4", text="Gmail")
        self.adminpage_bookings_reports_tab_treeview.heading("#5", text="Seats Booked")
        self.adminpage_bookings_reports_tab_treeview.heading("#6", text="Total Price")

        #treeview column width
        self.adminpage_bookings_reports_tab_treeview.column("#1", width=100, anchor="center")
        self.adminpage_bookings_reports_tab_treeview.column("#2", width=100, anchor="center")
        self.adminpage_bookings_reports_tab_treeview.column("#3", width=100,anchor="center")
        self.adminpage_bookings_reports_tab_treeview.column("#4", width=100,anchor="center")
        self.adminpage_bookings_reports_tab_treeview.column("#5", width=100,anchor="center")
        self.adminpage_bookings_reports_tab_treeview.column("#6", width=100,anchor="center")

        #treeview data
        # Connect to the MySQL server
        conn = mysql.connector.connect(**mysql_database)
        cursor = conn.cursor()
        #get all bookings
        cursor.execute("SELECT * FROM bookings")
        current_reports=cursor.fetchall()
        # print(current_reports)
        #iterate one by one from all movies and display images
        for i, booking in enumerate(current_reports):
            booking=list(booking)
            #display movie image as button
            booking_id=booking[0]
            #get movie name and show date from movie id
            cursor.execute("SELECT * FROM movies WHERE movie_id=%s",(booking[1],))
            movie=cursor.fetchone()
            # print(movie)
            movie=list(movie)
            movie_name=movie[1]
            show_date=movie[4]
            name=booking[4]
            gmail=booking[5]
            seats_booked=booking[6]
            total_price=booking[7]

            self.adminpage_bookings_reports_tab_treeview.insert('', 'end', values=(movie_name, show_date, name, gmail, seats_booked, total_price))

        #print as pdf button
        self.adminpage_bookings_reports_tab_print_as_pdf_button=tk.Button(self.adminpage_bookings_reports_tab, text="Print as PDF", font=("Arial", 15), command=self.bookings_reports_print_as_pdf)
        self.adminpage_bookings_reports_tab_print_as_pdf_button.pack(pady=10)


        
        #users reports tab
        self.adminpage_users_reports_tab=tk.Frame(self.adminpage_notebook)
        self.adminpage_notebook.add(self.adminpage_users_reports_tab, text="Users Reports")

        #users reports frame
        self.adminpage_users_reports_tab.grid_columnconfigure(0, weight=1)

        #treeview of users reports
        self.adminpage_users_reports_tab_treeview=ttk.Treeview(self.adminpage_users_reports_tab,columns=("username", "gmail"),show="headings")
        self.adminpage_users_reports_tab_treeview.pack(fill="both", expand=True)

        #treeview headings
        self.adminpage_users_reports_tab_treeview.heading("#1", text="Username")
        self.adminpage_users_reports_tab_treeview.heading("#2", text="Gmail")

        #treeview column width
        self.adminpage_users_reports_tab_treeview.column("#1", width=100,anchor="center")
        self.adminpage_users_reports_tab_treeview.column("#2", width=100,anchor="center")

        #treeview data
        # Connect to the MySQL server
        conn = mysql.connector.connect(**mysql_database)    
        cursor = conn.cursor()
        #get all bookings
        cursor.execute("SELECT * FROM users")
        current_reports=cursor.fetchall()
        # print(current_reports)
        #iterate one by one from all movies and display images
        for i, user in enumerate(current_reports):
            #display movie image as button
            user=list(user)
            # print(user)
            user = {
                "username": user[1],
                "gmail": user[6]
            }
            # print(user)
            # print(user["movie_image_path"])
            self.adminpage_users_reports_tab_treeview.insert(parent='', index='end', iid=i, values=(user["username"], user["gmail"]))

        #pack
        self.adminpage_users_reports_tab_treeview.pack()

        #print as pdf button
        self.adminpage_users_reports_tab_print_as_pdf_button=tk.Button(self.adminpage_users_reports_tab, text="Print as PDF", font=("Arial", 15), command=self.users_reports_print_as_pdf)
        self.adminpage_users_reports_tab_print_as_pdf_button.pack(pady=10)
    
        #take data from admin to add movie
        #movie name label and entry side by side
        self.adminpage_add_movie_name_label=tk.Label(self.adminpage_add_movie_tab, text="Movie Name", font=("Arial", 15))
        self.adminpage_add_movie_name_label.grid(row=0, column=1, padx=20, pady=20, sticky='w')
        self.adminpage_add_movie_name_entry=tk.Entry(self.adminpage_add_movie_tab, font=("Arial", 15))
        #width of entry
        self.adminpage_add_movie_name_entry.config(width=22)
        self.adminpage_add_movie_name_entry.grid(row=0, column=2, padx=20, pady=20, sticky='w')

        #date label and entry side by side
        self.adminpage_add_movie_date_label=tk.Label(self.adminpage_add_movie_tab, text="Show Date", font=("Arial", 15))
        self.adminpage_add_movie_date_label.grid(row=1, column=1, padx=20, pady=20, sticky='w')
        self.adminpage_add_movie_date_entry=DateEntry(self.adminpage_add_movie_tab, font=("Arial", 15))
        #increase width of date entry
        self.adminpage_add_movie_date_entry.config(width=18)
        self.adminpage_add_movie_date_entry.grid(row=1, column=2, padx=20, pady=20, sticky='w')

        #time label and entry side by side combobox for time
        self.adminpage_add_movie_time_label=tk.Label(self.adminpage_add_movie_tab, text="Time", font=("Arial", 15))
        self.adminpage_add_movie_time_label.grid(row=2, column=1, padx=20, pady=20, sticky='w')

        

        #entry combobox for time
        #combobox data 
        time=["04:30 PM","05:30 PM", "07:30 PM", "10:30 PM"]
        self.adminpage_add_movie_time_combobox=ttk.Combobox(self.adminpage_add_movie_tab, values=time, font=("Arial", 15))
        #width of combobox
        self.adminpage_add_movie_time_combobox.config(width=18)
        self.adminpage_add_movie_time_combobox.grid(row=2, column=2, padx=20, pady=20, sticky='w')

        #seats label and entry side by side
        self.adminpage_add_movie_seats_label=tk.Label(self.adminpage_add_movie_tab, text="No.of Seats", font=("Arial", 15))
        self.adminpage_add_movie_seats_label.grid(row=3, column=1, padx=20, pady=20, sticky='w')
        self.adminpage_add_movie_seats_entry=tk.Entry(self.adminpage_add_movie_tab, font=("Arial", 15))
        self.adminpage_add_movie_name_entry.config(width=22)
        self.adminpage_add_movie_seats_entry.grid(row=3, column=2, padx=20, pady=20, sticky='w')

        #price label and entry side by side
        self.adminpage_add_movie_price_label=tk.Label(self.adminpage_add_movie_tab, text="Price", font=("Arial", 15))
        self.adminpage_add_movie_price_label.grid(row=4, column=1, padx=20, pady=20, sticky='w')
        self.adminpage_add_movie_price_entry=tk.Entry(self.adminpage_add_movie_tab, font=("Arial", 15))
        #width of entry
        self.adminpage_add_movie_name_entry.config(width=22)
        self.adminpage_add_movie_price_entry.grid(row=4, column=2, padx=20, pady=20, sticky='w')

        #release date label and entry side by side
        self.adminpage_add_movie_release_date_label=tk.Label(self.adminpage_add_movie_tab, text="Release Date", font=("Arial", 15))
        self.adminpage_add_movie_release_date_label.grid(row=5, column=1, padx=20, pady=20, sticky='w')
        self.adminpage_add_movie_release_date_entry=DateEntry(self.adminpage_add_movie_tab, font=("Arial", 15))
        #increase width of date entry
        self.adminpage_add_movie_release_date_entry.config(width=18)
        self.adminpage_add_movie_release_date_entry.grid(row=5, column=2, padx=20, pady=20, sticky='w')



        #insert movie image button
        self.adminpage_add_movie_image_button=tk.Button(self.adminpage_add_movie_tab, text="Insert Movie Image", font=("Arial", 15), command=self.upload_image)
        self.adminpage_add_movie_image_button.grid(row=3, column=5, columnspan=3, pady=10)

        #insert movie button
        self.adminpage_add_movie_button=tk.Button(self.adminpage_add_movie_tab, text="Insert Movie", font=("Arial", 15), command=self.insert_movie_db)
        self.adminpage_add_movie_button.grid(row=4, column=5, columnspan=3, pady=10)

        #back button
        self.adminpage_add_movie_back_button=tk.Button(self.adminpage_add_movie_tab, text="Back", font=("Arial", 15), command=self.admin_page)
        self.adminpage_add_movie_back_button.grid(row=6, column=1, columnspan=2, pady=10)

        #create a salesperson tab in admin page
        self.adminpage_salesperson_tab=tk.Frame(self.adminpage_notebook)
        self.adminpage_notebook.add(self.adminpage_salesperson_tab, text="Salesperson")

        #salesperson tab
        self.adminpage_salesperson_tab.grid_rowconfigure(1, weight=1)
        self.adminpage_salesperson_tab.grid_columnconfigure(0, weight=1)

        #notebook inside salesperson tab
        self.adminpage_salesperson_notebook=ttk.Notebook(self.adminpage_salesperson_tab)
        self.adminpage_salesperson_notebook.grid(row=1, column=0, columnspan=4, pady=0,sticky='nsew')

        #add salesperson tab
        self.adminpage_salesperson_add_salesperson_tab=tk.Frame(self.adminpage_salesperson_notebook)
        self.adminpage_salesperson_notebook.add(self.adminpage_salesperson_add_salesperson_tab, text="Add Salesperson")

        #add salesperson tab

        # salesperson username label and entry side by side
        self.adminpage_salesperson_add_salesperson_username_label = tk.Label(self.adminpage_salesperson_add_salesperson_tab, text="Username", font=("Arial", 15))
        self.adminpage_salesperson_add_salesperson_username_label.grid(row=0, column=1, padx=20, pady=20, sticky='nsew')

        self.adminpage_salesperson_add_salesperson_username_entry = tk.Entry(self.adminpage_salesperson_add_salesperson_tab, font=("Arial", 15))
        self.adminpage_salesperson_add_salesperson_username_entry.config(width=22)
        self.adminpage_salesperson_add_salesperson_username_entry.grid(row=0, column=2, padx=20, pady=20, sticky='nsew')

        # salesperson first name label and entry side by side
        self.adminpage_salesperson_add_salesperson_first_name_label = tk.Label(self.adminpage_salesperson_add_salesperson_tab, text="First Name", font=("Arial", 15))
        self.adminpage_salesperson_add_salesperson_first_name_label.grid(row=1, column=1, padx=20, pady=20, sticky='nsew')

        self.adminpage_salesperson_add_salesperson_first_name_entry = tk.Entry(self.adminpage_salesperson_add_salesperson_tab, font=("Arial", 15))
        self.adminpage_salesperson_add_salesperson_first_name_entry.config(width=22)
        self.adminpage_salesperson_add_salesperson_first_name_entry.grid(row=1, column=2, padx=20, pady=20, sticky='nsew')

        # salesperson last name label and entry side by side
        self.adminpage_salesperson_add_salesperson_last_name_label = tk.Label(self.adminpage_salesperson_add_salesperson_tab, text="Last Name", font=("Arial", 15))
        self.adminpage_salesperson_add_salesperson_last_name_label.grid(row=2, column=1, padx=20, pady=20, sticky='nsew')

        self.adminpage_salesperson_add_salesperson_last_name_entry = tk.Entry(self.adminpage_salesperson_add_salesperson_tab, font=("Arial", 15))
        self.adminpage_salesperson_add_salesperson_last_name_entry.config(width=22)
        self.adminpage_salesperson_add_salesperson_last_name_entry.grid(row=2, column=2, padx=20, pady=20, sticky='nsew')

        # salesperson password label and entry side by side
        self.adminpage_salesperson_add_salesperson_password_label = tk.Label(self.adminpage_salesperson_add_salesperson_tab, text="Password", font=("Arial", 15))
        self.adminpage_salesperson_add_salesperson_password_label.grid(row=3, column=1, padx=20, pady=20, sticky='nsew')

        self.adminpage_salesperson_add_salesperson_password_entry = tk.Entry(self.adminpage_salesperson_add_salesperson_tab, font=("Arial", 15))
        self.adminpage_salesperson_add_salesperson_password_entry.config(width=22)
        self.adminpage_salesperson_add_salesperson_password_entry.grid(row=3, column=2, padx=20, pady=20, sticky='nsew')

        # set password with firstname_lastname after inserting last name key release event
        self.adminpage_salesperson_add_salesperson_last_name_entry.bind("<KeyRelease>", self.set_password)

        # salesperson email label and entry side by side
        self.adminpage_salesperson_add_salesperson_email_label = tk.Label(self.adminpage_salesperson_add_salesperson_tab, text="Gmail", font=("Arial", 15))
        self.adminpage_salesperson_add_salesperson_email_label.grid(row=4, column=1, padx=20, pady=20, sticky='nsew')

        self.adminpage_salesperson_add_salesperson_email_entry = tk.Entry(self.adminpage_salesperson_add_salesperson_tab, font=("Arial", 15))
        self.adminpage_salesperson_add_salesperson_email_entry.config(width=22)
        self.adminpage_salesperson_add_salesperson_email_entry.grid(row=4, column=2, padx=20, pady=20, sticky='nsew')

        #save salesperson button
        self.adminpage_salesperson_add_salesperson_save_button=tk.Button(self.adminpage_salesperson_add_salesperson_tab, text="Save", font=("Arial", 15), command=self.registerUserSalesperson)
        self.adminpage_salesperson_add_salesperson_save_button.grid(row=5, column=1, columnspan=2, pady=10)

        #back button
        self.adminpage_salesperson_add_salesperson_back_button=tk.Button(self.adminpage_salesperson_add_salesperson_tab, text="Back", font=("Arial", 15), command=self.admin_page)
        self.adminpage_salesperson_add_salesperson_back_button.grid(row=6, column=1, columnspan=2, pady=10)

        #salesperson details tab
        self.adminpage_salesperson_details_tab=tk.Frame(self.adminpage_salesperson_notebook)
        self.adminpage_salesperson_notebook.add(self.adminpage_salesperson_details_tab, text="Salesperson Details")

        #salesperson details tab
        self.adminpage_salesperson_details_tab.grid_rowconfigure(1, weight=1)
        self.adminpage_salesperson_details_tab.grid_columnconfigure(0, weight=1)

        #tree view inside salesperson details tab display all salesperson details
        self.adminpage_salesperson_details_treeview=ttk.Treeview(self.adminpage_salesperson_details_tab)
        self.adminpage_salesperson_details_treeview.pack(fill="both", expand=True)

        #create columns in treeview
        self.adminpage_salesperson_details_treeview["columns"]=("username", "first_name", "last_name", "email")

        #format columns
        self.adminpage_salesperson_details_treeview.column("#0", width=0, stretch=tk.NO)
        self.adminpage_salesperson_details_treeview.column("username", anchor=tk.W, width=100)
        self.adminpage_salesperson_details_treeview.column("first_name", anchor=tk.W, width=100)
        self.adminpage_salesperson_details_treeview.column("last_name", anchor=tk.W, width=100)
        self.adminpage_salesperson_details_treeview.column("email", anchor=tk.W, width=100)

        #create headings
        self.adminpage_salesperson_details_treeview.heading("#0", text="", anchor=tk.W)
        self.adminpage_salesperson_details_treeview.heading("username", text="Username", anchor=tk.W)
        self.adminpage_salesperson_details_treeview.heading("first_name", text="First Name", anchor=tk.W)
        self.adminpage_salesperson_details_treeview.heading("last_name", text="Last Name", anchor=tk.W)
        self.adminpage_salesperson_details_treeview.heading("email", text="Email", anchor=tk.W)

        #insert data into treeview
        # Connect to the MySQL server
        conn=mysql.connector.connect(**mysql_database)
        # Get cursor
        cursor=conn.cursor()
        #query select details from user where role is salesperson
        query="SELECT username, firstname, lastname, gmail FROM showtime.users WHERE role='salesperson'"
        #execute query
        cursor.execute(query)
        #fetch all data
        salesperson_details=cursor.fetchall()
        # print(salesperson_details)
        #insert data into treeview
        for salesperson in salesperson_details:
            # print(salesperson)
            self.adminpage_salesperson_details_treeview.insert("", tk.END, text="", values=salesperson)
        
        #close cursor
        cursor.close()
        #close connection
        conn.close()

        #back button
        self.adminpage_salesperson_details_back_button=tk.Button(self.adminpage_salesperson_details_tab, text="Back", font=("Arial", 15), command=self.admin_page)
        self.adminpage_salesperson_details_back_button.pack(side=tk.BOTTOM, padx=5, pady=5, anchor='e')



            


        #logout button adminpage
        self.adminpage_add_movie_logout_button=tk.Button(self.adminpage, text="Logout", font=("Arial", 15), command=self.show_homepage)
        self.adminpage_add_movie_logout_button.pack(side=tk.BOTTOM, padx=5, pady=5, anchor='e')

        

    #show movie details
    def show_movie_details(self, movie):
        #clear all movies tab and fill movie details
        #check current notebook tab
        current_tab=self.adminpage_movies_details_notebook.tab(self.adminpage_movies_details_notebook.select(), "text")
        # print(current_tab)
        frame=None
        canvas=None
        if current_tab=="Top Trending Movies":
            #frame to trending movies tab
            frame=self.adminpage_top_trending_movies_tab_movies_image_canvas_frame
            canvas=self.adminpage_top_trending_movies_tab_movies_image_canvas
        elif current_tab=="Recently Booked Movies":
            #frame to recently booked movies tab
            frame=self.adminpage_recently_booked_movies_tab_movies_image_canvas_frame
            canvas=self.adminpage_recently_booked_movies_tab_movies_image_canvas
        elif current_tab=="All Movies":
            #frame to all movies tab
            frame=self.adminpage_all_movies_tab_movies_image_canvas_frame
            canvas=self.adminpage_all_movies_tab_movies_image_canvas
        elif current_tab=="Upcoming Movies":
            #frame to upcoming movies tab
            frame=self.adminpage_upcoming_movies_tab_movies_image_canvas_frame
            canvas=self.adminpage_upcoming_movies_tab_movies_image_canvas

        frame.destroy()
        frame = tk.Frame(canvas)
        frame.columnconfigure(0, weight=1)
        canvas.create_window((0, 0), window=frame, anchor="nw")
        #get movie details from all movies
        # print(movie)
        #convert dictionary to list
        movie=list(movie.values())
        print(movie)
        #image on the left side and movie details on the right side
        #image
        image = Image.open(movie[7])
        image = image.resize((350, 400), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        self.image_canvas=tk.Label(frame, image=photo)
        self.image_canvas.image = photo
        self.image_canvas.grid(row=0, column=0, padx=5, pady=5)

        # create a new frame next to the image
        movie_frame = tk.Frame(frame)
        movie_frame.grid(row=0, column=1, padx=5, pady=5, sticky='n')

        #movie details and details also as label
        self.adminpage_all_movies_tab_movies_details_frame_movie_name_label=tk.Label(movie_frame,font=("Arial", 15))
        self.adminpage_all_movies_tab_movies_details_frame_movie_name_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        #configure label as "Movie Name: movie name"
        self.adminpage_all_movies_tab_movies_details_frame_movie_name_label.config(text="Movie Name: "+movie[1])

        self.adminpage_all_movies_tab_movies_details_frame_movie_date_label=tk.Label(movie_frame,font=("Arial", 15))
        self.adminpage_all_movies_tab_movies_details_frame_movie_date_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        #configure label as "Date: movie date"
        self.adminpage_all_movies_tab_movies_details_frame_movie_date_label.config(text="Date: "+str(movie[3]))

        self.adminpage_all_movies_tab_movies_details_frame_movie_time_label=tk.Label(movie_frame,font=("Arial", 15))
        self.adminpage_all_movies_tab_movies_details_frame_movie_time_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        #configure label as "Time: movie time"
        self.adminpage_all_movies_tab_movies_details_frame_movie_time_label.config(text="Time: "+str(movie[4]))

        self.adminpage_all_movies_tab_movies_details_frame_movie_seats_label=tk.Label(movie_frame,font=("Arial", 15))
        self.adminpage_all_movies_tab_movies_details_frame_movie_seats_label.grid(row=3, column=0, padx=5, pady=5, sticky='w')
        #configure label as "Seats: movie seats"
        self.adminpage_all_movies_tab_movies_details_frame_movie_seats_label.config(text="Seats: "+str(movie[5]))

        self.adminpage_all_movies_tab_movies_details_frame_movie_price_label=tk.Label(movie_frame,font=("Arial", 15))
        self.adminpage_all_movies_tab_movies_details_frame_movie_price_label.grid(row=4, column=0, padx=5, pady=5, sticky='w')

        #configure label as "Price: movie price"
        self.adminpage_all_movies_tab_movies_details_frame_movie_price_label.config(text="Price: "+str(movie[6]))  


        #total seats booked
        #seats_booked(movie_id)
        seats_booked=self.seats_booked(movie[0])
        # print(seats_booked)
        self.adminpage_all_movies_tab_movies_details_frame_movie_seats_booked_label=tk.Label(movie_frame,font=("Arial", 15))
        self.adminpage_all_movies_tab_movies_details_frame_movie_seats_booked_label.grid(row=5, column=0, padx=5, pady=5, sticky='w')
        #configure label as "Seats Booked: seats booked"
        self.adminpage_all_movies_tab_movies_details_frame_movie_seats_booked_label.config(text="Seats Booked: "+str(seats_booked))


        
        #back button
        self.adminpage_all_movies_tab_movies_details_frame_back_button=tk.Button(movie_frame, text="Back", font=("Arial", 15), command=self.admin_page)
        self.adminpage_all_movies_tab_movies_details_frame_back_button.grid(row=6, column=0, padx=5, pady=5, sticky='w')




    #add_movie
    def trending_add_movie_page(self):
        #clear top trending movies tab and fill movie details
        self.adminpage_top_trending_movies_tab_movies_image_canvas_frame.destroy()
        self.adminpage_top_trending_movies_tab_movies_image_canvas_frame=tk.Frame(self.adminpage_top_trending_movies_tab_movies_image_canvas)
        self.adminpage_top_trending_movies_tab_movies_image_canvas_frame.columnconfigure(0, weight=1)
        self.adminpage_top_trending_movies_tab_movies_image_canvas.create_window((0, 0), window=self.adminpage_top_trending_movies_tab_movies_image_canvas_frame, anchor="nw")
        #get movie details from all movies  

        #display all movies except top trending movies from trending movies list
        # Connect to the MySQL server
        current_trending_movies=self.trending_movie
        row=0
        #iterate one by one from all movies and display images
        #print all movies
        for i, movie in enumerate(self.all_movies):
            #display movie image as button
            movie=list(movie)
            #if movie already in trending movies list then skip
            if not movie[3]:
                movie = {
                    "movie_id": movie[0],
                    "movie_name": movie[1],
                    "release_date": movie[2],
                    "movie_date": movie[4],
                    "movie_time": movie[5],
                    "movie_seats": movie[6],
                    "movie_price": movie[7],
                    "movie_image_path": movie[8]   
                }
                # print(movie)
                # print(movie["movie_image_path"])
                image = Image.open(movie["movie_image_path"])
                image = image.resize((150, 200), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                row = i // 6
                col = i % 6

                trending_add_movie_button = tk.Button(self.adminpage_top_trending_movies_tab_movies_image_canvas_frame, image=photo, command=lambda i=i: self.trending_add_movie(i))
                trending_add_movie_button.image = photo
                trending_add_movie_button.grid(row=row, column=col, padx=5, pady=5)
            

        #select a movie label in the end
        self.adminpage_top_trending_movies_tab_movies_image_canvas_frame_select_movie_label=tk.Label(self.adminpage_top_trending_movies_tab_movies_image_canvas_frame, text="Select a movie", font=("Arial", 15,'bold'))
        self.adminpage_top_trending_movies_tab_movies_image_canvas_frame_select_movie_label.grid(row=row+1, column=0, columnspan=6, padx=5, pady=5)

        #back button
        self.adminpage_top_trending_movies_tab_movies_image_canvas_frame_back_button=tk.Button(self.adminpage_top_trending_movies_tab_movies_image_canvas_frame, text="Back", font=("Arial", 15), command=self.admin_page)
        self.adminpage_top_trending_movies_tab_movies_image_canvas_frame_back_button.grid(row=row+2, column=0, columnspan=6, padx=5, pady=5)



    #trending_add_movie
    def trending_add_movie(self, i):
        #update the movie in trending column in database
        #get movie id from all movies
        movie_id=self.all_movies[i][0]
        #update trending column in database
        conn=mysql.connector.connect(**mysql_database)
        cursor=conn.cursor()
        cursor.execute("UPDATE movies SET trending=1 WHERE movie_id=%s", (movie_id,))
        conn.commit()
        cursor.close()
        conn.close()
        #run extract_movies
        self.extract_movies()
        #back to admin page
        self.admin_page()


    #seats_booked
    def seats_booked(self, movie_id):
       return 1




    #book movie
    def book_movie(self, i,tab):

        #check of seats are available
        #get movie details from i as movie id from database
        movie=self.get_movie_by_id(i)
        # print(movie)
        if movie[6]==0:
            #no seats available
            messagebox.showerror("Error", "No seats available")
            return
        
        print("book movie",i)
        #clear admin page book movie tab all movies tab and fill movie details
        #destroy based on the user
        current_frame=None
        print(self.currentuser_username)
        if self.currentuser_username=='admin':
            if tab=="top_trending_movies":
                current_frame=self.adminpage_book_movie_top_trending_movies_tab_movies_image_canvas_frame
                canvas=self.adminpage_book_movie_top_trending_movies_tab_movies_image_canvas
            elif tab=="recently_booked_movies":
                current_frame=self.adminpage_book_movie_recently_booked_movies_tab_movies_image_canvas_frame
                canvas=self.adminpage_book_movie_recently_booked_movies_tab_movies_image_canvas
            elif tab=="all_movies":
                current_frame=self.adminpage_book_movie_all_movies_tab_movies_image_canvas_frame
                canvas=self.adminpage_book_movie_all_movies_tab_movies_image_canvas
        elif self.currentuser_username=='salesperson':
            if tab=="top_trending_movies":
                current_frame=self.salespersonpage_book_movie_top_trending_movies_tab_movies_image_canvas_frame
                canvas=self.salespersonpage_book_movie_top_trending_movies_tab_movies_image_canvas
            elif tab=="recently_booked_movies":
                current_frame=self.salespersonpage_book_movie_recently_booked_movies_tab_movies_image_canvas_frame
                canvas=self.salespersonpage_book_movie_recently_booked_movies_tab_movies_image_canvas
            elif tab=="all_movies":
                current_frame=self.salespersonpage_book_movie_all_movies_tab_movies_image_canvas_frame
                canvas=self.salespersonpage_book_movie_all_movies_tab_movies_image_canvas
        else:
            current_frame=self.userpage_book_movie_all_movies_tab_movies_image_canvas_frame
            canvas=self.userpage_book_movie_all_movies_tab_movies_image_canvas

        current_frame.destroy()

        #create new frame
        current_frame=tk.Frame(canvas)
        #columnconfigure
        current_frame.columnconfigure(0, weight=1)
        canvas.create_window((0, 0), window=current_frame, anchor="nw")

        #get movie details from i as movie id from database 
        # Connect to the MySQL server
        self.movie=self.get_movie_by_id(i)

        # print(self.movie)

        # print(movie)
        #image on the left side and movie details on the right side
        #image
        image = Image.open(self.movie[8])
        image = image.resize((350, 400), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        frame_image_label=tk.Label(current_frame, image=photo)
        frame_image_label.image = photo  # Keep a reference to avoid garbage collection
        frame_image_label.grid(row=0, column=0, padx=5, pady=5)

        # create a new frame next to the image
        self.adminpage_book_movie_all_movies_tab_movies_details_frame = tk.Frame(current_frame)
        self.adminpage_book_movie_all_movies_tab_movies_details_frame.grid(row=0, column=1, padx=5, pady=5, sticky='n')

        #movie details and details also as label
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_movie_name_label=tk.Label(self.adminpage_book_movie_all_movies_tab_movies_details_frame,font=("Arial", 15))
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_movie_name_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        #configure label as "Movie Name: movie name"
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_movie_name_label.config(text="Movie Name: "+self.movie[1])

        self.adminpage_book_movie_all_movies_tab_movies_details_frame_movie_date_label=tk.Label(self.adminpage_book_movie_all_movies_tab_movies_details_frame,font=("Arial", 15))
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_movie_date_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        #configure label as "Date: movie date"
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_movie_date_label.config(text="Show Date: "+str(self.movie[4]))

        self.adminpage_book_movie_all_movies_tab_movies_details_frame_movie_time_label=tk.Label(self.adminpage_book_movie_all_movies_tab_movies_details_frame,font=("Arial", 15))
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_movie_time_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        #configure label as "Time: movie time"
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_movie_time_label.config(text="Time: "+str(self.movie[5]))

        self.adminpage_book_movie_all_movies_tab_movies_details_frame_movie_seats_label=tk.Label(self.adminpage_book_movie_all_movies_tab_movies_details_frame,font=("Arial", 15))
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_movie_seats_label.grid(row=3, column=0, padx=5, pady=5, sticky='w')
        #configure label as "Seats: movie seats"
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_movie_seats_label.config(text=" Available Seats: "+str(self.movie[6]))

        #Name label and entry side by side
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_name_label=tk.Label(self.adminpage_book_movie_all_movies_tab_movies_details_frame, text="Name", font=("Arial", 15))
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_name_label.grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_name_entry=tk.Entry(self.adminpage_book_movie_all_movies_tab_movies_details_frame, font=("Arial", 15))
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_name_entry.grid(row=4, column=1, padx=5, pady=5, sticky='w')

        #gmail label and entry side by side
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_gmail_label=tk.Label(self.adminpage_book_movie_all_movies_tab_movies_details_frame, text="Email", font=("Arial", 15))
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_gmail_label.grid(row=5, column=0, padx=5, pady=5, sticky='w')
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_gmail_entry=tk.Entry(self.adminpage_book_movie_all_movies_tab_movies_details_frame, font=("Arial", 15))
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_gmail_entry.grid(row=5, column=1, padx=5, pady=5, sticky='w')

        #no.of seats label and entry side by side
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_no_of_seats_label=tk.Label(self.adminpage_book_movie_all_movies_tab_movies_details_frame, text="No.of Seats", font=("Arial", 15))
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_no_of_seats_label.grid(row=6, column=0, padx=5, pady=5, sticky='w')
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_no_of_seats_entry=tk.Entry(self.adminpage_book_movie_all_movies_tab_movies_details_frame, font=("Arial", 15))
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_no_of_seats_entry.grid(row=6, column=1, padx=5, pady=5, sticky='w')

        #set to 1 as default
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_no_of_seats_entry.insert(0, 1)
        
        #Total Price
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_total_price_label=tk.Label(self.adminpage_book_movie_all_movies_tab_movies_details_frame, text="Total Price", font=("Arial", 15))
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_total_price_label.grid(row=7, column=0, padx=5, pady=5, sticky='w')
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_total_price_entry=tk.Entry(self.adminpage_book_movie_all_movies_tab_movies_details_frame, font=("Arial", 15))
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_total_price_entry.grid(row=7, column=1, padx=5, pady=5, sticky='w')

        #update total price label movie price * no.of seats

        self.adminpage_book_movie_all_movies_tab_movies_details_frame_total_price_entry.insert(0, self.movie[7]*1)

        self.current_movie_price=self.movie[7]

        #update total price label when no.of seats changes
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_no_of_seats_entry.bind("<KeyRelease>", self.update_total_price)

        #book movie button
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_book_movie_button=tk.Button(self.adminpage_book_movie_all_movies_tab_movies_details_frame, text="Book Movie", font=("Arial", 15), command=lambda movie=self.movie: self.book_movie_db(movie))
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_book_movie_button.grid(row=8, column=0, padx=5, pady=5, sticky='w')

        #back button

        #back button based on current user
        if self.currentuser_username=='admin':
            self.adminpage_book_movie_all_movies_tab_movies_details_frame_back_button=tk.Button(self.adminpage_book_movie_all_movies_tab_movies_details_frame, text="Back", font=("Arial", 15), command=self.admin_page)
            self.adminpage_book_movie_all_movies_tab_movies_details_frame_back_button.grid(row=9, column=0, padx=5, pady=5, sticky='w')
        elif self.currentuser_username=='salesperson':
            self.adminpage_book_movie_all_movies_tab_movies_details_frame_back_button=tk.Button(self.adminpage_book_movie_all_movies_tab_movies_details_frame, text="Back", font=("Arial", 15), command=self.salesperson_page)
            self.adminpage_book_movie_all_movies_tab_movies_details_frame_back_button.grid(row=9, column=0, padx=5, pady=5, sticky='w')
        # else:
        #     self.adminpage_book_movie_all_movies_tab_movies_details_frame_back_button=tk.Button(self.adminpage_book_movie_all_movies_tab_movies_details_frame, text="Back", font=("Arial", 15), command=self.user_page)
        #     self.adminpage_book_movie_all_movies_tab_movies_details_frame_back_button.grid(row=9, column=0, padx=5, pady=5, sticky='w')


    def salesperson_page(self):
        self.clear_content()
        self.root.geometry("1000x700")


        #salesperson page label
        self.salespersonpage_label=tk.Label(self.salespersonpage, text="Salesperson Page", font=("Arial", 30))
        self.salespersonpage_label.pack(padx=10, pady=10)

        self.salespersonpage=tk.Frame(self.root)
        self.salespersonpage.pack(fill="both", expand=True)
        self.salespersonpage.grid_rowconfigure(0, weight=1)
        self.salespersonpage.grid_columnconfigure(0, weight=1)

        #notebook tabs
        self.salespersonpage_notebook=ttk.Notebook(self.salespersonpage)
        self.salespersonpage_notebook.pack(fill="both", expand=True)

        #book movie tab
        self.salespersonpage_book_movie_tab=tk.Frame(self.salespersonpage_notebook)
        self.salespersonpage_notebook.add(self.salespersonpage_book_movie_tab, text="Book Movie")

        #book movie tab
        self.salespersonpage_book_movie_tab.grid_rowconfigure(1, weight=1)
        self.salespersonpage_book_movie_tab.grid_columnconfigure(0, weight=1)

        #movie reports tab
        self.salespersonpage_reports_tab=tk.Frame(self.salespersonpage_notebook)
        self.salespersonpage_notebook.add(self.salespersonpage_reports_tab, text="Movie Reports")

        #users reports tab
        self.salespersonpage_users_reports_tab=tk.Frame(self.salespersonpage_notebook)
        self.salespersonpage_notebook.add(self.salespersonpage_users_reports_tab, text="Users Reports")

        #notebook inside book movie tab
        self.salespersonpage_book_movie_notebook=ttk.Notebook(self.salespersonpage_book_movie_tab)
        self.salespersonpage_book_movie_notebook.grid(row=1, column=0, columnspan=4, pady=0,sticky='nsew')

        #top trending movies tab
        self.salespersonpage_book_movie_top_trending_movies_tab=tk.Frame(self.salespersonpage_book_movie_notebook)
        self.salespersonpage_book_movie_notebook.add(self.salespersonpage_book_movie_top_trending_movies_tab, text="Top Trending Movies")

        #recently booked movies tab
        self.salespersonpage_book_movie_recently_booked_movies_tab=tk.Frame(self.salespersonpage_book_movie_notebook)
        self.salespersonpage_book_movie_notebook.add(self.salespersonpage_book_movie_recently_booked_movies_tab, text="Recently Booked Movies")

        #all movies tab
        self.salespersonpage_book_movie_all_movies_tab=tk.Frame(self.salespersonpage_book_movie_notebook)
        self.salespersonpage_book_movie_notebook.add(self.salespersonpage_book_movie_all_movies_tab, text="All Movies")

        #upcoming movies tab
        self.salespersonpage_book_movie_upcoming_movies_tab=tk.Frame(self.salespersonpage_book_movie_notebook)
        self.salespersonpage_book_movie_notebook.add(self.salespersonpage_book_movie_upcoming_movies_tab, text="Upcoming Movies")

        #set all movies tab as default tab
        self.salespersonpage_book_movie_notebook.select(self.salespersonpage_book_movie_top_trending_movies_tab)

        #all movies tab movies image canvas
        self.salespersonpage_book_movie_all_movies_tab_movies_image_canvas=tk.Canvas(self.salespersonpage_book_movie_all_movies_tab)
        self.salespersonpage_book_movie_all_movies_tab_movies_image_canvas.pack(fill="both", expand=True)

        #all movies tab movies image scrollbar
        self.salespersonpage_book_movie_all_movies_tab_movies_image_scrollbar=tk.Scrollbar(self.salespersonpage_book_movie_all_movies_tab, orient=tk.VERTICAL, command=self.salespersonpage_book_movie_all_movies_tab_movies_image_canvas.xview)
        self.salespersonpage_book_movie_all_movies_tab_movies_image_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        #configure canvas
        self.salespersonpage_book_movie_all_movies_tab_movies_image_canvas.configure(yscrollcommand=self.salespersonpage_book_movie_all_movies_tab_movies_image_scrollbar.set)
        self.salespersonpage_book_movie_all_movies_tab_movies_image_canvas.bind('<Configure>', lambda e: self.salespersonpage_book_movie_all_movies_tab_movies_image_canvas.configure(scrollregion=self.salespersonpage_book_movie_all_movies_tab_movies_image_canvas.bbox("all")))

        #create another frame inside canvas
        self.salespersonpage_book_movie_all_movies_tab_movies_image_canvas_frame=tk.Frame(self.salespersonpage_book_movie_all_movies_tab_movies_image_canvas)
        self.salespersonpage_book_movie_all_movies_tab_movies_image_canvas.create_window((0, 0), window=self.salespersonpage_book_movie_all_movies_tab_movies_image_canvas_frame, anchor="nw")

        #get movies from database and display images
        # Connect to the MySQL server
        for i, movie in enumerate(self.all_movies):
            #display movie image as button
            movie=list(movie)
            movie = {
                "movie_id": movie[0],
                "movie_name": movie[1],
                "release_date": movie[2],
                "movie_date": movie[4],
                "movie_time": movie[5],
                "movie_seats": movie[6],
                "movie_price": movie[7],
                "movie_image_path": movie[8]   
            }
            # print(movie)
            # print(movie["movie_image_path"])
            image = Image.open(movie["movie_image_path"])
            image = image.resize((150, 200), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            row = i // 6
            col = i % 6

            salesperson_all_movies_button = tk.Button(self.salespersonpage_book_movie_all_movies_tab_movies_image_canvas_frame, image=photo, command=lambda movie=movie: self.book_movie(movie["movie_id"],"all_movies"))
            salesperson_all_movies_button.image = photo
            salesperson_all_movies_button.grid(row=row, column=col, padx=5, pady=5)

        #trending movies tab movies image canvas
        self.salespersonpage_book_movie_top_trending_movies_tab_movies_image_canvas=tk.Canvas(self.salespersonpage_book_movie_top_trending_movies_tab)
        self.salespersonpage_book_movie_top_trending_movies_tab_movies_image_canvas.pack(fill="both", expand=True)

        #treanding movies tab movies image scrollbar
        self.salespersonpage_book_movie_top_trending_movies_tab_movies_image_scrollbar=tk.Scrollbar(self.salespersonpage_book_movie_top_trending_movies_tab, orient=tk.VERTICAL, command=self.salespersonpage_book_movie_top_trending_movies_tab_movies_image_canvas.xview)
        self.salespersonpage_book_movie_top_trending_movies_tab_movies_image_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        #configure canvas
        self.salespersonpage_book_movie_top_trending_movies_tab_movies_image_canvas.configure(yscrollcommand=self.salespersonpage_book_movie_top_trending_movies_tab_movies_image_scrollbar.set)
        self.salespersonpage_book_movie_top_trending_movies_tab_movies_image_canvas.bind('<Configure>', lambda e: self.salespersonpage_book_movie_top_trending_movies_tab_movies_image_canvas.configure(scrollregion=self.salespersonpage_book_movie_top_trending_movies_tab_movies_image_canvas.bbox("all")))

        #create another frame inside canvas
        self.salespersonpage_book_movie_top_trending_movies_tab_movies_image_canvas_frame=tk.Frame(self.salespersonpage_book_movie_top_trending_movies_tab_movies_image_canvas)
        self.salespersonpage_book_movie_top_trending_movies_tab_movies_image_canvas.create_window((0, 0), window=self.salespersonpage_book_movie_top_trending_movies_tab_movies_image_canvas_frame, anchor="nw")

        #get movies from database and display images
        # Connect to the MySQL server
        for i, movie in enumerate(self.trending_movie):
            #display movie image as button
            movie=list(movie)
            #if movie already in trending movies list then skip
            movie = {
                "movie_id": movie[0],
                "movie_name": movie[1],
                "release_date": movie[2],
                "movie_date": movie[4],
                "movie_time": movie[5],
                "movie_seats": movie[6],
                "movie_price": movie[7],
                "movie_image_path": movie[8]   
            }
            # print(movie)
            # print(movie["movie_image_path"])
            image = Image.open(movie["movie_image_path"])
            image = image.resize((150, 200), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            row = i // 6
            col = i % 6

            salesperson_top_trending_movies_button = tk.Button(self.salespersonpage_book_movie_top_trending_movies_tab_movies_image_canvas_frame, image=photo, command=lambda movie=movie: self.book_movie(movie["movie_id"],"top_trending_movies"))
            salesperson_top_trending_movies_button.image = photo
            salesperson_top_trending_movies_button.grid(row=row, column=col, padx=5, pady=5)




        #recently booked movies tab movies image canvas
        self.salespersonpage_book_movie_recently_booked_movies_tab_movies_image_canvas=tk.Canvas(self.salespersonpage_book_movie_recently_booked_movies_tab)
        self.salespersonpage_book_movie_recently_booked_movies_tab_movies_image_canvas.pack(fill="both", expand=True)

        #recently booked movies tab movies image scrollbar
        self.salespersonpage_book_movie_recently_booked_movies_tab_movies_image_scrollbar=tk.Scrollbar(self.salespersonpage_book_movie_recently_booked_movies_tab, orient=tk.VERTICAL, command=self.salespersonpage_book_movie_recently_booked_movies_tab_movies_image_canvas.xview)
        self.salespersonpage_book_movie_recently_booked_movies_tab_movies_image_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        #configure canvas
        self.salespersonpage_book_movie_recently_booked_movies_tab_movies_image_canvas.configure(yscrollcommand=self.salespersonpage_book_movie_recently_booked_movies_tab_movies_image_scrollbar.set)
        self.salespersonpage_book_movie_recently_booked_movies_tab_movies_image_canvas.bind('<Configure>', lambda e: self.salespersonpage_book_movie_recently_booked_movies_tab_movies_image_canvas.configure(scrollregion=self.salespersonpage_book_movie_recently_booked_movies_tab_movies_image_canvas.bbox("all")))
        
        #create another frame inside canvas
        self.salespersonpage_book_movie_recently_booked_movies_tab_movies_image_canvas_frame=tk.Frame(self.salespersonpage_book_movie_recently_booked_movies_tab_movies_image_canvas)
        self.salespersonpage_book_movie_recently_booked_movies_tab_movies_image_canvas.create_window((0, 0), window=self.salespersonpage_book_movie_recently_booked_movies_tab_movies_image_canvas_frame, anchor="nw")

        #get movies from database and display images
        # Connect to the MySQL server

        #upcoming movies tab movies image canvas
        self.salespersonpage_book_movie_upcoming_movies_tab_movies_image_canvas=tk.Canvas(self.salespersonpage_book_movie_upcoming_movies_tab)
        self.salespersonpage_book_movie_upcoming_movies_tab_movies_image_canvas.pack(fill="both", expand=True)

        #upcoming movies tab movies image scrollbar
        self.salespersonpage_book_movie_upcoming_movies_tab_movies_image_scrollbar=tk.Scrollbar(self.salespersonpage_book_movie_upcoming_movies_tab, orient=tk.VERTICAL, command=self.salespersonpage_book_movie_upcoming_movies_tab_movies_image_canvas.xview)
        self.salespersonpage_book_movie_upcoming_movies_tab_movies_image_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        #configure canvas
        self.salespersonpage_book_movie_upcoming_movies_tab_movies_image_canvas.configure(yscrollcommand=self.salespersonpage_book_movie_upcoming_movies_tab_movies_image_scrollbar.set)
        self.salespersonpage_book_movie_upcoming_movies_tab_movies_image_canvas.bind('<Configure>', lambda e: self.salespersonpage_book_movie_upcoming_movies_tab_movies_image_canvas.configure(scrollregion=self.salespersonpage_book_movie_upcoming_movies_tab_movies_image_canvas.bbox("all")))

        #create another frame inside canvas
        self.salespersonpage_book_movie_upcoming_movies_tab_movies_image_canvas_frame=tk.Frame(self.salespersonpage_book_movie_upcoming_movies_tab_movies_image_canvas)
        self.salespersonpage_book_movie_upcoming_movies_tab_movies_image_canvas.create_window((0, 0), window=self.salespersonpage_book_movie_upcoming_movies_tab_movies_image_canvas_frame, anchor="nw")

        #get movies from database and display images
        # Connect to the MySQL server
        for i, movie in enumerate(self.upcoming_movies):
            #display movie image as button
            movie=list(movie)
            #if movie already in trending movies list then skip
            movie = {
                "movie_id": movie[0],
                "movie_name": movie[1],
                "release_date": movie[2],
                "movie_date": movie[4],
                "movie_time": movie[5],
                "movie_seats": movie[6],
                "movie_price": movie[7],
                "movie_image_path": movie[8]   
            }
            # print(movie)
            # print(movie["movie_image_path"])
            image = Image.open(movie["movie_image_path"])
            image = image.resize((150, 200), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            row = i // 6
            col = i % 6

            salesperson_upcoming_movies_button = tk.Button(self.salespersonpage_book_movie_upcoming_movies_tab_movies_image_canvas_frame, image=photo, command=lambda movie=movie: self.book_movie(movie["movie_id"],"upcoming_movies"))
            salesperson_upcoming_movies_button.image = photo
            salesperson_upcoming_movies_button.grid(row=row, column=col, padx=5, pady=5)

        #logout button
        self.salespersonpage_book_movie_all_movies_tab_movies_details_frame_logout_button=tk.Button(self.salespersonpage, text="Logout", font=("Arial", 15), command=self.show_homepage)
        self.salespersonpage_book_movie_all_movies_tab_movies_details_frame_logout_button.pack(side=tk.BOTTOM, padx=5, pady=5, anchor='e')






    def user_page(self):
        self.clear_content()
        self.root.geometry("1000x700")
        self.userpage=tk.Frame(self.root)
        self.userpage.pack(fill="both", expand=True)
        self.userpage.grid_rowconfigure(0, weight=1)
        self.userpage.grid_columnconfigure(0, weight=1)

        #notebook tabs
        self.userpage_notebook=ttk.Notebook(self.userpage)
        self.userpage_notebook.pack(fill="both", expand=True)

        #book movie tab
        self.userpage_book_movie_tab=tk.Frame(self.userpage_notebook)
        self.userpage_notebook.add(self.userpage_book_movie_tab, text="Book Movie")

        #book movie tab
        self.userpage_book_movie_tab.grid_rowconfigure(1, weight=1)
        self.userpage_book_movie_tab.grid_columnconfigure(0, weight=1)

        #my bookings tab
        self.userpage_my_bookings_tab=tk.Frame(self.userpage_notebook)
        self.userpage_notebook.add(self.userpage_my_bookings_tab, text="My Bookings")

        #notebook inside book movie tab
        self.userpage_book_movie_notebook=ttk.Notebook(self.userpage_book_movie_tab)
        self.userpage_book_movie_notebook.grid(row=1, column=0, columnspan=4, pady=0,sticky='nsew')

        #top trending movies tab
        self.userpage_book_movie_top_trending_movies_tab=tk.Frame(self.userpage_book_movie_notebook)
        self.userpage_book_movie_notebook.add(self.userpage_book_movie_top_trending_movies_tab, text="Top Trending Movies")

        #upcoming movies tab
        self.userpage_book_movie_upcoming_movies_tab=tk.Frame(self.userpage_book_movie_notebook)
        self.userpage_book_movie_notebook.add(self.userpage_book_movie_upcoming_movies_tab, text="Upcoming Movies")

        #all movies tab
        self.userpage_book_movie_all_movies_tab=tk.Frame(self.userpage_book_movie_notebook)
        self.userpage_book_movie_notebook.add(self.userpage_book_movie_all_movies_tab, text="All Movies")

        #set all movies tab as default tab
        self.userpage_book_movie_notebook.select(self.userpage_book_movie_top_trending_movies_tab)

        #all movies tab movies image canvas
        self.userpage_book_movie_all_movies_tab_movies_image_canvas=tk.Canvas(self.userpage_book_movie_all_movies_tab)
        self.userpage_book_movie_all_movies_tab_movies_image_canvas.pack(fill="both", expand=True)

        #all movies tab movies image scrollbar
        self.userpage_book_movie_all_movies_tab_movies_image_scrollbar=tk.Scrollbar(self.userpage_book_movie_all_movies_tab, orient=tk.VERTICAL, command=self.userpage_book_movie_all_movies_tab_movies_image_canvas.xview)
        self.userpage_book_movie_all_movies_tab_movies_image_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        #configure canvas
        self.userpage_book_movie_all_movies_tab_movies_image_canvas.configure(yscrollcommand=self.userpage_book_movie_all_movies_tab_movies_image_scrollbar.set)
        self.userpage_book_movie_all_movies_tab_movies_image_canvas.bind('<Configure>', lambda e: self.userpage_book_movie_all_movies_tab_movies_image_canvas.configure(scrollregion=self.userpage_book_movie_all_movies_tab_movies_image_canvas.bbox("all")))

        #create another frame inside canvas
        self.userpage_book_movie_all_movies_tab_movies_image_canvas_frame=tk.Frame(self.userpage_book_movie_all_movies_tab_movies_image_canvas)
        self.userpage_book_movie_all_movies_tab_movies_image_canvas.create_window((0, 0), window=self.userpage_book_movie_all_movies_tab_movies_image_canvas_frame, anchor="nw")

        #get movies from database and display images
        # Connect to the MySQL server
        for i, movie in enumerate(self.all_movies):
            #display movie image as button
            movie=list(movie)
            movie = {
                "movie_id": movie[0],
                "movie_name": movie[1],
                "release_date": movie[2],
                "movie_date": movie[4],
                "movie_time": movie[5],
                "movie_seats": movie[6],
                "movie_price": movie[7],
                "movie_image_path": movie[8]   
            }
            # print(movie)
            # print(movie["movie_image_path"])
            image = Image.open(movie["movie_image_path"])
            image = image.resize((150, 200), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            row = i // 6
            col = i % 6

            user_all_movies_button = tk.Button(self.userpage_book_movie_all_movies_tab_movies_image_canvas_frame, image=photo, command=lambda movie=movie: self.book_movie(movie["movie_id"],"all_movies"))
            user_all_movies_button.image = photo
            user_all_movies_button.grid(row=row, column=col, padx=5, pady=5)
        
        #trending movies tab movies image canvas
        self.userpage_book_movie_top_trending_movies_tab_movies_image_canvas=tk.Canvas(self.userpage_book_movie_top_trending_movies_tab)
        self.userpage_book_movie_top_trending_movies_tab_movies_image_canvas.pack(fill="both", expand=True)

        #treanding movies tab movies image scrollbar
        self.userpage_book_movie_top_trending_movies_tab_movies_image_scrollbar=tk.Scrollbar(self.userpage_book_movie_top_trending_movies_tab_movies_image_canvas, orient=tk.VERTICAL, command=self.userpage_book_movie_top_trending_movies_tab_movies_image_canvas.xview)
        self.userpage_book_movie_top_trending_movies_tab_movies_image_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        #configure canvas
        self.userpage_book_movie_top_trending_movies_tab_movies_image_canvas.configure(yscrollcommand=self.userpage_book_movie_top_trending_movies_tab_movies_image_scrollbar.set)
        self.userpage_book_movie_top_trending_movies_tab_movies_image_canvas.bind('<Configure>', lambda e: self.userpage_book_movie_top_trending_movies_tab_movies_image_canvas.configure(scrollregion=self.userpage_book_movie_top_trending_movies_tab_movies_image_canvas.bbox("all")))
     
        #create another frame inside canvas
        self.userpage_book_movie_top_trending_movies_tab_movies_image_canvas_frame=tk.Frame(self.userpage_book_movie_top_trending_movies_tab_movies_image_canvas)
        self.userpage_book_movie_top_trending_movies_tab_movies_image_canvas.create_window((0, 0), window=self.userpage_book_movie_top_trending_movies_tab_movies_image_canvas_frame, anchor="nw")

        #get movies from database and display images
        # Connect to the MySQL server
        for i, movie in enumerate(self.trending_movie):
            #display movie image as button
            movie=list(movie)
            #if movie already in trending movies list then skip
            movie = {
                "movie_id": movie[0],
                "movie_name": movie[1],
                "release_date": movie[2],
                "movie_date": movie[4],
                "movie_time": movie[5],
                "movie_seats": movie[6],
                "movie_price": movie[7],
                "movie_image_path": movie[8]   
            }
            # print(movie)
            # print(movie["movie_image_path"])
            image = Image.open(movie["movie_image_path"])
            image = image.resize((150, 200), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            row = i // 6
            col = i % 6

            user_top_trending_movies_button = tk.Button(self.userpage_book_movie_top_trending_movies_tab_movies_image_canvas_frame, image=photo, command=lambda movie=movie: self.book_movie(movie["movie_id"],"top_trending_movies"))
            user_top_trending_movies_button.image = photo
            user_top_trending_movies_button.grid(row=row, column=col, padx=5, pady=5)

        #upcoming movies tab movies image canvas
        self.userpage_book_movie_upcoming_movies_tab_movies_image_canvas=tk.Canvas(self.userpage_book_movie_upcoming_movies_tab)
        self.userpage_book_movie_upcoming_movies_tab_movies_image_canvas.pack(fill="both", expand=True)

        #upcoming movies tab movies image scrollbar
        self.userpage_book_movie_upcoming_movies_tab_movies_image_scrollbar=tk.Scrollbar(self.userpage_book_movie_upcoming_movies_tab, orient=tk.VERTICAL, command=self.userpage_book_movie_upcoming_movies_tab_movies_image_canvas.xview)
        self.userpage_book_movie_upcoming_movies_tab_movies_image_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        #configure canvas
        self.userpage_book_movie_upcoming_movies_tab_movies_image_canvas.configure(yscrollcommand=self.userpage_book_movie_upcoming_movies_tab_movies_image_scrollbar.set)
        self.userpage_book_movie_upcoming_movies_tab_movies_image_canvas.bind('<Configure>', lambda e: self.userpage_book_movie_upcoming_movies_tab_movies_image_canvas.configure(scrollregion=self.userpage_book_movie_upcoming_movies_tab_movies_image_canvas.bbox("all")))

        #create another frame inside canvas
        self.userpage_book_movie_upcoming_movies_tab_movies_image_canvas_frame=tk.Frame(self.userpage_book_movie_upcoming_movies_tab_movies_image_canvas)
        self.userpage_book_movie_upcoming_movies_tab_movies_image_canvas.create_window((0, 0), window=self.userpage_book_movie_upcoming_movies_tab_movies_image_canvas_frame, anchor="nw")

        #get movies from database and display images
        # Connect to the MySQL server

        for i, movie in enumerate(self.upcoming_movies):
            #display movie image as button
            movie=list(movie)
            #if movie already in trending movies list then skip
            movie = {
                "movie_id": movie[0],
                "movie_name": movie[1],
                "release_date": movie[2],
                "movie_date": movie[4],
                "movie_time": movie[5],
                "movie_seats": movie[6],
                "movie_price": movie[7],
                "movie_image_path": movie[8]   
            }
            # print(movie)
            # print(movie["movie_image_path"])
            image = Image.open(movie["movie_image_path"])
            image = image.resize((150, 200), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            row = i // 6
            col = i % 6

            user_upcoming_movies_button = tk.Button(self.userpage_book_movie_upcoming_movies_tab_movies_image_canvas_frame, image=photo, command=lambda movie=movie: self.book_movie(movie["movie_id"],"upcoming_movies"))
            user_upcoming_movies_button.image = photo
            user_upcoming_movies_button.grid(row=row, column=col, padx=5, pady=5)

        #my bookings tab movies image canvas
        self.userpage_my_bookings_tab_movies_image_canvas=tk.Canvas(self.userpage_my_bookings_tab)
        self.userpage_my_bookings_tab_movies_image_canvas.pack(fill="both", expand=True)

        #my bookings tab movies image scrollbar
        self.userpage_my_bookings_tab_movies_image_scrollbar=tk.Scrollbar(self.userpage_my_bookings_tab, orient=tk.VERTICAL, command=self.userpage_my_bookings_tab_movies_image_canvas.xview)
        self.userpage_my_bookings_tab_movies_image_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        #configure canvas
        self.userpage_my_bookings_tab_movies_image_canvas.configure(yscrollcommand=self.userpage_my_bookings_tab_movies_image_scrollbar.set)
        self.userpage_my_bookings_tab_movies_image_canvas.bind('<Configure>', lambda e: self.userpage_my_bookings_tab_movies_image_canvas.configure(scrollregion=self.userpage_my_bookings_tab_movies_image_canvas.bbox("all")))

        #create another frame inside canvas
        self.userpage_my_bookings_tab_movies_image_canvas_frame=tk.Frame(self.userpage_my_bookings_tab_movies_image_canvas)
        self.userpage_my_bookings_tab_movies_image_canvas.create_window((0, 0), window=self.userpage_my_bookings_tab_movies_image_canvas_frame, anchor="nw")

        #get movies booked by user from bookings table and display images
        # Connect to the MySQL server
        # conn = mysql.connector.connect(**mysql_database)
        # c=conn.cursor()
        # c.execute("SELECT * FROM showtime.bookings WHERE gmail=%s", (self.currentuser_gmail,))
        # my_bookings=c.fetchall()
        # # print(my_bookings)
        # for i, booking in enumerate(my_bookings):
        #     #booking details
    

        #     #display seats booked under each movie
        #     #get no.of seats booked for this movie
        #     c.execute("SELECT SUM(no_of_seats) FROM showtime.bookings WHERE movie_id=%s", (movie["movie_id"],))

        #logout button
        self.userpage_book_movie_all_movies_tab_movies_details_frame_logout_button=tk.Button(self.user_page, text="Logout", font=("Arial", 15), command=self.show_homepage)
        self.userpage_book_movie_all_movies_tab_movies_details_frame_logout_button.pack(side=tk.BOTTOM, padx=5, pady=5, anchor='e')




#Controller=======================================================================================================================================================================

    #update_total_price
    def update_total_price(self,event):
        #get no.of seats
        no_of_seats=self.adminpage_book_movie_all_movies_tab_movies_details_frame_no_of_seats_entry.get()
        #get movie price
        movie_price=self.current_movie_price
        #update total price
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_total_price_entry.delete(0, tk.END)
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_total_price_entry.insert(0, float(movie_price)*int(no_of_seats))



    #book movie db
    def book_movie_db(self,movie):
        print(movie)

        agent_name=None

        if self.currentuser_username=='admin':
            agent_name='admin'
        elif self.currentuser_username=='salesperson':
            agent_name='salesperson'
        else:
            agent_name=self.currentuser_username


        #get name
        name=self.adminpage_book_movie_all_movies_tab_movies_details_frame_name_entry.get()
        #get gmail
        gmail=self.adminpage_book_movie_all_movies_tab_movies_details_frame_gmail_entry.get()
        #get no.of seats
        no_of_seats=self.adminpage_book_movie_all_movies_tab_movies_details_frame_no_of_seats_entry.get()
        #get total price
        total_price=self.adminpage_book_movie_all_movies_tab_movies_details_frame_total_price_entry.get()

        #validate name
        if len(name)==0:
            messagebox.showerror("Error", "Name cannot be empty")
            return
        
        #validate gmail
        if len(gmail)==0:
            messagebox.showerror("Error", "Gmail cannot be empty")
            return
        
        #validate no.of seats
        if len(no_of_seats)==0:
            messagebox.showerror("Error", "No.of Seats cannot be empty")
            return
        
        #validate total price
        if len(total_price)==0:
            messagebox.showerror("Error", "Total Price cannot be empty")
            return
        
        
        #validate no.of seats
        if int(no_of_seats)<1:
            messagebox.showerror("Error", "No.of Seats cannot be less than 1")
            return
        
        #validate gmail
        if not gmail.endswith("@gmail.com"):
            messagebox.showerror("Error", "Gmail must end with @gmail.com")
            return
        
        movie_id=list(movie)[0]
        user_id=None
        
        #check if user exists with gmail of not create one
        conn = mysql.connector.connect(**mysql_database)
        c=conn.cursor()
        c.execute("SELECT * FROM showtime.users WHERE gmail=%s", (gmail,))
        if not c.fetchone():
            c.execute("INSERT INTO showtime.users (username,gmail) VALUES (%s,%s)", (name,gmail,))
        #get recently created user id
        c.execute("SELECT user_id FROM showtime.users WHERE gmail=%s", (gmail,))
        user_id=c.fetchone()[0]
        conn.commit()

        agent_mail=None
        if agent_name=='admin':
            agent_mail='admin'
        else:
            #get agent mail from current user
            agent_mail=self.current_user_gmail
       
        #insert into bookings table
        c.execute("INSERT INTO showtime.bookings (movie_id,user_id,username,gmail,no_of_seats,total_price,agent_mail) VALUES (%s,%s,%s,%s,%s,%s,%s)", (movie_id,user_id,name,gmail,no_of_seats,total_price,agent_mail,))
        #update movie seats
        c.execute("UPDATE showtime.movies SET seats=seats-%s WHERE movie_id=%s", (no_of_seats, movie_id))

        #get recently created booking id
        c.execute("SELECT booking_id FROM showtime.bookings WHERE movie_id=%s AND user_id=%s", (movie_id, user_id))
        booking_id=c.fetchone()[0]

        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Movie Booked Successfully")
        self.booking_confirmation_page(booking_id)

    #booking_confirmation_page
    def booking_confirmation_page(self, booking_id):
        #open new window
        self.bookingconfirmationpage=tk.Toplevel(self.root) 
        self.bookingconfirmationpage.title("Booking Confirmation")
        self.bookingconfirmationpage.geometry("500x700")
        
        #get movie details from booking id
        conn = mysql.connector.connect(**mysql_database)
        c=conn.cursor()
        c.execute("SELECT * FROM showtime.bookings WHERE booking_id=%s", (booking_id,))
        booking_details=c.fetchone()[1]
        c.execute("SELECT * FROM showtime.movies WHERE movie_id=%s", (booking_details,))
        movie_details=c.fetchone()
        conn.commit()
        conn.close()
    

        #display unique qr code with the booking details
        #get booking details
        conn = mysql.connector.connect(**mysql_database)
        c=conn.cursor()
        c.execute("SELECT * FROM showtime.bookings WHERE booking_id=%s", (booking_id,))
        booking_details=c.fetchone()
        conn.commit()
        conn.close()
        
        #create qr code
        qr_code = pyqrcode.create(booking_details[0])
        #image name as booking id and store in bookings folder
        qr_code.png(f"bookings/{booking_details[0]}.png", scale=8)
        #save qr code image path in variable
        qr_code_image_path=f"bookings/{booking_details[0]}.png"
        #display qr code
        self.bookingconfirmationpage_qr_code_image=ImageTk.PhotoImage(Image.open(qr_code_image_path))
        self.bookingconfirmationpage_qr_code_image_label=tk.Label(self.bookingconfirmationpage, image=self.bookingconfirmationpage_qr_code_image)
        self.bookingconfirmationpage_qr_code_image_label.pack(padx=10, pady=10)

        #display booking details
        self.bookingconfirmationpage_booking_details_frame=tk.Frame(self.bookingconfirmationpage)
        self.bookingconfirmationpage_booking_details_frame.pack(padx=10, pady=10)

        movie_name=movie_details[1]
        movie_date=movie_details[4]
        movie_time=movie_details[5]
        name=booking_details[3]
        movie_seats=booking_details[5]
        movie_total_price=booking_details[6]

        #insert movie name into label as "Movie Name : movie_name"
        self.bookingconfirmationpage_booking_details_frame_movie_name=tk.Label(self.bookingconfirmationpage_booking_details_frame, text=f"Movie Name : {movie_name}", font=("Arial", 15))
        self.bookingconfirmationpage_booking_details_frame_movie_name.grid(row=0, column=0, padx=5, pady=5)

        #insert movie date into label as "Movie Date : movie_date"
        self.bookingconfirmationpage_booking_details_frame_movie_date=tk.Label(self.bookingconfirmationpage_booking_details_frame, text=f"Movie Date : {movie_date}", font=("Arial", 15))
        self.bookingconfirmationpage_booking_details_frame_movie_date.grid(row=1, column=0, padx=5, pady=5)

        #insert movie time into label as "Movie Time : movie_time"
        self.bookingconfirmationpage_booking_details_frame_movie_time=tk.Label(self.bookingconfirmationpage_booking_details_frame, text=f"Movie Time : {movie_time}", font=("Arial", 15))
        self.bookingconfirmationpage_booking_details_frame_movie_time.grid(row=2, column=0, padx=5, pady=5)

        #insert name into label as "Name : name"
        self.bookingconfirmationpage_booking_details_frame_name=tk.Label(self.bookingconfirmationpage_booking_details_frame, text=f"Name : {name}", font=("Arial", 15))
        self.bookingconfirmationpage_booking_details_frame_name.grid(row=3, column=0, padx=5, pady=5)

        #insert movie seats into label as "Movie Seats : movie_seats"
        self.bookingconfirmationpage_booking_details_frame_movie_seats=tk.Label(self.bookingconfirmationpage_booking_details_frame, text=f"Movie Seats : {movie_seats}", font=("Arial", 15))
        self.bookingconfirmationpage_booking_details_frame_movie_seats.grid(row=4, column=0, padx=5, pady=5)

        #insert movie total price into label as "Movie Total Price : movie_total_price"
        self.bookingconfirmationpage_booking_details_frame_movie_total_price=tk.Label(self.bookingconfirmationpage_booking_details_frame, text=f"Movie Total Price : {movie_total_price}", font=("Arial", 15))
        self.bookingconfirmationpage_booking_details_frame_movie_total_price.grid(row=5, column=0, padx=5, pady=5)


        #back to home button
        #destroy booking confirmation page and show homepage
        self.bookingconfirmationpage_back_to_home_button=tk.Button(self.bookingconfirmationpage, text="Back To Home", font=("Arial", 15), command=lambda: [self.bookingconfirmationpage.destroy(),self.admin_page()])
        self.bookingconfirmationpage_back_to_home_button.pack(padx=10, pady=10)





    #registerUserSalesperson
    def registerUserSalesperson(self):
       #get detials from salesperson register page
        username=self.adminpage_salesperson_add_salesperson_username_entry.get()
        gmail=self.adminpage_salesperson_add_salesperson_email_entry.get()
        firstname=self.adminpage_salesperson_add_salesperson_first_name_entry.get()
        lastname=self.adminpage_salesperson_add_salesperson_last_name_entry.get()
        password=self.adminpage_salesperson_add_salesperson_password_entry.get()

       
        
        #check if user already exists
        conn = mysql.connector.connect(**mysql_database)
        c=conn.cursor()
        c.execute("SELECT * FROM showtime.users WHERE username=%s", (username,))
        if c.fetchone():
            messagebox.showerror("Error", "User already exists")
            return
        
        #check if gmail already exists
        c.execute("SELECT * FROM showtime.users WHERE gmail=%s", (gmail,))
        if c.fetchone():
            messagebox.showerror("Error", "Gmail already exists")
            return

        role='salesperson'
        #insert into users table
        c.execute("INSERT INTO showtime.users (username, gmail, firstname, lastname, password, role) VALUES (%s, %s, %s, %s, %s, %s)", (username, gmail, firstname, lastname, password, role))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Salesperson Created Successfully")
        self.admin_page()

        


    def movie_reports_print_as_pdf(self):
        # Get movie details from the database
        conn = mysql.connector.connect(**mysql_database)
        c = conn.cursor()
        c.execute("SELECT * FROM showtime.movies")
        movies = c.fetchall()
        conn.commit()
        conn.close()

        # Create a new PDF object
        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()

        # Add a title to the page
        pdf.set_font("Arial", size=20)
        pdf.cell(200, 10, txt="Movie Reports", ln=1, align="C")

        # Add a header to the table
        pdf.set_font("Arial", size=12)
        pdf.cell(45, 10, txt="Title", border=1)
        pdf.cell(45, 10, txt="Release Date", border=1)
        pdf.cell(45, 10, txt="Show Date", border=1)
        pdf.cell(45, 10, txt="Show Time", border=1)
        pdf.cell(45, 10, txt="Available Seats", border=1)
        pdf.cell(45, 10, txt="Price", border=1)
        pdf.ln()

        # Add movie data to the table
        for movie in movies:
            title = movie[1]
            release_date = movie[2].strftime("%d-%m-%Y")
            #convert release date to string
            release_date=str(release_date)
            show_date = movie[4].strftime("%d-%m-%Y")
            #convert show date to string
            show_date=str(show_date)
            #time is of 19:30:00 format
            show_time = self.format_timedelta(movie[5])
            seats = str(movie[6])
            price = str(movie[7])

            pdf.cell(45, 10, txt=title, border=1)
            pdf.cell(45, 10, txt=release_date, border=1)
            pdf.cell(45, 10, txt=show_date, border=1)
            pdf.cell(45, 10, txt=show_time, border=1)
            pdf.cell(45, 10, txt=seats, border=1)
            pdf.cell(45, 10, txt=price, border=1)

            pdf.ln()

        # Save the PDF with today's date in the "reports" folder
        today_date = datetime.now().strftime("%d_%m_%Y")
        pdf.output(f"reports/movies_{today_date}.pdf")

        messagebox.showinfo("Success", "Movie Reports Printed Successfully")
        self.admin_page()

    #formated time
    def format_timedelta(self,td):
        hours, remainder = divmod(td.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{td.microseconds // 1000:02}"



    #users_reports_print_as_pdf
    def users_reports_print_as_pdf(self):
        # Get user details from the database
        conn = mysql.connector.connect(**mysql_database)
        c = conn.cursor()
        c.execute("SELECT * FROM showtime.users")
        users = c.fetchall()
        conn.commit()
        conn.close()

        # Create a new PDF object
        pdf = FPDF(unit='mm', format='A4')
        pdf.add_page()

        # Add a title to the page
        pdf.set_font("Arial", size=20)
        pdf.cell(200, 10, txt="User Reports", ln=1, align="C")

        # Add a header to the table
        pdf.set_font("Arial", size=12)
        pdf.cell(50, 10, txt="Username", border=1)
        pdf.cell(50, 10, txt="Gmail", border=1)
        pdf.cell(50, 10, txt="Firstname", border=1)
        pdf.cell(50, 10, txt="Lastname", border=1)
        pdf.ln()

        # Add user data to the table
        for user in users:
            username = user[0]
            gmail = user[1]
            firstname = user[2]
            lastname = user[3]

            pdf.cell(50, 10, txt=username, border=1)
            pdf.cell(50, 10, txt=gmail, border=1)
            pdf.cell(50, 10, txt=firstname, border=1)
            pdf.cell(50, 10, txt=lastname, border=1)
            pdf.ln()

        # Save the PDF with today's date in the "reports" folder
        today_date = datetime.now().strftime("%d_%m_%Y")
        pdf.output(f"reports/users_{today_date}.pdf")

        messagebox.showinfo("Success", "User Reports Printed Successfully")
        self.admin_page()


        
    #bookings_reports_print_as_pdf
    def bookings_reports_print_as_pdf(self):
        # Get booking details from the database
        conn = mysql.connector.connect(**mysql_database)
        c = conn.cursor()
        c.execute("SELECT * FROM showtime.bookings")
        bookings = c.fetchall()
        conn.commit()
        conn.close()

        # Create a new PDF object
        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()

        # Add a title to the page
        pdf.set_font("Arial", size=20)
        pdf.cell(200, 10, txt="Booking Reports", ln=1, align="C")

        # Add a header to the table
        pdf.set_font("Arial", size=12)
        pdf.cell(45, 10, txt="Movie Name", border=1)
        pdf.cell(45, 10, txt="Show Date", border=1)
        pdf.cell(45, 10, txt="Name", border=1)
        pdf.cell(45, 10, txt="Gmail", border=1)
        pdf.cell(45, 10, txt="No.of Seats", border=1)
        pdf.cell(45, 10, txt="Total Price", border=1)
        pdf.ln()

        # Add booking data to the table
        for booking in bookings:
            movie_id = booking[1]
            #get movie name from movie id
            conn = mysql.connector.connect(**mysql_database)
            c = conn.cursor()
            c.execute("SELECT * FROM showtime.movies WHERE movie_id=%s", (movie_id,))
            movie = c.fetchone()
            movie_name=movie[1]
            conn.commit()
            conn.close()
            movie_date = movie[4].strftime("%d-%m-%Y")
            #convert movie date to string
            movie_date=str(movie_date)
            name = booking[3]
            gmail = booking[2]
            no_of_seats = str(booking[5])
            total_price = str(booking[6])

            pdf.cell(45, 10, txt=movie_name, border=1)
            pdf.cell(45, 10, txt=movie_date, border=1)
            pdf.cell(45, 10, txt=name, border=1)
            pdf.cell(45, 10, txt=gmail, border=1)
            pdf.cell(45, 10, txt=no_of_seats, border=1)
            pdf.cell(45, 10, txt=total_price, border=1)

            pdf.ln()

        # Save the PDF with today's date in the "reports" folder
        today_date = datetime.now().strftime("%d_%m_%Y")
        pdf.output(f"reports/bookings_{today_date}.pdf")

        messagebox.showinfo("Success", "Booking Reports Printed Successfully")
        self.admin_page()




    #get_all_movies
    def get_all_movies(self):
        conn = mysql.connector.connect(**mysql_database)
        c=conn.cursor()
        c.execute("SELECT * FROM showtime.movies")
        rows=c.fetchall()
        conn.commit()
        conn.close()
        return rows

    #upload image
    def upload_image(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select A File", filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        print(self.filename)
        #messagebox.showinfo("Success", "Image Uploaded")
        messagebox.showinfo("Success", "Image Uploaded")

        #update insert movie page image button adminpage_add_movie_image_button
        self.adminpage_add_movie_image_button.config(text="Image Uploaded")


    #display_top_trending_movies
    def display_top_trending_movies(self):
        pass

    #display_upcoming_movies
    def display_upcoming_movies(self):
        pass

    #display_recently_booked_movies
    def display_recently_booked_movies(self):
        pass



    #change_password
    def change_password(self):
        username=self.troublesigninginpage_username_entry.get()
        new_password=self.troublesigninginpage_new_password_entry.get()
        confirm_new_password=self.troublesigninginpage_confirm_new_password_entry.get()

        #validate password and include numbers and special characters
        if len(new_password)<8:
            messagebox.showerror("Error", "Password must be atleast 8 characters")
            return
        
        #check password contains numbers and special characters
        if new_password.isalpha():
            messagebox.showerror("Error", "Password must contain numbers and special characters")
            return

        #check if new password and confirm new password are same
        if new_password!=confirm_new_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        conn = mysql.connector.connect(**mysql_database)
        c=conn.cursor()
        c.execute("SELECT * FROM showtime.users WHERE username=%s", (username,))
        if c.fetchone():
            c.execute("UPDATE showtime.users SET password=%s WHERE username=%s", (new_password, username))
            messagebox.showinfo("Success", "Password changed successfully")
            self.login_page()
        else:
            messagebox.show
        conn.commit()
        conn.close()



    #remove movie from database from focus of treeview
    def remove_movie(self):
        selected_item = self.tree.focus()
        movie_details = list(self.tree.item(selected_item, 'values'))
        print(movie_details, "movie deleted")
        conn = mysql.connector.connect(**mysql_database)
        c=conn.cursor()
        c.execute("SELECT * FROM showtime.movies WHERE name=%s", (movie_details[0],))
        if c.fetchone():
            c.execute("DELETE FROM showtime.movies WHERE name=%s", (movie_details[0],))
            messagebox.showinfo("Success", "Movie Deleted successfully")
            self.admin_page()
        else:
            messagebox.showerror("Error", "Movie does not exist")
        conn.commit()
        conn.close()
        self.admin_page()
 
    def calculate_total_price(self, event):
        price=float(self.bookmoviepage_movie_price_entry.get())
        seats=int(self.bookmoviepage_no_of_seats_entry.get())
        total_price=price*seats
        self.bookmoviepage_total_price_entry.delete(0, tk.END)
        self.bookmoviepage_total_price_entry.insert(0, total_price)


    def finialize_booking(self):
        pass

    #get_movie_by_id
    def get_movie_by_id(self, movie_id):
        conn = mysql.connector.connect(**mysql_database)
        c=conn.cursor()
        c.execute("SELECT * FROM showtime.movies WHERE movie_id=%s", (movie_id,))
        movie=c.fetchone()
        conn.commit()
        conn.close()
        return movie
    

    def search_movies(self):
        search_term = self.search_entry.get()
        self.tree.delete(*self.tree.get_children())  # Clear existing entries from treeview

        movies = self.fetch_movies(search_term)
        for movie in movies:
            self.tree.insert('', 'end', values=movie[1:])

    def fetch_movies(self, search_term=""):
        conn = mysql.connector.connect(**mysql_database)
        c = conn.cursor()
        c.execute("SELECT * FROM showtime.movies WHERE name LIKE %s", (f"%{search_term}%",))
        rows = c.fetchall()
        conn.commit()
        conn.close()
        return rows




    def insert_movies_tree(self):
        self.tree.delete(*self.tree.get_children())

        conn = mysql.connector.connect(**mysql_database)
        c=conn.cursor()
        c.execute("SELECT * FROM showtime.movies")
        rows=c.fetchall()
        for row in rows:
            self.tree.insert("", tk.END, values=row)
        conn.commit()
        conn.close()


    
    def get_selected_date(self):
        selected_date = self.insertmoviepage_date_entry.get()
        self.insertmoviepage_date_entry.delete(0, tk.END)  # Clear the current entry text
        self.insertmoviepage_date_entry.insert(0, selected_date)
    
    
    def loginUser(self):
        username=self.loginpage_username_entry.get()
        password=self.loginpage_password_entry.get()
        conn = mysql.connector.connect(**mysql_database)
        c=conn.cursor()
        c.execute("SELECT * FROM showtime.users WHERE username=%s AND password=%s", (username, password))
        self.currentuser_username=username
        #gmail
        print(self.currentuser_username)
        user=c.fetchone()
        if user:
            self.current_user_gmail=user[5]
            messagebox.showinfo("Success", "Login successful")
            #check role
            if user[6]=='admin':
                self.admin_page()
            elif user[6]=='salesperson':
                self.salesperson_page()
            else:
                self.user_page()
        else:
            messagebox.showerror("Error", "Wrong username or password")
            self.login_page()
        conn.commit()
        conn.close()


    def registerUser(self):
        username=self.createaccountpage_username_entry.get()
        firstname=self.createaccountpage_firstname_entry.get()
        lastname=self.createaccountpage_lastname_entry.get()
        password=self.createaccountpage_password_entry.get()
        gmail=self.createaccountpage_gmail_entry.get()

        #validate username
        if len(username)<4:
            messagebox.showerror("Error", "Username must be atleast 4 characters")
            return
        
        #validate password and include numbers and special characters
        if len(password)<8:
            messagebox.showerror("Error", "Password must be atleast 8 characters")
            return
        
        #check password contains numbers and special characters
        if password.isalpha():
            messagebox.showerror("Error", "Password must contain numbers and special characters")
            return

        #validate email contains @ and ends with .com
        if gmail.find("@")==-1 or gmail.find(".com")==-1:
            messagebox.showerror("Error", "Enter a valid email address")
            return

        conn = mysql.connector.connect(**mysql_database)
        c=conn.cursor()
        c.execute("SELECT * FROM showtime.users WHERE username=%s", (username,))
        if c.fetchone():
            messagebox.showerror("Error", "Username already exists")
        else:
            c.execute("INSERT INTO users (username, firstname, lastname, password, gmail) VALUES (%s, %s, %s, %s, %s)", (username, firstname, lastname, password, gmail))
            messagebox.showinfo("Success", "Account created successfully")
            self.login_page()
        conn.commit()
        conn.close()

    
    #insert movie into database
    def insert_movie_db(self):
        name=self.adminpage_add_movie_name_entry.get()
        date=datetime.strptime(self.adminpage_add_movie_date_entry.get(), "%m/%d/%y").date()
        time=datetime.strptime(self.adminpage_add_movie_time_combobox.get(), "%I:%M %p").time()
        seats=int(self.adminpage_add_movie_seats_entry.get())
        price=float(self.adminpage_add_movie_price_entry.get())
        image_path=self.filename
        release_date=datetime.strptime(self.adminpage_add_movie_release_date_entry.get(), "%m/%d/%y").date()

        # print(name, date, time, seats, price)
        # print(type(name), type(date), type(time), type(seats), type(price))
        conn = mysql.connector.connect(**mysql_database)
        conn.autocommit=True
        c=conn.cursor()
        c.execute("SELECT * FROM showtime.movies WHERE name=%s", (name,))
        if c.fetchone():
            messagebox.showerror("Error", "Movie already exists")
        else:
            c.execute("INSERT INTO showtime.movies (name,release_date, date, time, seats, price, movie_image_path) VALUES (%s, %s,%s, %s, %s, %s,%s)", (name,release_date, date, time, seats, price, image_path))
            messagebox.showinfo("Success", "Movie inserted successfully")
            
            #re extract all movies
            self.extract_movies()
            self.admin_page()
        conn.close()
        # self.display_all_movies()


    #set_password
    def set_password(self,event):
        #get salesperson first name and last name
        firstname=self.adminpage_salesperson_add_salesperson_first_name_entry.get()
        lastname=self.adminpage_salesperson_add_salesperson_last_name_entry.get()

        print(firstname, lastname)

        #set password as firstname_lastname
        password=f"{firstname}_{lastname}"
        #adminpage_salesperson_add_salesperson_password_entry
        self.adminpage_salesperson_add_salesperson_password_entry.delete(0, tk.END)
        self.adminpage_salesperson_add_salesperson_password_entry.insert(0, password)

        

    #verify_user
    #verify username and email
    def verify_user(self):
        username=self.troublesigninginpage_username_entry.get()
        gmail=self.troublesigninginpage_gmail_entry.get()
        conn = mysql.connector.connect(**mysql_database)
        c=conn.cursor()
        c.execute("SELECT * FROM showtime.users WHERE username=%s AND gmail=%s", (username, gmail))
        self.current_user=c.fetchone()
        print(self.current_user)
        if self.current_user:
            messagebox.showinfo("Success", "User verified successfully")
            #enable password entry
            self.troublesigninginpage_new_password_entry.config(state="normal")
            self.troublesigninginpage_confirm_new_password_entry.config(state="normal")

            #enter new password message box
            messagebox.showinfo("Success", "Enter new password")
        
        else:
            messagebox.showerror("Error", "Wrong username or email")
        conn.commit()
        conn.close()
        
        

    def change_movie_price_db(self):
        name=self.changemoviepricepage_name_entry.get()
        price=self.changemoviepricepage_price_entry.get()
        conn = mysql.connector.connect(**mysql_database)
        c=conn.cursor()
        c.execute("SELECT * FROM showtime.movies WHERE name=%s", (name,))
        if c.fetchone():
            c.execute("UPDATE showtime.movies SET price=%s WHERE name=%s", (price, name))
            messagebox.showinfo("Success", "Price changed successfully")
            self.admin_page()
        else:
            messagebox.showerror("Error", "Movie does not exist")
        conn.commit()
        conn.close()
        self.search_movies()


    def clear_content(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__=="__main__":
    init_db()
    ShowTime()
    tk.mainloop()