# import pyautogui

# myScreenshot = pyautogui.screenshot()
# myScreenshot.save(r'c:/users/seanw/downloads/image.png')
from PIL import Image, ImageGrab
from pynput.mouse import Listener

def on_move(x, y):
    print("Mouse Moved")
def on_click(x, y, button, pressed):
    print("Mouse Clicked")
def on_scroll(x, y, dx, dy):
    print("scrolled")

with Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
    listener.join()

# im2 = ImageGrab.grab(bbox=(0, 0, 300, 300))
# im2.show()