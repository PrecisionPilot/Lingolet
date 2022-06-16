import tkinter as tk
from tkinter import ttk


window = tk.Tk()
window.title("Text Widget Example")
window.geometry('400x200')

# Text Widget
t = tk.Text(window, font=("Arial", 12))

t.place(x=0, y=0, width=400, height=100)
t.place(x=0, y=0, width=400, height=50)

window.mainloop()
