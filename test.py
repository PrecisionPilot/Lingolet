from PIL import ImageGrab
import atexist

clipboard = ImageGrab.grabclipboard()
if clipboard:
    clipboard.save("clipboard.png")
print(clipboard)

# image = ImageGrab.grab(bbox=(0, 0, 500, 500))
# print(image)