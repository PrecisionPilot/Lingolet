import tkinter as tk
from tkinter import ttk


window = tk.Tk()
window.title("Text Widget Example")
window.geometry('400x200')
# Configure grid
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

# Text Widget
t = tk.Text(window, font=("Arial", 12))
t.grid(row=1, column=1, padx=10, pady=10, sticky="se")

# Function declaration
def a(event):
    print("A")
def b(event):
    print("B")

# Keybindings
window.bind("<Return>", a)
window.bind("<Control-Return>", b)


window.mainloop()
