import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
from tkinter import filedialog
from tkinter import font
import sqlite3
import os
import sys


users_db_path=os.path.join(os.getcwd(), "users.db")
bookings_db_path=os.path.join(os.getcwd(), "bookings.db")
movies_db_path=os.path.join(os.getcwd(), "movies.db")





def init_db():
    with sqlite3.connect(bookings_db_path) as conn:
        c=conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS bookings (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_id INTEGER not null,
            no_of_seats INTEGER not null,
            total_price float not null,
            username text
        );""")


    with sqlite3.connect(movies_db_path) as conn:
        c=conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS movies (
            movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name text,
            date DATE  not null,
            time DATETIME not null,
            seats INTEGER not null,
            price FLOAT not null
        );""")


    with sqlite3.connect(users_db_path) as conn:
        c=conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username text,
            firstname text,
            lastname text,
            password text,
            gmail text
        );""")



class ShowTime:
    def __init__(self):
        super().__init__()
        self.root=tk.Tk()
        self.root.title("Welcome to CMU Movie ticket management system")
        self.root.geometry("800x600")
        self.show_homepage()

        # Create a custom style for the Treeview
        self.style = ttk.Style()
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

    def show_homepage(self):
        self.clear_content()
        self.homepage=tk.Frame(self.root)
        self.homepage.pack(fill="both", expand=True)
        self.homepage.grid_rowconfigure(0, weight=1)
        self.homepage.grid_columnconfigure(0, weight=1)

        self.homepage_label=tk.Label(self.homepage, text="Start Booking, It's Show Time", font=("Arial", 20))
        self.homepage_label.pack(pady=20)

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

        self.create_account_button=tk.Button(self.loginpage, text="Not a User??..SIGN UP", font=("Arial", 15), command=self.create_account)
        self.create_account_button.pack(pady=10)

    def create_account(self):
        self.clear_content()
        self.root.geometry("700x800")
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


        self.createaccountpage_gmail_label=tk.Label(self.createaccountpage, text="Gmail", font=("Arial", 15))
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
        self.root.geometry("800x600")
        self.adminpage=tk.Frame(self.root)
        self.adminpage.pack(fill="both", expand=True)
        self.adminpage.grid_rowconfigure(0, weight=1)
        self.adminpage.grid_columnconfigure(0, weight=1)

        self.adminpage_label=tk.Label(self.adminpage, text="Admin Page", font=("Arial", 20))
        self.adminpage_label.grid(row=0, column=0, columnspan=4, pady=0)
        # self.adminpage_label.pack(pady=20)

        self.search_label = tk.Label(self.adminpage, text="Search Movie:")
        self.search_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.search_entry = tk.Entry(self.adminpage)
        self.search_entry.grid(row=1, column=1, padx=10, pady=10, sticky='e')
        self.search_button = tk.Button(self.adminpage, text="Search", command=self.search_movies)
        self.search_button.grid(row=1, column=2, padx=10, pady=10, sticky='w')

        self.adminpage_functions_frame = tk.Frame(self.adminpage)
        self.adminpage_functions_frame.grid(row=2, column=0, pady=0)
        self.adminpage_functions_frame.grid_rowconfigure(0, weight=1)
        self.adminpage_functions_frame.grid_columnconfigure(0, weight=1)

        self.admin_page_insert_movie_button = tk.Button(self.adminpage_functions_frame, text="Insert Movie", font=("Arial", 15), command=self.insert_movie_page)
        self.admin_page_insert_movie_button.grid(row=0, column=0, pady=20,padx=20)

        self.admin_page_change_movie_price_button = tk.Button(self.adminpage_functions_frame, text="Change Movie Price", font=("Arial", 15), command=self.change_movie_price)
        self.admin_page_change_movie_price_button.grid(row=0, column=1, pady=20,    padx=20)

        self.admin_page_book_ticket_button = tk.Button(self.adminpage_functions_frame, text="Book Ticket", font=("Arial", 15), command=self.book_movie_page)
        self.admin_page_book_ticket_button.grid(row=0, column=2, pady=20,  padx=20)

        self.admin_page_back_button = tk.Button(self.adminpage, text="Back", font=("Arial", 15), command=self.login_page)
        self.admin_page_back_button.grid(row=6, column=0, pady=20)

        # Create a Treeview widget for movie list
        self.tree = ttk.Treeview(self.adminpage, columns=("Name", "Date", "Time", "Seats", "Price"), show="headings",style="Treeview")
        self.tree.heading("Name", text="Movie Name")
        self.tree.column("Name", width=150,anchor='center')
        self.tree.heading("Date", text="Date")
        self.tree.column("Date", width=150,anchor='center')
        self.tree.heading("Time", text="Time")
        self.tree.column("Time", width=150,anchor='center')
        self.tree.heading("Seats", text="Seats")
        self.tree.column("Seats", width=150,anchor='center')
        self.tree.heading("Price", text="Price")
        self.tree.column("Price", width=150,anchor='center')
        self.tree.grid(row=3, column=0, columnspan=4, padx=10, pady=10) 

        # self.tree.bind("<ButtonRelease-1>", self.book_movie_page)
        
        # Populate the Treeview with movie data
        self.search_movies()

        self.admin_page_back_button = tk.Button(self.adminpage, text="Back", font=("Arial", 15), command=self.login_page)
        self.admin_page_back_button.grid(row=6, column=0, pady=20)

    def insert_movie_page(self):
        self.clear_content()
        self.insertmoviepage = tk.Frame(self.root)
        self.insertmoviepage.pack(fill="both", expand=True)
        self.insertmoviepage.grid_rowconfigure(0, weight=1)
        self.insertmoviepage.grid_columnconfigure(0, weight=1)

        self.insertmoviepage_label = tk.Label(self.insertmoviepage, text="Insert Movie", font=("Arial", 20))
        self.insertmoviepage_label.grid(row=0, column=0, columnspan=2, pady=0)

        # Movie Name
        self.insertmoviepage_name_label = tk.Label(self.insertmoviepage, text="Movie Name", font=("Arial", 15))
        self.insertmoviepage_name_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.insertmoviepage_name_entry = tk.Entry(self.insertmoviepage, font=("Arial", 15))
        self.insertmoviepage_name_entry.grid(row=1, column=1, padx=10, pady=10,sticky='w')

        # Date
        self.insertmoviepage_date_label = tk.Label(self.insertmoviepage, text="Date", font=("Arial", 15))
        self.insertmoviepage_date_label.grid(row=2, column=0, padx=10, pady=10, sticky='w')

        self.insertmoviepage_date_entry = DateEntry(self.insertmoviepage, width=18,background="darkblue", foreground="white", date_pattern="MM/dd/yyyy", font=("Arial", 15))
        self.insertmoviepage_date_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        

        # Time
        self.insertmoviepage_time_frame=tk.Frame(self.insertmoviepage)
        self.insertmoviepage_time_frame.grid(row=3, column=1, padx=10, pady=10, sticky='w')
        self.insertmoviepage_time_frame.grid_rowconfigure(0, weight=1)
        self.insertmoviepage_time_frame.grid_columnconfigure(0, weight=1)

        self.hour_combobox = ttk.Combobox(self.insertmoviepage_time_frame, values=["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"],font=("Arial", 15))
        self.hour_combobox.set("01")
        self.hour_combobox.config(width=4)
        self.hour_combobox.grid(row=0, column=1, padx=(0, 5))

        self.minute_combobox = ttk.Combobox(self.insertmoviepage_time_frame, values=["00", "15", "30", "45"],font=("Arial", 15))
        self.minute_combobox.set("00")
        self.minute_combobox.config(width=4)
        self.minute_combobox.grid(row=0, column=2, padx=5)

        self.ampm_combobox = ttk.Combobox(self.insertmoviepage_time_frame, values=["AM", "PM"],font=("Arial", 15))
        self.ampm_combobox.set("AM")
        self.ampm_combobox.config(width=4)
        self.ampm_combobox.grid(row=0, column=3, padx=(5, 0))


        self.insertmoviepage_time_label = tk.Label(self.insertmoviepage, text="Time", font=("Arial", 15))  
        self.insertmoviepage_time_label.grid(row=3, column=0, padx=10, pady=10, sticky='w')
        
        # Total Number of Seats Available
        self.insertmoviepage_seats_label = tk.Label(self.insertmoviepage, text="Total Number of Seats Available", font=("Arial", 15))
        self.insertmoviepage_seats_label.grid(row=4, column=0, padx=10, pady=10, sticky='w')
        self.insertmoviepage_seats_entry = tk.Entry(self.insertmoviepage, font=("Arial", 15))
        self.insertmoviepage_seats_entry.grid(row=4, column=1, padx=10, pady=10,    sticky='w')

        # Price
        self.insertmoviepage_price_label = tk.Label(self.insertmoviepage, text="Price ( USD Per Seat)", font=("Arial", 15))
        self.insertmoviepage_price_label.grid(row=5, column=0, padx=10, pady=10, sticky='w')
        self.insertmoviepage_price_entry = tk.Entry(self.insertmoviepage, font=("Arial", 15))
        self.insertmoviepage_price_entry.grid(row=5, column=1, padx=10, pady=10, sticky='w')

        self.insertmoviepage_button = tk.Button(self.insertmoviepage, text="Insert Movie", font=("Arial", 15), command=self.insert_movie_db)
        self.insertmoviepage_button.grid(row=6, column=0, columnspan=2, pady=10)


        self.insertmoviepage_back_button = tk.Button(self.insertmoviepage, text="Back", font=("Arial", 15), command=self.admin_page)
        self.insertmoviepage_back_button.grid(row=7, column=0, columnspan=2, pady=10)

        self.insertmoviepage_back_login_button = tk.Button(self.insertmoviepage, text="Back to Login", font=("Arial", 15), command=self.login_page)
        self.insertmoviepage_back_login_button.grid(row=8, column=0, columnspan=2, pady=10)

    
    #book movie page
    #consists of movie details and booking details
    #consists of user who is booking the ticket and number of seats they want to buy
    #seller name, admin or salesperson or user himself
    def book_movie_page(self):
        # get movie details from tree focus
        selected_item = self.tree.focus()
        movie_details = list(self.tree.item(selected_item, 'values'))
        print(movie_details)
        self.clear_content()
        #display movie details and ask for number of seats to book side by side
        self.bookmoviepage=tk.Frame(self.root)
        self.bookmoviepage.pack(fill="both", expand=True)

        self.bookmoviepage.grid_rowconfigure(0, weight=1)
        self.bookmoviepage.grid_columnconfigure(0, weight=1)

        #Book Movie Page Label

        # self.bookmoviepage_label=tk.Label(self.bookmoviepage, text="Book Movie", font=("Arial", 20))
        # self.bookmoviepage_label.pack(pady=20)


        #label and entry side by side
        self.bookmoviepage_movie_name_label=tk.Label(self.bookmoviepage, text="Movie Name", font=("Arial", 15))
        self.bookmoviepage_movie_name_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        self.bookmoviepage_movie_name_entry=tk.Entry(self.bookmoviepage, font=("Arial", 15))
        self.bookmoviepage_movie_name_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        self.bookmoviepage_movie_date_label=tk.Label(self.bookmoviepage, text="Date", font=("Arial", 15))
        self.bookmoviepage_movie_date_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        self.bookmoviepage_movie_date_entry=tk.Entry(self.bookmoviepage, font=("Arial", 15))
        self.bookmoviepage_movie_date_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        self.bookmoviepage_movie_time_label=tk.Label(self.bookmoviepage, text="Time", font=("Arial", 15))
        self.bookmoviepage_movie_time_label.grid(row=2, column=0, padx=10, pady=10, sticky='w')

        self.bookmoviepage_movie_time_entry=tk.Entry(self.bookmoviepage, font=("Arial", 15))
        self.bookmoviepage_movie_time_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')

        self.bookmoviepage_movie_price_label=tk.Label(self.bookmoviepage, text="Price ( USD Per Seat)", font=("Arial", 15))
        self.bookmoviepage_movie_price_label.grid(row=3, column=0, padx=10, pady=10, sticky='w')

        self.bookmoviepage_movie_price_entry=tk.Entry(self.bookmoviepage, font=("Arial", 15))
        self.bookmoviepage_movie_price_entry.grid(row=3, column=1, padx=10, pady=10, sticky='w')

        self.bookmoviepage_no_of_seats_label=tk.Label(self.bookmoviepage, text="Number of Seats", font=("Arial", 15))
        self.bookmoviepage_no_of_seats_label.grid(row=4, column=0, padx=10, pady=10, sticky='w')

        self.bookmoviepage_no_of_seats_entry=tk.Entry(self.bookmoviepage, font=("Arial", 15))
        self.bookmoviepage_no_of_seats_entry.grid(row=4, column=1, padx=10, pady=10, sticky='w')

        self.bookmoviepage_total_price_label=tk.Label(self.bookmoviepage, text="Total Price", font=("Arial", 15))
        self.bookmoviepage_total_price_label.grid(row=5, column=0, padx=10, pady=10, sticky='w')

        self.bookmoviepage_total_price_entry=tk.Entry(self.bookmoviepage, font=("Arial", 15))
        self.bookmoviepage_total_price_entry.grid(row=5, column=1, padx=10, pady=10, sticky='w')

        #fill movie details from tree focus
        self.bookmoviepage_movie_name_entry.insert(0, movie_details[0])
        self.bookmoviepage_movie_date_entry.insert(0, movie_details[1])
        self.bookmoviepage_movie_time_entry.insert(0, movie_details[2])
        self.bookmoviepage_movie_price_entry.insert(0, movie_details[4])

        #calculate total price
        self.bookmoviepage_no_of_seats_entry.bind("<KeyRelease>", self.calculate_total_price)




        self.bookmoviepage_button=tk.Button(self.bookmoviepage, text="Book Movie", font=("Arial", 15), command=self.finialize_booking)
        self.bookmoviepage_button.grid(row=6, column=0, columnspan=2, pady=10)

        self.bookmoviepage_back_button=tk.Button(self.bookmoviepage, text="Back", font=("Arial", 15), command=self.admin_page)
        self.bookmoviepage_back_button.grid(row=7, column=0, columnspan=2, pady=10)

        self.bookmoviepage_back_login_button=tk.Button(self.bookmoviepage, text="Back to Login", font=("Arial", 15), command=self.login_page)
        self.bookmoviepage_back_login_button.grid(row=8, column=0, columnspan=2, pady=10)








    
    def change_movie_price(self):
        self.clear_content()
        self.changemoviepricepage=tk.Frame(self.root)
        self.changemoviepricepage.pack(fill="both", expand=True)
        self.changemoviepricepage.grid_rowconfigure(0, weight=1)
        self.changemoviepricepage.grid_columnconfigure(0, weight=1)

        self.changemoviepricepage_label=tk.Label(self.changemoviepricepage, text="Change Movie Price", font=("Arial", 20))
        self.changemoviepricepage_label.pack(pady=20)

        self.changemoviepricepage_name_label=tk.Label(self.changemoviepricepage, text="Movie Name", font=("Arial", 15))
        self.changemoviepricepage_name_label.pack(pady=10)

        self.changemoviepricepage_name_entry=tk.Entry(self.changemoviepricepage, font=("Arial", 15))
        self.changemoviepricepage_name_entry.pack(pady=10)

        self.changemoviepricepage_price_label=tk.Label(self.changemoviepricepage, text="Price", font=("Arial", 15))
        self.changemoviepricepage_price_label.pack(pady=10)

        self.changemoviepricepage_price_entry=tk.Entry(self.changemoviepricepage, font=("Arial", 15))
        self.changemoviepricepage_price_entry.pack(pady=10)

        self.changemoviepricepage_button=tk.Button(self.changemoviepricepage, text="Change Price ( USD Per Seat)", font=("Arial", 15), command=self.change_movie_price_db)
        self.changemoviepricepage_button.pack(pady=10)


        self.changemoviepricepage_back_button=tk.Button(self.changemoviepricepage, text="Back", font=("Arial", 15), command=self.admin_page)
        self.changemoviepricepage_back_button.pack(pady=10)

        self.changemoviepricepage_back_login_button=tk.Button(self.changemoviepricepage, text="Back to Login", font=("Arial", 15), command=self.login_page)
        self.changemoviepricepage_back_login_button.pack(pady=10)


    def salesperson_page(self):
        self.clear_content()
        self.salespersonpage=tk.Frame(self.root)
        self.salespersonpage.pack(fill="both", expand=True)
        self.salespersonpage.grid_rowconfigure(0, weight=1)
        self.salespersonpage.grid_columnconfigure(0, weight=1)

        self.salespersonpage_label=tk.Label(self.salespersonpage, text="Ticket Booking", font=("Arial", 20))
        self.salespersonpage_label.pack(pady=20)

        self.salespersonpage_searchbar_entry=tk.Entry(self.salespersonpage, font=("Arial", 15))
        self.salespersonpage_searchbar_entry.pack(pady=10)

        self.salespersonpage_searchbar_button=tk.Button(self.salespersonpage, text="Search", font=("Arial", 15), command=self.book_movie_page)
        self.salespersonpage_searchbar_button.pack(pady=10)

        self.salespersonpage_back_button=tk.Button(self.salespersonpage, text="Back", font=("Arial", 15), command=self.login_page)
        self.salespersonpage_back_button.pack(pady=10)





    def user_page(self):
        self.clear_content()
        self.userpage=tk.Frame(self.root)
        self.userpage.pack(fill="both", expand=True)
        self.userpage.grid_rowconfigure(0, weight=1)
        self.userpage.grid_columnconfigure(0, weight=1)

        self.userpage_label=tk.Label(self.userpage, text="Welcome to Showtime", font=("Arial", 20))
        self.userpage_label.pack(pady=20)

        self.userpage_button=tk.Button(self.userpage, text="Start", font=("Arial", 15), command=self.login_page)
        self.userpage_button.pack(pady=20)

#Controller=======================================================================================================================================================================
 
    def calculate_total_price(self, event):
        price=float(self.bookmoviepage_movie_price_entry.get())
        seats=int(self.bookmoviepage_no_of_seats_entry.get())
        total_price=price*seats
        self.bookmoviepage_total_price_entry.delete(0, tk.END)
        self.bookmoviepage_total_price_entry.insert(0, total_price)


    def finialize_booking(self):
        pass



    def search_movies(self):
        search_term = self.search_entry.get()
        self.tree.delete(*self.tree.get_children())  # Clear existing entries from treeview

        movies = self.fetch_movies(search_term)
        for movie in movies:
            self.tree.insert('', 'end', values=movie[1:])

    def fetch_movies(self, search_term=""):
        conn = sqlite3.connect(movies_db_path)
        c = conn.cursor()
        c.execute("SELECT * FROM movies WHERE name LIKE ?", (f"%{search_term}%",))
        rows = c.fetchall()
        conn.commit()
        conn.close()
        return rows




    def insert_movies_tree(self):
        self.tree.delete(*self.tree.get_children())

        conn=sqlite3.connect(movies_db_path)
        c=conn.cursor()
        c.execute("SELECT * FROM movies")
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
        conn=sqlite3.connect(users_db_path)
        c=conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        if c.fetchone():
            messagebox.showinfo("Success", "Login successful")
            if username=="admin" or username=="":
                self.admin_page()
            if username=="salesperson":
                self.salesperson_page()
            # else:
            #     self.user_page()

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

        conn=sqlite3.connect(users_db_path)
        c=conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        if c.fetchone():
            messagebox.showerror("Error", "Username already exists")
        else:
            c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", (None, username, firstname, lastname, password, gmail))
            messagebox.showinfo("Success", "Account created successfully")
            self.login_page()
        conn.commit()
        conn.close()

    
    #insert movie into database
    def insert_movie_db(self):
        name=self.insertmoviepage_name_entry.get()
        date=self.insertmoviepage_date_entry.get()
        time=self.hour_combobox.get()+":"+self.minute_combobox.get()+" "+self.ampm_combobox.get()
        seats=self.insertmoviepage_seats_entry.get()
        price=self.insertmoviepage_price_entry.get()

        conn=sqlite3.connect(movies_db_path)
        c=conn.cursor()
        c.execute("SELECT * FROM movies WHERE name=?", (name,))
        if c.fetchone():
            messagebox.showerror("Error", "Movie already exists")
        else:
            c.execute("INSERT INTO movies VALUES (?, ?, ?, ?, ?, ?)", (None, name, date, time, seats, price))
            messagebox.showinfo("Success", "Movie inserted successfully")
            self.admin_page()
        conn.commit()
        conn.close()
        self.search_movies()
        

    def change_movie_price_db(self):
        name=self.changemoviepricepage_name_entry.get()
        price=self.changemoviepricepage_price_entry.get()
        conn=sqlite3.connect(movies_db_path)
        c=conn.cursor()
        c.execute("SELECT * FROM movies WHERE name=?", (name,))
        if c.fetchone():
            c.execute("UPDATE movies SET price=? WHERE name=?", (price, name))
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