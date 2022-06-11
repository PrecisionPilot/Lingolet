import tkinter as tk

class Widget():

    def __init__(self) -> None:
        # width x height
        self.size = (300, 150)
        self.inText = None
        self.outText = None

    def open(self, inText="", outText="Translation text"):
        # Set variables
        self.inText = inText
        self.outText = outText

        # Open widget
        self.root = tk.Tk()
        self.root.title("Screen OCR")
        self.root.iconbitmap("icon.ico")
        self.root.geometry(str(self.size[0]) + "x" + str(self.size[1]))

        # Textbox
        self.inputBox = tk.Entry(self.root)
        self.inputBox.place(x=0, y=0, width=self.size[0], height=20)
        self.inputBox.insert(0, self.inText)

        self.outputText = tk.Label(self.root, text=self.outText)
        self.outputText.place(x=0, y=self.size[1] / 2)
        

        self.root.mainloop()

def main():
    widget = Widget()
    widget.open(inText="其实一切都如故", outText="Translation text")

if __name__ == "__main__":
    main()


# Make it so that you can show or hide window