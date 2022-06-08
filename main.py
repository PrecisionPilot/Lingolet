from PIL import Image, ImageGrab
from pynput import mouse
from pynput import keyboard
from PyQt5 import QtWidgets, QtCore, QtGui
import pyperclip
from ocr import parseImage
# import SnippingMenu


# Screenshot snipping implementation
x1 = 0
y1 = 0
x2 = 0
y2 = 0

def on_move(x, y):
    print(f"Mouse Moved, ({x}, {y})")
def on_click(x, y, button, pressed):
    print("Mouse Clicked", button, pressed)
    if pressed:
        global x1, y1
        x1 = x
        y1 = y
    else:
        global x2, y2
        x2 = x
        y2 = y

        # Make sure x1 < x2, y1 < y2
        if x1 > x2:
            tmp = x1
            x1 = x2
            x2 = tmp
        if y1 > y2:
            tmp = y1
            y1 = y2
            y2 = tmp
        
        im2 = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        im2.show()

def on_scroll(x, y, dx, dy):
    print("scrolled")

# Screenshot snipping
# with mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
#     listener.join()


def parseClipboard():
    clipboard = ImageGrab.grabclipboard()

    # Check if clipboard contains image
    if clipboard:
        # Check if clipboard is a list
        if isinstance(clipboard, list):
            # Use the clipboard image to parse
            clipboard = clipboard[0]
            text = parseImage(clipboard)
        else:
            clipboard.save("clipboard.png")
            text = parseImage("clipboard.png")
        
        # Copy to clipboard
        pyperclip.copy(text)
        print(text)

    else:
        print("Error: You do not have an image copied to clipboard")

# Hotkey implementation
with keyboard.GlobalHotKeys({'<alt>+q': parseClipboard}) as h:
    h.join()