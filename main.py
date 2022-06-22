import os
def importPackages():
    from PIL import Image, ImageGrab
    from pynput import keyboard
    from pynput.keyboard import Key, Controller
    import pyperclip
    import tkinter as tk
    from tkinter import messagebox

    from ocr import parseImage
    from internetConnection import isConnected
    import widget
    import time
    # import SnippingMenu
try:
    importPackages()
except:
    # Automatically install packages if they don't exist
    os.system("pip install -r requirements.txt")
    importPackages()


popUp = widget.Widget()

# Variables
debugMode = False
key = Controller()


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
        
        # Prevent key-binding bugs
        time.sleep(0.5)
        key.release("q")
        time.sleep(0.1)
        key.release(Key.alt)
    
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