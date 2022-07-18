import tkinter as tk
from tkinter import ttk

root = tk.Tk()

mytext = tk.StringVar(value='test ' * 30)

myframe = ttk.Frame(root)
myentry = ttk.Entry(myframe, textvariable=mytext, state='readonly')
myscroll = ttk.Scrollbar(myframe, orient='horizontal', command=myentry.xview)
myentry.config(xscrollcommand=myscroll.set)

myframe.grid()
myentry.grid(row=1, sticky='ew')
myscroll.grid(row=2, sticky='ew')

root.mainloop()