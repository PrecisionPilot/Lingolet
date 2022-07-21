import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image


master = tk.Tk()
 
# this will create a label widget
l1 = tk.Label(master, text = "First:")
l2 = tk.Label(master, text = "Second:")
 
# grid method to arrange labels in respective
# rows and columns as specified
l1.grid(row = 0, column = 0, sticky = tk.W, pady = 2)
l2.grid(row = 1, column = 0, sticky = tk.W, pady = 2)
 
# entry widgets, used to take entry from user
e1 = tk.Entry(master)
e2 = tk.Entry(master)
 
# this will arrange entry widgets
e1.grid(row = 0, column = 1, pady = 2)
e2.grid(row = 1, column = 1, pady = 2)
 
# infinite loop which can be terminated by keyboard
# or mouse interrupt
tk.mainloop()