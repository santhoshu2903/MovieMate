# import tkinter as tk
# from tkinter import ttk


# def add():
#     value = add_entry.get()
#     values.append(value)
#     tree.insert("", tk.END, values=(f'#{len(values)}', value, 'more', 'moar'))


# def search():
#     query = search_entry.get()
#     selections = []
#     for child in tree.get_children():
#         if query.lower() in tree.item(child)['values'].lower():   # compare strings in  lower cases.
#             print(tree.item(child)['values'])
#             selections.append(child)
#     print('search completed')
#     tree.selection_set(selections)


# values = []

# root = tk.Tk()
# root.title("Medicine database")

# lb1 = tk.Label(root, text="Search:")
# lb1.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
# search_entry = tk.Entry(root, width=15)
# search_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.E, rowspan=1)
# btn = tk.Button(root, text="search", width=10, command=search)
# btn.grid(row=0, column=0, padx=10, pady=10, rowspan=2)

# add_lb = tk.Label(root, text="add:")
# add_lb.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
# add_entry = tk.Entry(root, width=15)
# add_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.E, rowspan=1)
# btn1 = tk.Button(root, text="add", width=10, command=add)
# btn1.grid(row=1, column=0, padx=10, pady=10, rowspan=2)

# # treeview
# tree = ttk.Treeview(root, height=25)
# tree["columns"] = ("one", "two", "three", "four")
# tree.column("one", width=120)
# tree.column("two", width=160)
# tree.column("three", width=130)
# tree.column("four", width=160)
# tree.heading("one", text="Numer seryjny leku")
# tree.heading("two", text="Nazwa Leku")
# tree.heading("three", text="Ampułki/Tabletki")
# tree.heading("four", text="Data ważności")
# tree["show"]="headings"
# tree.grid(row=0, column=2, rowspan=6, pady=20)

# root.geometry("840x580")


# if __name__ == '__main__':
#     root.mainloop()




# Step 1 and Step 2:-

# import module
from sqlite3 import *

con = None

# creates/opens database
con = connect("data.db")

# create cursor(connecting user to database)  
cur = con.cursor()

# creates table
sql = "create table if not exists student(rno int primary key, name text)"
cur.execute(sql)

# database closed
if con is not None:
    con.close()

# Step 3:-

# import module
from sqlite3 import *

con = None

# create/open database
con = connect("data.db")

# connecting user to database
cur = con.cursor()

# inserting values into database
sql1 = "insert into student values(1, 'darshan')"
sql2 = "insert into student values(2, 'yogesh')"
sql3 = "insert into student values(3, 'devesh')"
sql4 = "insert into student values(4, 'sandip')"
sql5 = "insert into student values(5, 'tushar')"
sql6 = "insert into student values(6, 'raju')"
sql7 = "insert into student values(7, 'rajprasad')"

# executing sql1, sql2, sql3, sql4, sql5, sql6 & sql7
cur.execute(sql1)
cur.execute(sql2)
cur.execute(sql3)
cur.execute(sql4)
cur.execute(sql5)
cur.execute(sql6)
cur.execute(sql7)

# saving inserted data into database
con.commit()

# database closed
if con is not None:
    con.close()

# Step 4, Step 5 and Step 6:-

# Import Modules
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from sqlite3 import *


view_window = Tk()                       
view_window.title("View Student ")     # title of view_window   
view_window.geometry("750x700+400+50") # set geometry   
view_window.resizable(0, 0)            # disable maximize/minimize view_window      


def show():
    view_window_ent.delete(0, END)     
    view_window_ent.focus()
    tv.selection()
    con = None
    try:
        con = connect("data.db")    
        cursor = con.cursor()
        sql = "select * from student"   
        cursor.execute(sql)

        fetchdata = tv.get_children()       
        for elements in fetchdata:
            tv.delete(elements)
    

        data = cursor.fetchall()
        for d in data:
            tv.insert("", END, values=d)

        con.commit()
    except Exception as e:
        showerror("Fail", e)
        con.rollback()
    finally:
        if con is not None:
            con.close()
def search():
    tv.selection()
    fetchdata = tv.get_children()
    for f in fetchdata:
        tv.delete(f)
    con = None
    try:
        con = connect("data.db")
        core = con.cursor()
        sql = "select * from student where name = '%s' "
        name = view_window_ent.get()
        if (len(name) < 2) or (not name.isalpha()):
            showerror("fail", "invalid name")
        else:
            core.execute(sql %(name))
            data = core.fetchall()
            for d in data:
                tv.insert("", END, values=d)
            
    except Exception as e:
        showerror("issue", e)

    finally:
        if con is not None:
            con.close()
def reset():
    show()  


#treeview
scrollbarx = Scrollbar(view_window, orient=HORIZONTAL)  
scrollbary = Scrollbar(view_window, orient=VERTICAL)    
tv = ttk.Treeview(view_window, columns=("rollno", "name"), show='headings', height=22)  
tv.pack()
tv.heading('rollno', text="Roll No", anchor=CENTER)
tv.column("rollno", stretch=NO, width = 100) 
tv.heading('name', text="Name", anchor=CENTER)
tv.column("name", stretch=NO)
scrollbary.config(command=tv.yview)
scrollbary.place(x = 526, y = 7)
scrollbarx.config(command=tv.xview)
scrollbarx.place(x = 220, y = 460)
style = ttk.Style()
style.theme_use("default")
style.map("Treeview")


# Widgets
view_window_lbl = Label(view_window, text = "Name", font=('calibri', 12, 'normal'))
view_window_lbl.place(x = 290, y = 518)
view_window_ent = Entry(view_window,  width = 20, font=('Arial', 15, 'bold'))
view_window_ent.place(x = 220, y = 540)
view_window_btn1 = Button(view_window, text = 'Search',  width = 8, font=('calibri', 12, 'normal'), command = search)
view_window_btn1.place(x = 480, y = 540)
view_window_btn2 = Button(view_window, text = 'Reset',  width = 8, font=('calibri', 12, 'normal'), command = reset)
view_window_btn2.place(x = 600, y = 540)


show()  
view_window.mainloop()