import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image


window = tk.Tk()
window.title("Text Widget Example")
window.geometry('200x200')
# Configure grid
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=2)

# Label
label = tk.Label(window, text="", font=("Arial", 12), bg="blue")
label.place(x=0, y=0)
label.update()
print(label.winfo_width(), label.winfo_height())

# Text Field
# text = tk.Text(window, font=("Arial", 12))
# text.place(width=label.winfo_width(), height=label.winfo_height())
# text.insert(1.0, "Ok then")
# text.update()
# print(text.winfo_width(), text.winfo_height())


window.mainloop()
