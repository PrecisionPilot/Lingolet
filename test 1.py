import tkinter as tk
from tkinter import ttk


window = tk.Tk()
window.title("Text Widget Example")
window.geometry('600x500')
# Configure grid
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=2)

# Text Widget
text = tk.Label(window, font=("Arial", 12), text="Yo: ", bg="green")
text.place(x=0, y=0, width=100, height=100)
text.place(x=0, y=0, width=0, height=0)


window.mainloop()
