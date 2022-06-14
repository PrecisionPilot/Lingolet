from fnmatch import translate
import tkinter as tk
from tkinter import messagebox
from tkinter import font
import deepl
from internetConnection import isConnected

class Widget():
    def __init__(self) -> None:
        # width x height
        self.size = (400, 250)
        self.inText = None
        self.outText = None

        # Initialize deepL API
        self.key = ""
        with open("deepL auth.txt", "r") as f:
            self.key = f.read()
        self.translator = deepl.Translator(self.key)

        # Other variables
        self.connected = True

    def open(self, inText=""):
        # Initialize window
        self.root = tk.Tk()
        self.root.title("Screen OCR")
        self.root.iconbitmap("icon.ico")
        self.root.geometry(str(self.size[0]) + "x" + str(self.size[1]))
        self.root.focus()
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.resizable(False, False)

        # Set variables
        self.inText = inText
        self.outText = tk.StringVar()
        self.myFont = ("Arial", 12)
        self.textHeight = self.myFont[1] * 1.75

        # Button
        self.translateButton = tk.Button(self.root, text="Translate", command=self.translate)
        # Place button at bottom right corder
        self.translateButton.grid(row=1, column=1, padx=10, pady=10, sticky="se")

        # Textbox
        self.inputBox = tk.Text(self.root, font=self.myFont)
        self.inputBox.place(x=0, y=0, width=self.size[0], height=self.size[1] / 2 - self.textHeight)
        self.inputBox.insert(tk.END, inText)
        # Translate text, then set the label accordingly
        self.translate()
        self.outputText = tk.Label(self.root, textvariable=self.outText, font=self.myFont)
        self.outputText.place(x=0, y=self.size[1] / 2)

        # Key bindings
        self.root.bind("<Escape>", self.close)
        self.root.bind("<Return>", self.translate)


        # Open widget if connected, otherwise close it
        if self.connected:
            self.root.mainloop()
        else:
            self.close()
        
        
    
    def translate(self, event=None):
        # Update "self.inText"
        self.inText = self.inputBox.get(1.0, tk.END)

        # No text error handling
        if self.inText == "":
            messagebox.showwarning(title="Error", message="Text field cannot be empty!")
            return

        # Check if there's internet connnection
        if isConnected():
            # Get text from textbox and set it as the outText variable
            self.targetText = self.translator.translate_text(self.inText, source_lang="ZH", target_lang="EN-US")
            # Set the text ok the label
            self.outText.set(self.targetText)
        else:
            self.connected = False
            messagebox.showwarning(title="Error", message="No Internet connection!")
    
    def close(self, event=None):
        self.root.destroy()

def main():
    widget = Widget()
    widget.open(inText="其实一切都如故")

if __name__ == "__main__":
    main()


# Make it so that you can show or hide window