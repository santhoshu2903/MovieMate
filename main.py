import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
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
            movie text,
            date text,
            time text,
            seats text,
            price text,
            username text
        );""")


    with sqlite3.connect(movies_db_path) as conn:
        c=conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS movies (
            name text,
            date text,
            time text,
            seats text,
            price text
        );""")


    with sqlite3.connect(users_db_path) as conn:
        c=conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS users (
            username text,
            password text,
            gmail text
        );""")
        c.execute("INSERT INTO users VALUES ('admin', 'admin','admin')")


class ShowTime:
    def __init__(self):
        super().__init__()
        self.root=tk.Tk()
        self.root.title("Show Time")
        self.root.geometry("800x600")
        self.show_homepage()

    def show_homepage(self):
        self.clear_content()
        self.homepage=tk.Frame(self.root)
        self.homepage.pack(fill="both", expand=True)
        self.homepage.grid_rowconfigure(0, weight=1)
        self.homepage.grid_columnconfigure(0, weight=1)

        self.homepage_label=tk.Label(self.homepage, text="Show Time", font=("Arial", 20))
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

        self.create_account_button=tk.Button(self.loginpage, text="Create Account", font=("Arial", 15), command=self.create_account)
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
        self.insertmoviepage=tk.Frame(self.root)
        self.insertmoviepage.pack(fill="both", expand=True)
        self.insertmoviepage.grid_rowconfigure(0, weight=1)
        self.insertmoviepage.grid_columnconfigure(0, weight=1)

        self.insertmoviepage_label=tk.Label(self.insertmoviepage, text="Insert Movie", font=("Arial", 20))
        self.insertmoviepage_label.pack(pady=20)

        self.insertmoviepage_name_label=tk.Label(self.insertmoviepage, text="Movie Name", font=("Arial", 15))
        self.insertmoviepage_name_label.pack(pady=10)

        self.insertmoviepage_name_entry=tk.Entry(self.insertmoviepage, font=("Arial", 15))
        self.insertmoviepage_name_entry.pack(pady=10)

        self.insertmoviepage_date_label=tk.Label(self.insertmoviepage, text="Date", font=("Arial", 15))
        self.insertmoviepage_date_label.pack(pady=10)

        self.insertmoviepage_date_entry=tk.Entry(self.insertmoviepage, font=("Arial", 15))
        self.insertmoviepage_date_entry.pack(pady=10)

        self.insertmoviepage_time_label=tk.Label(self.insertmoviepage, text="Time", font=("Arial", 15))
        self.insertmoviepage_time_label.pack(pady=10)

        self.insertmoviepage_time_entry=tk.Entry(self.insertmoviepage, font=("Arial", 15))
        self.insertmoviepage_time_entry.pack(pady=10)

        self.insertmoviepage_seats_label=tk.Label(self.insertmoviepage, text="Seats", font=("Arial", 15))
        self.insertmoviepage_seats_label.pack(pady=10)

        self.insertmoviepage_seats_entry=tk.Entry(self.insertmoviepage, font=("Arial", 15))
        self.insertmoviepage_seats_entry.pack(pady=10)

        self.insertmoviepage_price_label=tk.Label(self.insertmoviepage, text="Price", font=("Arial", 15))
        self.insertmoviepage_price_label.pack(pady=10)

        self.insertmoviepage_price_entry=tk.Entry(self.insertmoviepage, font=("Arial", 15))
        self.insertmoviepage_price_entry.pack(pady=10)

        self.insertmoviepage_button=tk.Button(self.insertmoviepage, text="Insert Movie", font=("Arial", 15), command=self.insert_movie_db)
        self.insertmoviepage_button.pack(pady=10)

        self.insertmoviepage_back_button=tk.Button(self.insertmoviepage, text="Back", font=("Arial", 15), command=self.admin_page)
        self.insertmoviepage_back_button.pack(pady=10)

        self.insertmoviepage_back_login_button=tk.Button(self.insertmoviepage, text="Back to Login", font=("Arial", 15), command=self.login_page)
        self.insertmoviepage_back_login_button.pack(pady=10)



    
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

        self.changemoviepricepage_button=tk.Button(self.changemoviepricepage, text="Change Price", font=("Arial", 15), command=self.change_movie_price_db)
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

        self.salespersonpage_searchbar_label=tk.Label(self.salespersonpage, text="Search", font=("Arial", 15))
        self.salespersonpage_searchbar_label.pack(pady=10)

#Controller=======================================================================================================================================================================

    def loginUser(self):
        username=self.loginpage_username_entry.get()
        password=self.loginpage_password_entry.get()
        conn=sqlite3.connect(users_db_path)
        c=conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        if c.fetchone():
            messagebox.showinfo("Success", "Login successful")
            if username=="admin":
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
        time=self.insertmoviepage_time_entry.get()
        seats=self.insertmoviepage_seats_entry.get()
        price=self.insertmoviepage_price_entry.get()
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

    def clear_content(self):
        for widget in self.root.winfo_children():
            widget.destroy()









if __name__=="__main__":
    init_db()
    ShowTime()
    tk.mainloop()