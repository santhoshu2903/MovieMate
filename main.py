import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
from tkinter import filedialog
from tkinter import font
import mysql.connector
from datetime import datetime
from time import strftime
from PIL import Image, ImageTk
import sv_ttk
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
        password VARCHAR(255),
        gmail VARCHAR(255)
    );""")

        # Create the 'bookings' table
    cursor.execute("""CREATE TABLE IF NOT EXISTS bookings (
        booking_id INT AUTO_INCREMENT PRIMARY KEY,
        movie_id INT NOT NULL,
        user_id INT NOT NULL default 0,
        no_of_seats INT NOT NULL,
        total_price FLOAT NOT NULL,
        username VARCHAR(255),
        foreign key (movie_id) references movies(movie_id),
        foreign key (user_id) references users(user_id)
    );""")

    # Commit and close the connection
    conn.commit()
    conn.close()



class ShowTime:
    def __init__(self):
        super().__init__()
        self.root=tk.Tk()
        self.root.title("Welcome to CMU Movie ticket management system")
        self.root.geometry("800x600")
        self.show_homepage()
        sv_ttk.set_theme("light")

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
        self.adminpage_label.grid(row=0, column=0, columnspan=4, pady=0,sticky='nsew')
        # self.adminpage_label.pack(pady=20)

        #notebook tabs
        self.adminpage_notebook=ttk.Notebook(self.adminpage)
        self.adminpage_notebook.grid(row=1, column=0, columnspan=4, pady=0,sticky='nsew')

        #movies details tab
        self.adminpage_movies_details_tab=tk.Frame(self.adminpage_notebook)
        self.adminpage_notebook.add(self.adminpage_movies_details_tab, text="Movies Details")

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

        #all movies tab
        self.adminpage_book_movie_all_movies_tab=tk.Frame(self.adminpage_book_movie_notebook)
        self.adminpage_book_movie_notebook.add(self.adminpage_book_movie_all_movies_tab, text="All Movies")

        #upcoming movies tab
        self.adminpage_book_movie_upcoming_movies_tab=tk.Frame(self.adminpage_book_movie_notebook)
        self.adminpage_book_movie_notebook.add(self.adminpage_book_movie_upcoming_movies_tab, text="Upcoming Movies")

        #set trending movies tab as default tab
        self.adminpage_book_movie_notebook.select(self.adminpage_book_movie_top_trending_movies_tab)

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
        self.display_all_book_movies()


        #add movie tab
        self.adminpage_add_movie_tab=tk.Frame(self.adminpage_notebook)
        self.adminpage_notebook.add(self.adminpage_add_movie_tab, text="Add Movie")

        #movie reports tab
        self.adminpage_reports_tab=tk.Frame(self.adminpage_notebook)
        self.adminpage_notebook.add(self.adminpage_reports_tab, text="Movie Reports")
        
        #users reports tab
        self.adminpage_users_reports_tab=tk.Frame(self.adminpage_notebook)
        self.adminpage_notebook.add(self.adminpage_users_reports_tab, text="Users Reports")

        #movie details tab
        self.adminpage_movies_details_tab.grid_rowconfigure(1, weight=1)
        self.adminpage_movies_details_tab.grid_columnconfigure(0, weight=1)

        #notebook inside movie details tab
        self.adminpage_movies_details_notebook=ttk.Notebook(self.adminpage_movies_details_tab)
        self.adminpage_movies_details_notebook.grid(row=1, column=0, columnspan=4, pady=0,sticky='nsew')

        #top trending movies tab
        self.adminpage_top_trending_movies_tab=tk.Frame(self.adminpage_movies_details_notebook)
        self.adminpage_movies_details_notebook.add(self.adminpage_top_trending_movies_tab, text="Top Trending Movies")

        #upcoming movies tab
        self.adminpage_upcoming_movies_tab=tk.Frame(self.adminpage_movies_details_notebook)
        self.adminpage_movies_details_notebook.add(self.adminpage_upcoming_movies_tab, text="Upcoming Movies")

        #recently booked movies tab
        self.adminpage_recently_booked_movies_tab=tk.Frame(self.adminpage_movies_details_notebook)
        self.adminpage_movies_details_notebook.add(self.adminpage_recently_booked_movies_tab, text="Recently Booked Movies")

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
        
        #get movies from database and display images
        # Connect to the MySQL server
        self.display_all_movies()

    
        #take data from admin to add movie
        #movie name label and entry side by side
        self.adminpage_add_movie_name_label=tk.Label(self.adminpage_add_movie_tab, text="Movie Name", font=("Arial", 15))
        self.adminpage_add_movie_name_label.grid(row=0, column=1, padx=20, pady=20, sticky='w')
        self.adminpage_add_movie_name_entry=tk.Entry(self.adminpage_add_movie_tab, font=("Arial", 15))
        self.adminpage_add_movie_name_entry.grid(row=0, column=2, padx=20, pady=20, sticky='w')

        #date label and entry side by side
        self.adminpage_add_movie_date_label=tk.Label(self.adminpage_add_movie_tab, text="Date", font=("Arial", 15))
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
        time=["01:00 AM", "02:00 AM", "03:00 AM", "04:00 AM", "05:00 AM", "06:00 AM", "07:00 AM", "08:00 AM", "09:00 AM", "10:00 AM", "11:00 AM"]
        self.adminpage_add_movie_time_combobox=ttk.Combobox(self.adminpage_add_movie_tab, values=time, font=("Arial", 15))
        #width of combobox
        self.adminpage_add_movie_time_combobox.config(width=18)
        self.adminpage_add_movie_time_combobox.grid(row=2, column=2, padx=20, pady=20, sticky='w')

        #seats label and entry side by side
        self.adminpage_add_movie_seats_label=tk.Label(self.adminpage_add_movie_tab, text="No.of Seats", font=("Arial", 15))
        self.adminpage_add_movie_seats_label.grid(row=3, column=1, padx=20, pady=20, sticky='w')
        self.adminpage_add_movie_seats_entry=tk.Entry(self.adminpage_add_movie_tab, font=("Arial", 15))
        self.adminpage_add_movie_seats_entry.grid(row=3, column=2, padx=20, pady=20, sticky='w')

        #price label and entry side by side
        self.adminpage_add_movie_price_label=tk.Label(self.adminpage_add_movie_tab, text="Price", font=("Arial", 15))
        self.adminpage_add_movie_price_label.grid(row=4, column=1, padx=20, pady=20, sticky='w')
        self.adminpage_add_movie_price_entry=tk.Entry(self.adminpage_add_movie_tab, font=("Arial", 15))
        self.adminpage_add_movie_price_entry.grid(row=4, column=2, padx=20, pady=20, sticky='w')

        #insert movie image button
        self.adminpage_add_movie_image_button=tk.Button(self.adminpage_add_movie_tab, text="Insert Movie Image", font=("Arial", 15), command=self.upload_image)
        self.adminpage_add_movie_image_button.grid(row=5, column=1, columnspan=2, pady=10)

        #insert movie button
        self.adminpage_add_movie_button=tk.Button(self.adminpage_add_movie_tab, text="Insert Movie", font=("Arial", 15), command=self.insert_movie_db)
        self.adminpage_add_movie_button.grid(row=6, column=1, columnspan=2, pady=10)

        #back button
        self.adminpage_add_movie_back_button=tk.Button(self.adminpage_add_movie_tab, text="Back", font=("Arial", 15), command=self.admin_page)
        self.adminpage_add_movie_back_button.grid(row=7, column=1, columnspan=2, pady=10)



    #display_all_book_movies
    def display_all_book_movies(self):
        self.all_movies=self.get_all_movies()
        #iterate one by one from all movies and display images
        for i, movie in enumerate(self.all_movies):
            #display movie image as button
            movie=list(movie)
            movie = {
                "movie_id": movie[0],
                "movie_name": movie[1],
                "movie_date": movie[2],
                "movie_time": movie[3],
                "movie_seats": movie[4],
                "movie_price": movie[5],
                "movie_image_path": movie[6]
            }
            # print(movie)
            # print(movie["movie_image_path"])
            image = Image.open(movie["movie_image_path"])
            image = image.resize((150, 200), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            row = i // 6  # integer division to get row number
            col = i % 6 # modulo operator to get column number

            #current user is admin then in admin book tab
            if self.currentuser_username=='admin':
                button = tk.Button(self.adminpage_book_movie_all_movies_tab_movies_image_canvas_frame, image=photo, command=lambda i=i: self.book_movie(i,self.adminpage_book_movie_all_movies_tab_movies_image_canvas_frame))
                button.image = photo
                button.grid(row=row, column=col, padx=5, pady=5)
            #else if sales person then in sales person book tab
            elif self.currentuser_username=='salesperson':
                button = tk.Button(self.salespersonpage_book_movie_all_movies_tab_movies_image_canvas_frame, image=photo, command=lambda i=i: self.book_movie(i,self.salespersonpage_book_movie_all_movies_tab_movies_image_canvas_frame))
                button.image = photo
                button.grid(row=row, column=col, padx=5, pady=5)
            else:
                button = tk.Button(self.userpage_book_movie_all_movies_tab_movies_image_canvas_frame, image=photo, command=lambda i=i: self.book_movie(i,self.userpage_book_movie_all_movies_tab_movies_image_canvas_frame))
                button.image = photo
                button.grid(row=row, column=col, padx=5, pady=5)




    
    #show movie details
    def show_movie_details(self, i):
        #clear all movies tab and fill movie details
        self.adminpage_all_movies_tab_movies_image_canvas_frame.destroy()
        self.adminpage_all_movies_tab_movies_image_canvas_frame=tk.Frame(self.adminpage_all_movies_tab_movies_image_canvas)
        self.adminpage_all_movies_tab_movies_image_canvas_frame.columnconfigure(0, weight=1)
        self.adminpage_all_movies_tab_movies_image_canvas.create_window((0, 0), window=self.adminpage_all_movies_tab_movies_image_canvas_frame, anchor="nw")
        #get movie details from all movies
        movie=self.all_movies[i]
        # print(movie)
        #image on the left side and movie details on the right side
        #image
        image = Image.open(movie[6])
        image = image.resize((350, 400), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        self.adminpage_all_movies_tab_movies_image_canvas_frame_image_label=tk.Label(self.adminpage_all_movies_tab_movies_image_canvas_frame, image=photo)
        self.adminpage_all_movies_tab_movies_image_canvas_frame_image_label.image = photo  # Keep a reference to avoid garbage collection
        self.adminpage_all_movies_tab_movies_image_canvas_frame_image_label.grid(row=0, column=0, padx=5, pady=5)

        # create a new frame next to the image
        self.adminpage_all_movies_tab_movies_details_frame = tk.Frame(self.adminpage_all_movies_tab_movies_image_canvas_frame)
        self.adminpage_all_movies_tab_movies_details_frame.grid(row=0, column=1, padx=5, pady=5, sticky='n')

        #movie details and details also as label
        self.adminpage_all_movies_tab_movies_details_frame_movie_name_label=tk.Label(self.adminpage_all_movies_tab_movies_details_frame,font=("Arial", 15))
        self.adminpage_all_movies_tab_movies_details_frame_movie_name_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        #configure label as "Movie Name: movie name"
        self.adminpage_all_movies_tab_movies_details_frame_movie_name_label.config(text="Movie Name: "+movie[1])

        self.adminpage_all_movies_tab_movies_details_frame_movie_date_label=tk.Label(self.adminpage_all_movies_tab_movies_details_frame,font=("Arial", 15))
        self.adminpage_all_movies_tab_movies_details_frame_movie_date_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        #configure label as "Date: movie date"
        self.adminpage_all_movies_tab_movies_details_frame_movie_date_label.config(text="Date: "+str(movie[2]))

        self.adminpage_all_movies_tab_movies_details_frame_movie_time_label=tk.Label(self.adminpage_all_movies_tab_movies_details_frame,font=("Arial", 15))
        self.adminpage_all_movies_tab_movies_details_frame_movie_time_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        #configure label as "Time: movie time"
        self.adminpage_all_movies_tab_movies_details_frame_movie_time_label.config(text="Time: "+str(movie[3]))

        self.adminpage_all_movies_tab_movies_details_frame_movie_seats_label=tk.Label(self.adminpage_all_movies_tab_movies_details_frame,font=("Arial", 15))
        self.adminpage_all_movies_tab_movies_details_frame_movie_seats_label.grid(row=3, column=0, padx=5, pady=5, sticky='w')
        #configure label as "Seats: movie seats"
        self.adminpage_all_movies_tab_movies_details_frame_movie_seats_label.config(text="Seats: "+str(movie[4]))

        self.adminpage_all_movies_tab_movies_details_frame_movie_price_label=tk.Label(self.adminpage_all_movies_tab_movies_details_frame,font=("Arial", 15))
        self.adminpage_all_movies_tab_movies_details_frame_movie_price_label.grid(row=4, column=0, padx=5, pady=5, sticky='w')

        #configure label as "Price: movie price"
        self.adminpage_all_movies_tab_movies_details_frame_movie_price_label.config(text="Price: "+str(movie[5]))  
        
        #back button
        self.adminpage_all_movies_tab_movies_details_frame_back_button=tk.Button(self.adminpage_all_movies_tab_movies_details_frame, text="Back", font=("Arial", 15), command=self.admin_page)
        self.adminpage_all_movies_tab_movies_details_frame_back_button.grid(row=5, column=0, padx=5, pady=5, sticky='w')






    #book movie
    def book_movie(self, i,frame):
        #clear admin page book movie tab all movies tab and fill movie details
        frame.destroy()
        #based on the current user display the movie details
        #if current user is admin
        canvas= None
        if self.currentuser_username=='admin':
            frame=tk.Frame(self.adminpage_book_movie_all_movies_tab_movies_image_canvas)
            canvas=self.adminpage_book_movie_all_movies_tab_movies_image_canvas
        elif self.currentuser_username=='salesperson':
            frame=tk.Frame(self.salespersonpage_book_movie_all_movies_tab_movies_image_canvas)
            canvas=self.salespersonpage_book_movie_all_movies_tab_movies_image_canvas
        else:
            frame=tk.Frame(self.userpage_book_movie_all_movies_tab_movies_image_canvas)
            canvas=self.userpage_book_movie_all_movies_tab_movies_image_canvas


        frame.columnconfigure(0, weight=1)
        canvas.create_window((0, 0), window=frame, anchor="nw")
        #get movie details from all movies
        self.movie=self.all_movies[i]
        self.current_movie_price=self.movie[5]
        # print(movie)
        #image on the left side and movie details on the right side
        #image
        image = Image.open(self.movie[6])
        image = image.resize((350, 400), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        frame_image_label=tk.Label(frame, image=photo)
        frame_image_label.image = photo  # Keep a reference to avoid garbage collection
        frame_image_label.grid(row=0, column=0, padx=5, pady=5)

        # create a new frame next to the image
        self.adminpage_book_movie_all_movies_tab_movies_details_frame = tk.Frame(frame)
        self.adminpage_book_movie_all_movies_tab_movies_details_frame.grid(row=0, column=1, padx=5, pady=5, sticky='n')

        #movie details and details also as label
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_movie_name_label=tk.Label(self.adminpage_book_movie_all_movies_tab_movies_details_frame,font=("Arial", 15))
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_movie_name_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        #configure label as "Movie Name: movie name"
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_movie_name_label.config(text="Movie Name: "+self.movie[1])

        self.adminpage_book_movie_all_movies_tab_movies_details_frame_movie_date_label=tk.Label(self.adminpage_book_movie_all_movies_tab_movies_details_frame,font=("Arial", 15))
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_movie_date_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        #configure label as "Date: movie date"
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_movie_date_label.config(text="Date: "+str(self.movie[2]))

        self.adminpage_book_movie_all_movies_tab_movies_details_frame_movie_time_label=tk.Label(self.adminpage_book_movie_all_movies_tab_movies_details_frame,font=("Arial", 15))
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_movie_time_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        #configure label as "Time: movie time"
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_movie_time_label.config(text="Time: "+str(self.movie[3]))

        self.adminpage_book_movie_all_movies_tab_movies_details_frame_movie_seats_label=tk.Label(self.adminpage_book_movie_all_movies_tab_movies_details_frame,font=("Arial", 15))
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_movie_seats_label.grid(row=3, column=0, padx=5, pady=5, sticky='w')
        #configure label as "Seats: movie seats"
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_movie_seats_label.config(text=" Available Seats: "+str(self.movie[4]))

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

        self.adminpage_book_movie_all_movies_tab_movies_details_frame_total_price_entry.insert(0, self.movie[5]*int(self.adminpage_book_movie_all_movies_tab_movies_details_frame_no_of_seats_entry.get()))

        #update total price label when no.of seats changes
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_no_of_seats_entry.bind("<KeyRelease>", self.update_total_price())

        #book movie button
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_book_movie_button=tk.Button(self.adminpage_book_movie_all_movies_tab_movies_details_frame, text="Book Movie", font=("Arial", 15), command=self.book_movie_db)
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_book_movie_button.grid(row=8, column=0, padx=5, pady=5, sticky='w')

        #back button
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_back_button=tk.Button(self.adminpage_book_movie_all_movies_tab_movies_details_frame, text="Back", font=("Arial", 15), command=self.admin_page)
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_back_button.grid(row=9, column=0, padx=5, pady=5, sticky='w')


        #logout button
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_logout_button=tk.Button(self.adminpage_book_movie_all_movies_tab_movies_details_frame, text="Logout", font=("Arial", 15), command=self.logout)
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_logout_button.grid(row=10, column=0, padx=5, pady=5, sticky='w')

        





    def salesperson_page(self):
        self.clear_content()
        self.root.geometry("1000x700")
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
        self.display_all_book_movies()






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
        self.display_all_book_movies()

        #logout button
        self.userpage_book_movie_all_movies_tab_movies_details_frame_logout_button=tk.Button(self.userpage_book_movie_all_movies_tab_movies_details_frame, text="Logout", font=("Arial", 15), command=self.logout)
        self.userpage_book_movie_all_movies_tab_movies_details_frame_logout_button.grid(row=10, column=0, padx=5, pady=5, sticky='w')





#Controller=======================================================================================================================================================================

    #update_total_price
    def update_total_price(self):
        #get no.of seats
        no_of_seats=self.adminpage_book_movie_all_movies_tab_movies_details_frame_no_of_seats_entry.get()
        #get movie price
        movie_price=self.current_movie_price
        #update total price
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_total_price_entry.delete(0, tk.END)
        self.adminpage_book_movie_all_movies_tab_movies_details_frame_total_price_entry.insert(0, float(movie_price)*int(no_of_seats))



    #book movie db
    def book_movie_db(self):
        #get movie name
        movie_name=self.adminpage_book_movie_all_movies_tab_movies_details_frame_movie_name_label.cget("text")
        movie_name=movie_name.split(": ")[1]
        #get movie date
        movie_date=self.adminpage_book_movie_all_movies_tab_movies_details_frame_movie_date_label.cget("text")
        movie_date=movie_date.split(": ")[1]
        #get movie time
        movie_time=self.adminpage_book_movie_all_movies_tab_movies_details_frame_movie_time_label.cget("text")
        movie_time=movie_time.split(": ")[1]
        #get movie seats
        movie_seats=self.adminpage_book_movie_all_movies_tab_movies_details_frame_movie_seats_label.cget("text")
        movie_seats=movie_seats.split(": ")[1]
        #get movie price
        movie_price=self.adminpage_book_movie_all_movies_tab_movies_details_frame_total_price_entry
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
        if int(no_of_seats)>int(movie_seats):
            messagebox.showerror("Error", "No.of Seats cannot be greater than available seats")
            return
        
        #validate no.of seats
        if int(no_of_seats)<1:
            messagebox.showerror("Error", "No.of Seats cannot be less than 1")
            return
        
        #validate total price
        if float(total_price)<float(movie_price):
            messagebox.showerror("Error", "Total Price cannot be less than movie price")
            return
        
        #validate total price
        if float(total_price)>float(movie_price)*int(movie_seats):
            messagebox.showerror("Error", "Total Price cannot be greater than movie price * no.of seats")
            return
        
        #validate gmail
        if not gmail.endswith("@gmail.com"):
            messagebox.showerror("Error", "Gmail must end with @gmail.com")
            return
        
        #insert into database
        conn = mysql.connector.connect(**mysql_database)
        c=conn.cursor()
        c.execute("INSERT INTO showtime.bookings (movie_name, movie_date, movie_time, movie_seats, movie_price, name, gmail, no_of_seats, total_price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (movie_name, movie_date, movie_time, movie_seats, movie_price, name, gmail, no_of_seats, total_price))



    #display all movies
    def display_all_movies(self):
        self.all_movies=self.get_all_movies()
        #iterate one by one from all movies and display images
        for i, movie in enumerate(self.all_movies):
            #display movie image as button
            movie=list(movie)
            movie = {
                "movie_id": movie[0],
                "movie_name": movie[1],
                "movie_date": movie[2],
                "movie_time": movie[3],
                "movie_seats": movie[4],
                "movie_price": movie[5],
                "movie_image_path": movie[6]
            }
            # print(movie)
            # print(movie["movie_image_path"])
            image = Image.open(movie["movie_image_path"])
            image = image.resize((150, 200), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            row = i // 6  # integer division to get row number
            col = i % 6 # modulo operator to get column number
            button = tk.Button(self.adminpage_all_movies_tab_movies_image_canvas_frame, image=photo, command=lambda i=i: self.show_movie_details(i))
            button.image = photo  # Keep a reference to avoid garbage collection
            button.grid(row=row, column=col, padx=5, pady=5)


        


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
        if c.fetchone():
            messagebox.showinfo("Success", "Login successful")
            if username=="admin" or username=="":
                self.admin_page()
            if username=="salesperson":
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

        # print(name, date, time, seats, price)
        # print(type(name), type(date), type(time), type(seats), type(price))
        conn = mysql.connector.connect(**mysql_database)
        c=conn.cursor()
        c.execute("SELECT * FROM showtime.movies WHERE name=%s", (name,))
        if c.fetchone():
            messagebox.showerror("Error", "Movie already exists")
        else:
            c.execute("INSERT INTO showtime.movies (name, date, time, seats, price, movie_image_path) VALUES (%s, %s, %s, %s, %s,%s)", (name, date, time, seats, price, image_path))
            messagebox.showinfo("Success", "Movie inserted successfully")
            self.admin_page()
        conn.commit()
        conn.close()
        self.display_all_movies()

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