# import pyautogui

# myScreenshot = pyautogui.screenshot()
# myScreenshot.save(r'c:/users/seanw/downloads/image.png')
from PIL import Image, ImageGrab
from pynput.mouse import Listener

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
        im2 = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        im2.show()

def on_scroll(x, y, dx, dy):
    print("scrolled")

with Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
    listener.join()