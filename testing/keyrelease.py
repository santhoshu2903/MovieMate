import tkinter as tk

root = tk.Tk()

entry = tk.Entry(root)

entry.bind("<KeyRelease>", lambda event: print("Key released:", event.key))

entry.pack()

root.mainloop()
