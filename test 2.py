# Import the required libraries
from tkinter import *

# Create an instance of tkinter frame or window
win=Tk()

# Set the size of the window
win.geometry("700x350")

def stay_on_top():
   win.lift()
   win.after(2000, stay_on_top)

# Add a Label widget
Label(win, text="This window will always stay on Top", font=('Aerial 14')).pack(pady=30, anchor =CENTER)

# Call function to make the window stay on top
stay_on_top()

win.mainloop()