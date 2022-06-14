import tkinter as tk
from tkinter import ttk


window = tk.Tk()
window.title("Text Widget Example")
window.geometry('400x200')

ttk.Label(window, text="Enter your comment :",
		font=("Times New Roman", 15)).grid(
column=0, row=15, padx=10, pady=25)

# Text Widget
t = tk.Text(window, width=20, height=3, font=("Arial", 12))

t.grid(column=1, row=15)

window.mainloop()
