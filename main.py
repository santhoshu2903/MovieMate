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
            movie text not null,
            date DATE  not null,
            time DATETIME not null,
            seats INTEGER not null,
            price float not null,
            username text
        );""")


    with sqlite3.connect(movies_db_path) as conn:
        c=conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS movies (
            name text,
            date DATE  not null,
            time DATETIME not null,
            seats INTEGER not null,
            price FLOAT not null
        );""")


    with sqlite3.connect(users_db_path) as conn:
        c=conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS users (
            username text,
            firstname text,
            lastname text,
            password text,
            gmail text
        );""")
        c.execute("INSERT INTO users VALUES ('admin', 'admin','admin')")
        c.execute("INSERT INTO users VALUES ('salesperson', 'salesperson','salesperson')")


class ShowTime:
    def __init__(self):
        super().__init__()
        self.root=tk.Tk()
        self.root.title("Welcome to CMU Movie ticket management system")
        self.root.geometry("800x700")
        self.show_homepage()

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
        self.adminpage=tk.Frame(self.root)
        self.adminpage.pack(fill="both", expand=True)
        self.adminpage.grid_rowconfigure(0, weight=1)
        self.adminpage.grid_columnconfigure(0, weight=1)

        self.adminpage_label=tk.Label(self.adminpage, text="Admin Page", font=("Arial", 20))
        self.adminpage_label.pack(pady=20)

        self.admin_page_insert_movie_button=tk.Button(self.adminpage, text="Insert Movie", font=("Arial", 15), command=self.insert_movie_page)   
        self.admin_page_insert_movie_button.pack(pady=20)

        self.admin_page_change_movie_price_button=tk.Button(self.adminpage, text="Change Movie Price", font=("Arial", 15), command=self.change_movie_price)
        self.admin_page_change_movie_price_button.pack(pady=20)

        self.admin_page_back_button=tk.Button(self.adminpage, text="Back", font=("Arial", 15), command=self.login_page)
        self.admin_page_back_button.pack(pady=20)

    def insert_movie_page(self):
        self.clear_content()
        self.insertmoviepage = tk.Frame(self.root)
        self.insertmoviepage.pack(fill="both", expand=True)
        self.insertmoviepage.grid_rowconfigure(0, weight=1)
        self.insertmoviepage.grid_columnconfigure(0, weight=1)

        self.insertmoviepage_label = tk.Label(self.insertmoviepage, text="Insert Movie", font=("Arial", 20))
        self.insertmoviepage_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Movie Name
        self.insertmoviepage_name_label = tk.Label(self.insertmoviepage, text="Movie Name", font=("Arial", 15))
        self.insertmoviepage_name_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.insertmoviepage_name_entry = tk.Entry(self.insertmoviepage, font=("Arial", 15))
        self.insertmoviepage_name_entry.grid(row=1, column=1, padx=10, pady=10,sticky='w')

        # Date
        self.insertmoviepage_date_label = tk.Label(self.insertmoviepage, text="Calendar", font=("Arial", 15))
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

        self.salespersonpage_searchbar_button=tk.Button(self.salespersonpage, text="Search", font=("Arial", 15), command=self.search_movie)
        self.salespersonpage_searchbar_button.pack(pady=10)

        self.salespersonpage_back_button=tk.Button(self.salespersonpage, text="Back", font=("Arial", 15), command=self.login_page)
        self.salespersonpage_back_button.pack(pady=10)

    def movie_page(self, name):
        self.clear_content()
        self.moviepage=tk.Frame(self.root)
        self.moviepage.pack(fill="both", expand=True)
        self.moviepage.grid_rowconfigure(0, weight=1)
        self.moviepage.grid_columnconfigure(0, weight=1)

        self.moviepage_label=tk.Label(self.moviepage, text=name, font=("Arial", 20))
        self.moviepage_label.pack(pady=20)

        self.moviepage_date_label=tk.Label(self.moviepage, text="Date", font=("Arial", 15))
        self.moviepage_date_label.pack(pady=10)

        self.moviepage_date_entry=tk.Entry(self.moviepage, font=("Arial", 15))
        self.moviepage_date_entry.pack(pady=10)

        self.moviepage_time_label=tk.Label(self.moviepage, text="Time", font=("Arial", 15))
        self.moviepage_time_label.pack(pady=10)

        self.moviepage_time_entry=tk.Entry(self.moviepage, font=("Arial", 15))
        self.moviepage_time_entry.pack(pady=10)

        self.moviepage_seats_label=tk.Label(self.moviepage, text="Seats", font=("Arial", 15))
        self.moviepage_seats_label.pack(pady=10)

        self.moviepage_seats_entry=tk.Entry(self.moviepage, font=("Arial", 15))
        self.moviepage_seats_entry.pack(pady=10)

        self.moviepage_button=tk.Button(self.moviepage, text="Book", font=("Arial", 15), command=self.book_movie)
        self.moviepage_button.pack(pady=10)

        self.moviepage_back_button=tk.Button(self.moviepage, text="Back", font=("Arial", 15), command=self.salesperson_page)
        self.moviepage_back_button.pack(pady=10)

        self.moviepage_back_login_button=tk.Button(self.moviepage, text="Back to Login", font=("Arial", 15), command=self.login_page)
        self.moviepage_back_login_button.pack(pady=10)


#Controller=======================================================================================================================================================================

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

        else:
            messagebox.showerror("Error", "Wrong username or password")
            self.login_page()
        conn.commit()
        conn.close()


    def registerUser(self):
        username=self.createaccountpage_username_entry.get()
        password=self.createaccountpage_password_entry.get()
        gmail=self.createaccountpage_gmail_entry.get()
        conn=sqlite3.connect(users_db_path)
        c=conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        if c.fetchone():
            messagebox.showerror("Error", "Username already exists")
        else:
            c.execute("INSERT INTO users VALUES (?, ?, ?)", (username, password, gmail))
            messagebox.showinfo("Success", "Account created successfully")
            self.login_page()
        conn.commit()
        conn.close()

    
    def insert_movie_db(self):
        name=self.insertmoviepage_name_entry.get()
        date=self.insertmoviepage_date_entry.get()
        seats=self.insertmoviepage_seats_entry.get()
        price=self.insertmoviepage_price_entry.get()
        time=self.hour_combobox.get()+":"+self.minute_combobox.get()+" "+self.ampm_combobox.get()



        conn=sqlite3.connect(movies_db_path)
        c=conn.cursor()
        c.execute("SELECT * FROM movies WHERE name=?", (name,))
        if c.fetchone():
            messagebox.showerror("Error", "Movie already exists")
        else:
            c.execute("INSERT INTO movies VALUES (?, ?, ?, ?, ?)", (name, date, time, seats, price))
            messagebox.showinfo("Success", "Movie inserted successfully")
            self.admin_page()
        conn.commit()
        conn.close()

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


    def search_movie(self):
        name=self.salespersonpage_searchbar_entry.get()
        conn=sqlite3.connect(movies_db_path)
        c=conn.cursor()
        c.execute("SELECT * FROM movies WHERE name=?", (name,))
        if c.fetchone():
            self.movie_page(name)
        else:
            messagebox.showerror("Error", "Movie does not exist")
        conn.commit()
        conn.close()
        

    def book_movie(self):
        name=self.moviepage_label.cget("text")
        date=self.moviepage_date_entry.get()
        time=self.moviepage_time_entry.get()
        seats=self.moviepage_seats_entry.get()
        price=self.moviepage_price_entry.get()
        conn=sqlite3.connect(bookings_db_path)
        c=conn.cursor()
        c.execute("SELECT * FROM bookings WHERE movie=? AND date=? AND time=?", (name, date, time))
        if c.fetchone():
            messagebox.showerror("Error", "Movie already booked")
        else:
            c.execute("INSERT INTO bookings VALUES (?, ?, ?, ?, ?, ?)", (name, date, time, seats, price, "salesperson"))
            messagebox.showinfo("Success", "Movie booked successfully")
            self.salesperson_page()
        conn.commit()
        conn.close()

    def clear_content(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__=="__main__":
    init_db()
    ShowTime()
    tk.mainloop()