import os
import widget
import time
import tkinter as tk
from tkinter import messagebox
from internetConnection import isConnected
from ocr import parseImage
try:
    from PIL import Image, ImageGrab
    from pynput import keyboard
    import pyperclip
    # import SnippingMenu
except:
    # Automatically install packages if they don't exist
    os.system("pip install -r requirements.txt")

popUp = widget.Widget()

# Variables
debugMode = False


# Open welcome window
popUp.welcome()


# Activation hotkey triggers this procedure
def parseClipboard():
    clipboard = ImageGrab.grabclipboard()

    # Play sound

    # Check clipboard contents
    # If clipboard contains image
    if clipboard:
        # File name returned
        if isinstance(clipboard, list):
            # Use the clipboard image to parse
            clipboard = clipboard[0]
            text = parseImage(clipboard)
        # Image file returned
        else:
            clipboard.save("Assets/clipboard.png")
            text = parseImage("Assets/clipboard.png")
        
        # Copy to clipboard if text isn't empty
        if text:
            pyperclip.copy(text)
            print(text)
            # Open translation widget
            popUp.open(text)

    # if clibpoard contains text
    elif pyperclip.paste():
        # No need to copy to clipboard
        text = pyperclip.paste()
        print(text)
        # Open translation widget
        popUp.open(text)
            
    # Clipboard contains nothing
    else:
        print("Error: Empty clipboard")
        messagebox.showwarning(title="Error", message="Your clipboard is empty")

# Check if connected to internet
if not isConnected():
    print("Warning: No internet connection")

# Hotkey implementation
if not debugMode:
    with keyboard.GlobalHotKeys({'<alt>+q': parseClipboard}) as h:
        h.join()

# Debug mode
if debugMode:
    input("Whenever you're ready: ")
    parseClipboard()