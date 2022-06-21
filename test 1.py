import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image


window = tk.Tk()
window.title("Text Widget Example")
window.geometry('600x500')
# Configure grid
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=2)

# Image
img = Image.open(r"Assets/Powered by DeepL.png")
img.resize((200, 100), Image.ANTIALIAS)
img = ImageTk.PhotoImage(img)
label = tk.Label(window, image=img)
label.place(x=100, y=100)



window.mainloop()
