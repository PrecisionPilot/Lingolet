import tkinter as tk
from tkinter import ttk


window = tk.Tk()
window.title("Text Widget Example")
window.geometry('600x500')
# Configure grid
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=2)

# Text Widget
tk.Label(window, font=("Arial", 12), text="Yo: ").grid(row=0, column=0, padx=10, pady=10)
tk.Text(window, font=("Arial", 12)).grid(row=0, column=1, padx=10, pady=10)


window.mainloop()
