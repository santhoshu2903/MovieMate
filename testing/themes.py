from tkinter import ttk  # Normal Tkinter.* widgets are not themed!
from ttkthemes import ThemedTk

window = ThemedTk(theme="adapta")


#add a notebook
notebook = ttk.Notebook(window)
notebook.pack(fill='both', expand='yes')

#add a tab
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text='Tab1')

#add another tab
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text='Tab2')

ttk.Button(window, text="Quit", command=window.destroy).pack()
window.mainloop()
