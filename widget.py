from fnmatch import translate
import tkinter as tk
from tkinter import messagebox
import deepl

class Widget():

    def __init__(self) -> None:
        # width x height
        self.size = (300, 150)
        self.inText = None
        self.outText = None

        # Initialize deepL API
        self.key = ""
        with open("deepL auth.txt", "r") as f:
            self.key = f.read()
        self.translator = deepl.Translator(self.key)

    def open(self, inText=""):
        # Initialize window
        self.root = tk.Tk()
        self.root.title("Screen OCR")
        self.root.iconbitmap("icon.ico")
        self.root.geometry(str(self.size[0]) + "x" + str(self.size[1]))
        self.root.focus()
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Set variables
        self.inText = tk.StringVar()
        self.inText.set(inText)
        self.outText = tk.StringVar()

        # Textbox
        self.inputBox = tk.Entry(self.root, textvariable=self.inText)
        self.inputBox.place(x=0, y=0, width=self.size[0], height=20)
        # Translate text, then set the label accordingly
        self.translate()
        self.outputText = tk.Label(self.root, textvariable=self.outText)
        self.outputText.place(x=0, y=self.size[1] / 2)

        # Button
        self.translateButton = tk.Button(self.root, text="Translate", command=self.translate)
        # Place button at bottom right corder
        self.translateButton.grid(row=1, column=1, padx=10, pady=10, sticky="se")

        # Key bindings
        self.root.bind("<Escape>", self.close)
        self.root.bind("<Return>", self.translate)

        
        self.root.mainloop()
    
    def translate(self, event=None):
        print("Runned:", event)
        # No text error handling
        if self.inText.get() == "":
            messagebox.showwarning(title="Error", message="Text field cannot be empty!")
            return

        # Get text from textbox and set it as the outText variable
        self.targetText = self.translator.translate_text(self.inText.get(), source_lang="ZH", target_lang="EN-US")
        self.outText.set(self.targetText)
    
    def close(self, event=None):
        self.root.destroy()

def main():
    widget = Widget()
    widget.open(inText="其实一切都如故")

if __name__ == "__main__":
    main()


# Make it so that you can show or hide window